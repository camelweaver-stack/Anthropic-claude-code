#!/bin/bash
# Pre-deploy gate for northfwliving.com. Run from anywhere; exits non-zero
# (and the deploy must be aborted) if any check fails.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SITE="${1:-$HERE/../northfwliving}"

echo "== credibility validator =="
python3 "$HERE/validate_credibility.py" "$SITE"

echo "== technical validator (canonicals, hreflang, links, sitemap) =="
python3 "$HERE/validate_technical.py" "$SITE"

echo "== builder ledger data validation =="
python3 "$HERE/validate_ledger_data.py"

echo "== validator self-tests =="
python3 "$HERE/tests/test_validators.py" 2>&1 | tail -3

echo "ALL CHECKS PASSED"
