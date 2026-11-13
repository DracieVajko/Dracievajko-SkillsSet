# Engineering and Hardware

Read when: choosing components or architecture, power/thermal/mechanical design, BOM or bring-up testing.

Part of the `write-research-projects` method (version 2.3.0). The core rules, workflow, research and writing procedure are in `../SKILL.md`.

## Engineering Decisions

### Decision Procedure

1. State the decision and why it is needed now.
2. List hard constraints (must) separately from preferences (should).
3. Generate at least two realistic alternatives (include "keep current" and buy-vs-build where relevant).
4. Eliminate options that fail hard constraints; state why.
5. Score the rest on weighted criteria: compatibility, reliability, safety, cost, availability, performance margin, effort, repairability, user's skills and tools. Table when more than two options remain.
6. Resolve the biggest uncertainty first — by calculation, datasheet check, or minimal prototype — before committing.
7. Recommend one option; give trade-offs and the conditions that would change the decision.
8. Prefer simple, proven, documented, reversible solutions; flag irreversible choices.
9. Log the decision.

Decision record:

```text
ID / date / version:
Question or requirement:
Hard constraints:
Options considered:
Criteria and weights:
Evidence / calculations:
Decision and rationale:
Risks / assumptions:
Verification needed:
Revisit trigger:
```

### Requirements and Architecture

- Functional and non-functional requirements (accuracy, speed, reliability, safety, size, cost, maintainability) with measurable acceptance criteria.
- Operating modes, environment, worst credible case, hazards and failure consequences.
- Traceability: requirement → component → test.
- Subsystems: power, sensing, control, actuation, communication, thermal, mechanical, data, safety. Define interfaces first.
- Diagrams: separate energy, data, and control paths; legend; version; mark planned vs implemented. Subsystems first, integrate after interface check. Prefer editable formats.

## Hardware Checks

### Electrical

- Nominal, transient, and absolute-maximum voltages and currents. Absolute maximum ≠ recommended continuous rating.
- Power loss, thermal path, derating, safe operating area, heat sinking, ambient.
- Wire, connector, relay, fuse, trace, terminal ratings. Inrush, reverse polarity, short circuit, flyback, transients, isolation.
- Logic levels, gate drive, switching behavior, grounds and references, ADC range, input impedance, tolerances, calibration, error budget, filtering.
- Stored-energy hazards: batteries, capacitors, heat, moving parts, chemicals.
- Failure behavior: reset, power loss, sensor failure, communication loss, stuck relay, actuator fault, emergency stop.
- Hardware protection independent of software where software alone is inadequate; fuse placement; short-circuit risk.
- Read the full datasheet: conditions, curves, footnotes, exact suffix and revision. A headline number is not suitability.
- Never call a design "safe" or "validated" without evidence; match the claim to the testing scope.

### Mechanical / Thermal

- Dimensions, tolerances, mounting, assembly order, material properties, contact pressure, heat paths, expansion, insulation, airflow, condensation, maintenance.
- Fabricated / 3D-printed parts: material, orientation, perimeters, infill, fit tolerance, load, temperature. CAD is a proposal until fit and performance are tested.

### BOM and Change Control

- Per item: designator, exact manufacturer part number, quantity, key spec, role, alternative, status (considered / ordered / received / installed / tested).
- Keep schematic, pin map, firmware config, BOM, assembly notes, photos in sync. After a change, re-check connected subsystems.
- Old BOMs and plans stay historical until confirmed against the built system.

### Verification (Bring-Up)

Inspection → continuity/polarity → staged power-up with current limit → low-risk functional tests → instrument cross-checks → load/thermal → fault injection where safe → endurance → emergency-stop test. Record expected vs observed; investigate failures; never rerun until it passes.
