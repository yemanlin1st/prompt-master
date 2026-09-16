#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "PEFY" / "promptforge.registry.json"
GEOFABRIC = ROOT / "PEFY" / "domain-packs" / "geofabric.json"

REQUIRED_PIPELINE = [
    "PRESERVE", "RETRIEVE", "UNDERSTAND", "CLASSIFY", "REUSE", "ENRICH",
    "DECOMPOSE", "ROUTE", "RESEARCH", "EXECUTE", "VERIFY", "CHALLENGE",
    "CORRECT", "RETEST", "QUALIFY", "DELIVER", "OBSERVE", "LEARN", "CAPITALIZE"
]

REQUIRED_GATES = {
    "intent_fidelity", "correctness", "security", "privacy", "sovereignty",
    "accessibility_inclusion", "operationality", "evidence", "rollback_reversibility"
}


def load(path: Path):
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_registry(data):
    assert data["principles"]["source_preservation"] is True
    assert data["principles"]["bounded_recursion"] is True
    assert data["principles"]["human_in_command"] is True
    assert data["pipeline"] == REQUIRED_PIPELINE, "pipeline order drift detected"
    missing = REQUIRED_GATES - set(data["quality_gates"])
    assert not missing, f"missing quality gates: {sorted(missing)}"
    assert data["promotion_policy"]["require_material_improvement"] is True
    assert data["promotion_policy"]["forbid_unacceptable_regression"] is True


def validate_geofabric(data):
    assert data["canonical_crs"] == "EPSG:4326"
    assert data["analytical_world_africa_crs"] == "EPSG:8857"
    assert data["runtime_policy"]["single_provider_lock_in"] is False
    assert data["runtime_policy"]["fallback_must_preserve_security_privacy_licensing"] is True
    assert data["maturity"]["production"] == "not_qualified"


def main():
    try:
        validate_registry(load(REGISTRY))
        validate_geofabric(load(GEOFABRIC))
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"PEFY PromptForge validation FAILED: {exc}", file=sys.stderr)
        return 1
    print("PEFY PromptForge validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
