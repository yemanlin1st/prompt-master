# ΩPROMPTFORGE → Ω Mission Control Integration Handoff

## Intent

Integrate ΩPROMPTFORGE as a subordinate prompt-compilation capability under MƐTAPEFYON Ω / Ω Mission Control after qualification. Do not create a second orchestration or governance plane.

## Required adapter contract

Mission Control should receive a normalized compilation request containing:

- source prompt fingerprint
- authorized project/tenant context
- activated domain packs
- allowed capability set
- required evidence level
- risk class
- output contract

ΩPROMPTFORGE should return:

- compiled execution instruction
- preserved intent map
- capability routing decision
- required approvals
- evidence requirements
- quality-gate plan
- maturity ceiling for the current run
- machine-readable run-record payload

## Control boundaries

ΩPROMPTFORGE may recommend and compile.
Ω Mission Control owns orchestration, approval routing, execution lifecycle and operational evidence.
Human authority remains final for privileged/legal/financial/destructive/production actions.

## Fail-closed conditions

Do not proceed to privileged execution when any mandatory item is missing:

- identity
- authorization
- required secret or secure secret reference
- tenant context
- security/policy decision
- required production evidence

## Traceability

Every material compilation should retain:

`source fingerprint → compiler version → activated controls → capability routing → execution evidence → verifier result → maturity state`

## Rollback

The integration must support deterministic rollback to the previous qualified compiler baseline. A newer compiler version must never become mandatory merely because it exists.

## Initial integration sequence

1. Qualify the isolated PromptForge overlay.
2. Define a versioned adapter API/schema.
3. Add dry-run compilation in Mission Control.
4. Store run records without executing changes.
5. Enable approval-gated assisted execution.
6. Qualify controlled pilot.
7. Consider production promotion only after operational evidence.

## Current state

This document is an integration handoff specification. Mission Control integration is not yet implemented or production-qualified.
