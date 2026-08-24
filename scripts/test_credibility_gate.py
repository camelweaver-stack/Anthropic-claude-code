#!/usr/bin/env python3
"""Tests for the placeholder-assert credibility gate in apply_standing_fixes.py.

For each denylisted phrase: seed it into a temporary HTML page, run the gate in
--check mode, and require the build to FAIL naming placeholder-assert. Then
verify the clean tree PASSES (no false positives on the real site), and that
legitimate prose containing brackets or the word "tour" does not trip it.

Run: python3 scripts/test_credibility_gate.py   (exits nonzero on any failure)
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TMP = "zz-credibility-gate-test.html"

VIOLATIONS = [
    "[FIRST-HAND FIELD NOTE — added after an in-person visit.]",
    "[FIELD NOTE: describe parking]",
    "[PLACEHOLDER — quote goes here]",
    "FIELD PHOTO — added after an in-person visit",
    "This section was compiled after in-person visits.",
    "Our field-checked commute notes below.",
    "We visited the leasing office on Tuesday.",
    "We toured every floor plan.",
    "Locals report the pool is crowded.",
    "[TODO: verify the pet fee]",
    "[insert photo of the clubhouse]",
    "Lorem ipsum dolor sit amet.",
]

LEGITIMATE = [
    "Confirm the live offer by phone the morning you tour.",
    "The 3-bedroom [floor plan B] starts at the advertised rate.",
    "Todo: en español esta palabra es normal — aquí ocurre todo: la inspección.",
    "Public mapping estimates place the off-peak drive around 12 minutes.",
]


def run_gate():
    r = subprocess.run([sys.executable, "scripts/apply_standing_fixes.py", "--check"],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def seed(text):
    with open(TMP, "w", encoding="utf-8") as f:
        f.write(f"<html><head><title>t</title></head><body><p>{text}</p></body></html>")


def main():
    failures = []
    try:
        for v in VIOLATIONS:
            seed(v)
            code, out = run_gate()
            if code == 0 or "placeholder-assert" not in out:
                failures.append(f"NOT CAUGHT: {v!r}")
            else:
                print(f"  caught   {v[:58]!r}")
        for ok_text in LEGITIMATE:
            seed(ok_text)
            code, out = run_gate()
            if "placeholder-assert" in out and TMP in out:
                failures.append(f"FALSE POSITIVE: {ok_text!r}")
            else:
                print(f"  allowed  {ok_text[:58]!r}")
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)
    code, out = run_gate()
    if code != 0:
        failures.append("clean tree does not pass the gate:\n" + out[-600:])
    else:
        print("  clean tree passes")
    if failures:
        print("\nGATE TEST FAILED:")
        for f in failures:
            print("  ✗ " + f)
        return 1
    print(f"\nGATE TEST PASSED — {len(VIOLATIONS)} violations caught, "
          f"{len(LEGITIMATE)} legitimate phrasings allowed, clean tree green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
