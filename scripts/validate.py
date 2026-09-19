#!/usr/bin/env python3
"""Validate radar data and repository invariants."""

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
signals = json.loads((ROOT / "data/signals.json").read_text(encoding="utf-8"))
required = {
    "id", "title", "url", "source", "published_at", "detected_on",
    "domain", "audience", "enablement_lens", "adoption_risk",
    "recommended_response", "automation",
}
seen, errors = set(), []

for index, signal in enumerate(signals):
    missing = required - signal.keys()
    if missing:
        errors.append(f"Signal {index} missing: {sorted(missing)}")
    if signal.get("id") in seen:
        errors.append(f"Duplicate signal id: {signal.get('id')}")
    seen.add(signal.get("id"))
    parsed = urlparse(signal.get("url", ""))
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append(f"Invalid URL: {signal.get('url')}")
    if signal.get("adoption_risk") not in {"low", "medium", "high"}:
        errors.append(f"Invalid risk: {signal.get('adoption_risk')}")

sources = json.loads((ROOT / "config/sources.json").read_text(encoding="utf-8"))
if not sources.get("sources"):
    errors.append("No sources configured")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(signals)} signals and {len(sources['sources'])} sources.")
