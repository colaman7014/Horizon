import json
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_daily_launch_agent_runs_at_0100():
    with (ROOT / "scripts" / "com.colalin.horizon-daily.plist").open("rb") as f:
        plist = plistlib.load(f)

    assert plist["StartCalendarInterval"] == {"Hour": 1, "Minute": 0}


def test_local_config_uses_legacy_full_enrichment():
    config = json.loads((ROOT / "data" / "config.json").read_text())

    assert config["ai"]["enrichment_top_n"] is None
