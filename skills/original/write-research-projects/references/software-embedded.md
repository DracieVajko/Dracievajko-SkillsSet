# Software and Embedded Systems

Read when: writing, reviewing or debugging software or firmware.

Part of the `write-research-projects` method (version 2.3.0). The core rules, workflow, research and writing procedure are in `../SKILL.md`.

## Before Coding

- Use cases, inputs, outputs, formats, errors, security/privacy limits, dependencies, performance, environments.
- Acceptance tests first. Modules, interfaces, state ownership, error strategy, configuration.
- Diagram only to remove ambiguity (architecture, data flow, sequence, state machine); pseudocode for uncertain algorithms.
- Technology choice: compatibility, maintainability, security, resources, ecosystem, user's skills. Compare two or more options when consequential.

## Implementation

- Inspect the repository and environment first. Preserve user work; no destructive change without permission.
- Correct, readable, modular, testable over clever. Follow repo conventions.
- Verify library/API behavior against official docs or source for the exact version. Never invent functions, flags, packages, endpoints, or hardware features.
- Validate input; explicit error handling; no hard-coded secrets; no silent data loss.
- Deliver complete runnable code: where it goes, dependencies and versions, how to run and test. Mark untested code and placeholders.
- Say whether code was run. Never claim it compiles or passes unless it did.

## Embedded / Control

- Non-blocking where monitoring must continue; explicit state machine.
- Outputs safe at startup and reset.
- Invalid or disconnected sensor stops the test. Critical limits in firmware, not in the PC application.
- Loss of host communication → safe state.
- Serial protocol: version, monotonic time, state, error flags.
- Layers: config → acquisition → calibration/filtering → derived values → safety state machine → actuation → communication → diagnostics.

## Logging

- CSV: header, timestamps, raw values, derived values, mode, error flags, units.
- Flush regularly. Store test parameters or metadata with the data.
- Raw separate from processed. Mark gaps; never invent samples.

## Testing, Debugging, Repository

- Layers: static → unit → integration → system → boundary/invalid input → fault/recovery → regression → acceptance. Expected results defined first.
- A pass is evidence only for what was tested. Report tests not run.
- Debug: reproduce → expected vs observed → logs/measurements → root cause → smallest fix → regression test → short note.
- Repo: source, tests, config examples, docs, diagrams, sample data; `.gitignore`; no secrets or bulk raw data by default; meaningful commits; changelog; update schematic/BOM/pin map with hardware changes.
