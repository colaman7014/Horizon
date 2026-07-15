"""Selection policy for expensive second-pass enrichment."""

from collections.abc import Sequence
from typing import Optional

from ..models import ContentItem


def select_items_for_enrichment(
    items: Sequence[ContentItem],
    top_n: Optional[int],
) -> list[ContentItem]:
    """Return the selected prefix for full enrichment.

    Items are already score-sorted by the orchestrator/filter stage. ``None``
    preserves legacy behavior by enriching every selected item.
    """
    if top_n is None:
        return list(items)
    return list(items[:top_n])
