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
PDF compilation: shell out to the Metanorma Docker image.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def compile_pdf(output_dir: Path) -> bool:
    """
    Run `docker run metanorma/metanorma compile` against document.adoc
    in output_dir. Returns True on success.
    """
    if shutil.which("docker") is None:
        print("docker not found. Install Docker to use --pdf.", file=sys.stderr)
        sys.exit(1)

    doc = output_dir / "document.adoc"
    if not doc.exists():
        print(f"document.adoc not found in {output_dir}", file=sys.stderr)
        sys.exit(1)

    fonts_dir = Path.home() / ".fontist" / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{output_dir.resolve()}:/metanorma",
        "-v", f"{fonts_dir}:/config/fonts",
        "metanorma/metanorma",
        "metanorma", "compile",
        "--agree-to-terms",
        "-t", "ogc",
        "-x", "pdf",
        "document.adoc",
    ]

    print(f"Compiling PDF via Metanorma Docker...")
    result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        pdf = output_dir / "document.pdf"
        print(f"PDF written to {pdf}")
    return result.returncode == 0
