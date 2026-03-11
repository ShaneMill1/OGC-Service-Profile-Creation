# =================================================================
#
# Authors: Shane Mill <shane.mill@noaa.gov>
#
# Copyright (c) 2026 Shane Mill
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================
"""
CLI entry point.

Usage:
    ogc-edr-profile generate --config water_gauge.yaml --output ./my_profile
    ogc-edr-profile validate --config water_gauge.yaml
    ogc-edr-profile schema --output ./profile.schema.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from ogc_edr_profile.generate import generate
from ogc_edr_profile.models import ServiceProfile


def _parse_datetimes(obj):
    """Recursively convert ISO 8601 datetime strings to datetime objects for edr-pydantic."""
    from datetime import datetime
    import re
    ISO_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$')
    if isinstance(obj, dict):
        return {k: _parse_datetimes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_parse_datetimes(v) for v in obj]
    if isinstance(obj, str) and ISO_RE.match(obj):
        return datetime.fromisoformat(obj.replace('Z', '+00:00'))
    return obj


def load_config(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        return _parse_datetimes(yaml.safe_load(text))
    return _parse_datetimes(json.loads(text))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="OGC API - EDR Part 3 Service Profile Generator")
    sub = parser.add_subparsers(dest="command", required=True)

    # generate
    gen = sub.add_parser("generate", help="Validate a profile config and generate all artifacts")
    gen.add_argument("--config", required=True, type=Path, help="Profile YAML or JSON config")
    gen.add_argument("--output", required=True, type=Path, help="Output directory")

    # validate
    val = sub.add_parser("validate", help="Validate a profile config without generating output")
    val.add_argument("--config", required=True, type=Path, help="Profile YAML or JSON config")

    # schema
    sch = sub.add_parser("schema", help="Export the ServiceProfile JSON Schema")
    sch.add_argument("--output", type=Path, default=None, help="Write schema to file (default: stdout)")

    args = parser.parse_args()

    if args.command == "schema":
        schema = json.dumps(ServiceProfile.model_json_schema(), indent=2)
        if args.output:
            args.output.write_text(schema, encoding="utf-8")
            print(f"Schema written to {args.output}")
        else:
            print(schema)
        return

    if not args.config.exists():
        print(f"Error: config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)

    raw = load_config(args.config)

    try:
        profile = ServiceProfile.model_validate(raw)
    except ValidationError as exc:
        print("Profile validation failed:\n", exc, file=sys.stderr)
        sys.exit(1)

    if args.command == "validate":
        print(f"Profile '{profile.name}' is valid.")
        return

    generate(profile, args.output)


if __name__ == "__main__":
    main()
