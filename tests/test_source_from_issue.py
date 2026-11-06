#!/usr/bin/env python3
"""The source-from-issue parser's selftest, where CI finds tests. Run from repo root:

    python tests/test_source_from_issue.py

It is `scripts/source_from_issue.py --selftest`: the parse of both body shapes (the form's and the
site's, with its YAML block), the id, every refusal, and the written file checked against the real
dataset schema and validate.py's candidate rule.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from source_from_issue import selftest  # noqa: E402

if __name__ == "__main__":
    sys.exit(selftest())
