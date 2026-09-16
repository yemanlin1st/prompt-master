#!/usr/bin/env python3
"""Reference deterministic compiler for the PEFY ΩPROMPTFORGE overlay.

This tool does not call an LLM or external provider. It preserves source intent,
activates matching domain packs, emits an execution envelope, and records the
maturity ceiling and authorization boundaries for downstream orchestration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PEFY = ROOT / "PEFY"
REGISTRY_PATH = PEFY / "promptforge.registry.json"
DOMAIN_DIR = PEFY / "domain-packs"

AUTHORIZATION_TERMS = {
    "connect", "install", "activate", "deploy", "publish", "merge", "delete",
    "credential", "credentials", "api key", "secret", "production", "live"
}
VERIFY_TERMS = {
    "latest", "current", "real", "verify", "check", "search", "benchmark",
    "price", "pricing", "law", "standard", "version", "provider"
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fingerprint(source: str) -> str:
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def domain_packs() -> list[tuple[str, dict[str, Any]]]:
    packs: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(DOMAIN_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue
        packs.append((path.stem, load_json(path)))
    return packs


def match_pack(source: str, pack: dict[str, Any]) -> tuple[bool, list[str]]:
    lowered = source.lower()
    activation = pack.get("activation", {})
    signals: list[str] = []
    for group in ("keywords", "project_signals", "risk_signals"):
        for term in activation.get(group, []):
            if term.lower() in lowered:
                signals.append(term)
    return bool(signals), sorted(set(signals))


def classify_intent(source: str, activated: list[str]) -> list[str]:
    lowered = source.lower()
    classes = {"MUST_PRESERVE"}
    if activated:
        classes.update({"MAY_ENRICH", "MAY_OPTIMIZE"})
    if any(term in lowered for term in VERIFY_TERMS):
        classes.add("MUST_VERIFY")
    if any(term in lowered for term in AUTHORIZATION_TERMS):
        classes.add("REQUIRES_AUTHORIZATION")
    order = [
        "MUST_PRESERVE", "MUST_NOT_ALTER", "MAY_ENRICH", "MAY_OPTIMIZE",
        "MUST_VERIFY", "REQUIRES_AUTHORIZATION"
    ]
    return [item for item in order if item in classes]


def build_compiled_prompt(
    source: str,
    registry: dict[str, Any],
    activated: list[tuple[str, dict[str, Any], list[str]]],
    intent_classes: list[str],
) -> str:
    lines = [
        "PEFY ΩPROMPTFORGE COMPILED EXECUTION ENVELOPE",
        "",
        "SOURCE INTENT — authoritative; preserve meaning:",
        source.strip(),
        "",
        "COMPILATION RULES:",
        "- Preserve original objective, constraints, names, scope, and prior approved decisions.",
        "- Reuse before creating duplicate agents, skills, services, repositories, or control planes.",
        "- Apply only controls materially relevant to this mission.",
        "- Distinguish verified/observed/reported/inferred/assumed/proposed/to-verify information.",
        "- Never claim production/live status without target-environment evidence.",
        "- Fail closed where mandatory identity, authorization, secrets, policy, or evidence are missing.",
        "- Continue independent authorized work when one branch is blocked.",
        "- Promote only measurable improvements without unacceptable regression.",
        "- Human authority remains final for privileged, legal, financial, destructive, and production actions.",
        "",
        f"INTENT CLASSES: {', '.join(intent_classes)}",
    ]

    if activated:
        lines.extend(["", "ACTIVATED DOMAIN PACKS:"])
        for slug, pack, signals in activated:
            lines.append(f"- {slug}: {pack.get('name', slug)}")
            lines.append(f"  Activation evidence: {', '.join(signals)}")
            controls = pack.get("mandatory_controls", [])
            if controls:
                lines.append(f"  Mandatory controls: {', '.join(controls)}")
            if slug == "geofabric":
                lines.extend([
                    "  Geospatial rule: use a provider-neutral capability contract; Google Maps may be first-class but not an irreversible dependency.",
                    f"  CRS: canonical {pack.get('canonical_crs')}; world/Africa analytical {pack.get('analytical_world_africa_crs')}.",
                    "  Treat precise location as sensitive and use minimum necessary precision.",
                    "  Do not treat public community endpoints as guaranteed production capacity.",
                ])

    lines.extend([
        "",
        "QUALITY GATES:",
        "- " + ", ".join(registry.get("quality_gates", [])),
        "",
        "EXECUTION LOOP:",
        "- " + " → ".join(registry.get("pipeline", [])),
        "",
        "STOP CONDITIONS:",
        "- Stop recursive improvement when acceptance criteria are satisfied, further progress requires unavailable authorization/evidence, or another iteration has negligible expected value.",
        "",
        "OUTPUT REQUIREMENT:",
        "Deliver the best execution-ready real-world result, state residual gaps accurately, and capitalize reusable value without duplicating architecture.",
    ])
    return "\n".join(lines).strip() + "\n"


def compile_source(source: str) -> dict[str, Any]:
    if not source or not source.strip():
        raise ValueError("source prompt must not be empty")
    registry = load_json(REGISTRY_PATH)
    activated: list[tuple[str, dict[str, Any], list[str]]] = []
    for slug, pack in domain_packs():
        matched, signals = match_pack(source, pack)
        if matched:
            activated.append((slug, pack, signals))

    activated_slugs = [slug for slug, _, _ in activated]
    classes = classify_intent(source, activated_slugs)
    compiled_prompt = build_compiled_prompt(source, registry, activated, classes)

    quality_gates = {gate: "TO_VERIFY" for gate in registry.get("quality_gates", [])}
    quality_gates["intent_fidelity"] = "PASS"
    quality_gates["rollback_reversibility"] = "PASS"

    boundaries: list[str] = []
    if "REQUIRES_AUTHORIZATION" in classes:
        boundaries.append("privileged or external-account actions require explicit valid authorization and available credentials/permissions")

    run_record = {
        "run_id": fingerprint(source)[:23],
        "source_fingerprint": fingerprint(source),
        "intent_classes": classes,
        "activated_domain_packs": activated_slugs,
        "capabilities_used": ["omega_promptforge_reference_compiler"],
        "evidence_state": "OBSERVED",
        "quality_gates": quality_gates,
        "maturity": "SPECIFIED",
        "material_improvements": [
            "source intent preserved verbatim inside the execution envelope",
            "relevant domain controls activated deterministically",
            "authorization and evidence boundaries made explicit",
        ],
        "regressions_checked": [
            "no source prompt deletion",
            "no automatic production claim",
            "no external credentials consumed",
        ],
        "authorization_boundaries": boundaries,
        "residual_gaps": [
            "downstream execution and domain-specific verification remain separate governed stages"
        ],
        "next_action": "route compiled prompt through authorized Mission Control execution and verification path",
    }

    return {
        "compiler": "PEFY ΩPROMPTFORGE reference compiler",
        "compiler_version": registry.get("version"),
        "source_prompt": source,
        "compiled_prompt": compiled_prompt,
        "activation": {
            slug: {"signals": signals} for slug, _, signals in activated
        },
        "run_record": run_record,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile a prompt through the PEFY ΩPROMPTFORGE overlay")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="source prompt text")
    source.add_argument("--prompt-file", type=Path, help="UTF-8 file containing the source prompt")
    parser.add_argument("--output", type=Path, help="write JSON output to this file; stdout otherwise")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.prompt_file:
        source = args.prompt_file.read_text(encoding="utf-8")
    else:
        source = args.prompt
    result = compile_source(source)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
