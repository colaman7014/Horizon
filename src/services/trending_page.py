"""Standalone GitHub trending page.

Trending repos don't compete with news for digest slots; the top N by
star momentum get their own Jekyll page, overwritten on every run.
Descriptions are translated to Traditional Chinese in a single batched
LLM call, falling back to the English originals if that fails.
"""

import json
from pathlib import Path
from typing import List, Optional

from ..ai.prompts import TRENDING_TRANSLATION_SYSTEM, TRENDING_TRANSLATION_USER
from ..ai.utils import parse_json_response
from ..models import ContentItem

PAGE_HEADER = """---
layout: default
title: GitHub 每日趨勢
permalink: /github-trending/
---

# GitHub 每日趨勢 Top {top_n}

更新日期：{date_str}（每日自動更新，依過去 24 小時星數增量排名）

"""


class TrendingPageWriter:
    """Renders the daily GitHub trending page."""

    def __init__(self, ai_client=None, console=None):
        self.client = ai_client
        self.console = console

    async def write(
        self,
        items: List[ContentItem],
        date_str: str,
        path: str = "docs/github-trending.md",
        top_n: int = 10,
    ) -> Optional[Path]:
        """Write the page for the top `top_n` ranked repos; None if no items."""
        ranked = sorted(
            (i for i in items if i.metadata.get("trending_rank")),
            key=lambda i: i.metadata["trending_rank"],
        )[:top_n]
        if not ranked:
            return None

        descriptions = [(i.metadata.get("description") or "").strip() for i in ranked]
        translations = await self._translate(descriptions)

        lines = [PAGE_HEADER.format(top_n=len(ranked), date_str=date_str)]
        for item, description in zip(ranked, translations):
            repo = item.metadata.get("repo") or item.title
            stars = item.metadata.get("stars_gained", 0)
            language = item.metadata.get("primary_language") or "—"
            lines.append(f"1. **[{repo}]({item.url})** — +{stars}⭐ · {language}")
            if description:
                lines.append(f"   {description}")
            lines.append("")

        page = Path(path)
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text("\n".join(lines), encoding="utf-8")
        return page

    async def _translate(self, descriptions: List[str]) -> List[str]:
        """Batch-translate descriptions; any failure returns the originals."""
        if not self.client or not any(descriptions):
            return descriptions
        try:
            payload = json.dumps({"descriptions": descriptions}, ensure_ascii=False)
            # /no_think + a raised token cap: with the default 4096 budget
            # qwen3 spends everything thinking about 10 descriptions and
            # returns empty content (observed 2026-07-14).
            user_prompt = (
                TRENDING_TRANSLATION_USER.format(
                    count=len(descriptions), payload=payload
                )
                + "\n/no_think"
            )
            response = await self.client.complete(
                system=TRENDING_TRANSLATION_SYSTEM,
                user=user_prompt,
                max_tokens=8192,
            )
            result = parse_json_response(response)
            translations = (result or {}).get("translations")
            if isinstance(translations, list) and len(translations) == len(descriptions):
                return [
                    t.strip() if isinstance(t, str) and t.strip() else original
                    for t, original in zip(translations, descriptions)
                ]
        except Exception as e:
            if self.console:
                self.console.print(
                    f"[yellow]⚠️  Trending translation failed, keeping English: {e}[/yellow]"
                )
        return descriptions
