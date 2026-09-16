#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PEFY = ROOT / "PEFY"
REGISTRY = PEFY / "promptforge.registry.json"
GEOFABRIC = PEFY / "domain-packs" / "geofabric.json"
DOMAIN_TEMPLATE = PEFY / "domain-packs" / "_template.json"
RUN_SCHEMA = PEFY / "run-record.schema.json"
SAMPLE_RUN = PEFY / "tests" / "sample_geofabric_run.json"

REQUIRED_PIPELINE = [
    "PRESERVE", "RETRIEVE", "UNDERSTAND", "CLASSIFY", "REUSE", "ENRICH",
    "DECOMPOSE", "ROUTE", "RESEARCH", "EXECUTE", "VERIFY", "CHALLENGE",
    "CORRECT", "RETEST", "QUALIFY", "DELIVER", "OBSERVE", "LEARN", "CAPITALIZE"
]

REQUIRED_GATES = {
    "intent_fidelity", "correctness", "security", "privacy", "sovereignty",
    "accessibility_inclusion", "operationality", "evidence", "rollback_reversibility"
}

REQUIRED_RUN_FIELDS = {
    "run_id", "source_fingerprint", "intent_classes", "activated_domain_packs",
    "capabilities_used", "evidence_state", "quality_gates", "maturity", "residual_gaps"
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
    assert data["principles"]["no_architecture_sprawl"] is True
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
    assert data["runtime_policy"]["precise_location_default"] == "minimum_necessary_precision"
    assert data["maturity"]["production"] == "not_qualified"


def validate_domain_template(data):
    assert data["inherits"] == ["PEFY ΩPROMPTFORGE"]
    assert data["provider_policy"]["provider_neutral"] is True
    assert data["maturity"]["production"] == "not_qualified"


def validate_run_schema(data):
    assert data["type"] == "object"
    assert data["additionalProperties"] is False
    required = set(data["required"])
    missing = REQUIRED_RUN_FIELDS - required
    assert not missing, f"run schema missing required fields: {sorted(missing)}"
    props = data["properties"]
    assert set(props["evidence_state"]["enum"]) >= {
        "VERIFIED", "OBSERVED", "REPORTED", "INFERRED", "ASSUMED", "PROPOSED", "TO_VERIFY"
    }
    assert "PRODUCTION_QUALIFIED" in props["maturity"]["enum"]
    assert "REQUIRES_AUTHORIZATION" in props["intent_classes"]["items"]["enum"]


def validate_sample_run(sample, schema, registry):
    missing = REQUIRED_RUN_FIELDS - set(sample)
    assert not missing, f"sample run missing fields: {sorted(missing)}"
    allowed_intents = set(schema["properties"]["intent_classes"]["items"]["enum"])
    assert set(sample["intent_classes"]) <= allowed_intents, "sample has unknown intent class"
    allowed_evidence = set(schema["properties"]["evidence_state"]["enum"])
    assert sample["evidence_state"] in allowed_evidence, "sample has invalid evidence state"
    allowed_maturity = set(schema["properties"]["maturity"]["enum"])
    assert sample["maturity"] in allowed_maturity, "sample has invalid maturity"
    assert "geofabric" in sample["activated_domain_packs"]
    assert "geofabric" in registry["domain_packs"]
    sample_gates = set(sample["quality_gates"])
    missing_gates = REQUIRED_GATES - sample_gates
    assert not missing_gates, f"sample run missing quality gates: {sorted(missing_gates)}"
    assert sample["quality_gates"]["operationality"] != "PASS", (
        "sample must not claim full operationality before concrete provider adapters are qualified"
    )
    assert sample["maturity"] not in {"PRODUCTION_QUALIFIED", "LIVE"}, (
        "sample may not claim production/live maturity"
    )


def main():
    try:
        registry = load(REGISTRY)
        schema = load(RUN_SCHEMA)
        validate_registry(registry)
        validate_geofabric(load(GEOFABRIC))
        validate_domain_template(load(DOMAIN_TEMPLATE))
        validate_run_schema(schema)
        validate_sample_run(load(SAMPLE_RUN), schema, registry)
    except (AssertionError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"PEFY PromptForge validation FAILED: {exc}", file=sys.stderr)
        return 1
    print("PEFY PromptForge validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
