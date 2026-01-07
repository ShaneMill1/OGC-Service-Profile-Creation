# API Reference

## create_profile.py

Main script for generating OGC API - EDR Part 3 Service Profiles.

### Command Line Usage

```bash
python src/create_profile.py [OPTIONS]
```

### Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `--name` | Profile name (lowercase, hyphens) | Yes | - |
| `--title` | Profile title | Yes | - |
| `--query-types` | Comma-separated query types | Yes | - |
| `--output` | Output directory | No | `./output` |
| `--author` | Author name | No | `Your Name` |
| `--email` | Contact email | No | `your@email.com` |

### Supported Query Types

- `items` - Items query (GeoJSON Features)
- `position` - Point location query
- `area` - Polygon area query
- `radius` - Radius around point query
- `cube` - 3D bounding box query
- `trajectory` - Path/route query
- `corridor` - Buffered path query
- `locations` - Named locations query
- `instances` - Temporal instances query

### Example

```bash
python src/create_profile.py \
  --name "water-gauge-profile" \
  --title "Water Gauge Profile" \
  --query-types items,position,area \
  --output ./profiles/water-gauge \
  --author "Shane Mill" \
  --email "shane.mill@noaa.gov"
```

### Output Structure

```
output/
├── sections/
│   ├── 00-preface.adoc
│   ├── 01-scope.adoc
│   ├── 02-conformance.adoc
│   ├── 03-references.adoc
│   ├── 04-terms.adoc
│   ├── 05-conventions.adoc
│   ├── 06-overview.adoc
│   ├── 07-requirements.adoc
│   └── annex-*.adoc
├── requirements/
│   └── requirements_class_*.adoc
├── abstract_tests/
│   └── test_*.adoc
├── document.adoc
├── Makefile
└── README.md
```

## templates.py

Contains all documentation templates used by the generator.

### Functions

#### `get_main_document_template()`
Returns the main Metanorma document template.

#### `get_section_templates()`
Returns dictionary of section templates (preface, scope, conformance, etc.).

#### `get_makefile_template()`
Returns Makefile for building the profile with Metanorma.

#### `get_readme_template()`
Returns README template for the generated profile.

## query_types.py

Query type configurations and requirements.

### Constants

#### `QUERY_TYPE_REQUIREMENTS`
Dictionary mapping query types to their requirements.

#### `QUERY_TYPE_TEST_STEPS`
Dictionary mapping query types to test steps.

#### `FORMAT_REQUIREMENTS`
Dictionary of output format requirements.

### Example

```python
from query_types import QUERY_TYPE_REQUIREMENTS

# Get requirements for items query
items_reqs = QUERY_TYPE_REQUIREMENTS['items']
```

## Building Generated Profiles

### Using Metanorma

```bash
cd output/my-profile
make
```

### Using Docker

```bash
docker run -v $(pwd):/documents metanorma/metanorma \
  metanorma compile -t ogc -x xml,html,pdf document.adoc
```

## Testing Generated Profiles

### Validate Structure

```bash
# Check all required files exist
ls sections/ requirements/ abstract_tests/

# Validate AsciiDoc syntax
asciidoctor -o /dev/null document.adoc
```

### Build Documentation

```bash
make
```

### Review Output

```bash
# Open generated PDF
open document.pdf

# Open generated HTML
open document.html
```
