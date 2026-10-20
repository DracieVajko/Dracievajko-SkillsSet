# Debugging Rules
1. Capture the symptom, environment, versions and exact error.
2. Reproduce the failure or state why reproduction is unavailable.
3. Establish expected versus observed behavior.
4. Locate the earliest causal failure, not merely the final exception.
5. Form a small set of testable hypotheses.
6. Run the cheapest test that distinguishes leading hypotheses.
7. Change one causal factor at a time when practical.
8. Implement the smallest root-cause fix.
9. Add a regression test or equivalent reproducible verification.
10. Remove temporary diagnostics and inspect for side effects.
After two unsuccessful speculative fixes, return to evidence gathering.
Never hide failures by weakening tests, disabling validation or swallowing errors.
