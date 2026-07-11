from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "index.md"
CONFIG = DOCS / "_config.yml"
SCRIPT = DOCS / "assets" / "js" / "horizon.js"
HOME_LAYOUT = DOCS / "_layouts" / "home.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_homepage_source_uses_only_traditional_chinese_labels() -> None:
    combined = "\n".join([read(INDEX), read(CONFIG)])
    simplified_fragments = [
        "欢迎",
        "文档",
        "信息",
        "配置",
        "采集",
        "评分",
        "订阅",
        "暂无",
        "驱动",
        "每日速递",
    ]

    assert not [fragment for fragment in simplified_fragments if fragment in combined]
    assert "每日新聞彙整" in combined
    assert "尚無每日彙整" in combined


def test_homepage_lists_only_completed_daily_zh_posts() -> None:
    index = read(INDEX)

    assert "layout: home" in index
    assert "site.posts | where: \"lang\", \"zh\"" in index
    assert "配置指南" not in index
    assert "信息源采集器" not in index
    assert "评分系统" not in index
    assert "Welcome to" not in index
    assert "Documentation" not in index
    assert "lang-en" not in index
    assert "feed-en" not in index


def test_language_toggle_is_not_injected() -> None:
    script = read(SCRIPT)

    assert "lang-toggle" not in script
    assert "setupLanguageToggle" not in script
    assert "horizon-lang" not in script
    assert "btnEn" not in script


def test_home_layout_does_not_render_cayman_project_chrome() -> None:
    layout = read(HOME_LAYOUT)

    assert "page-header" not in layout
    assert "project-tagline" not in layout
    assert "View on GitHub" not in layout
    assert "site-footer" not in layout
    assert "{{ content }}" in layout
