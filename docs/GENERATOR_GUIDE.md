# Profile Generator Guide

Complete guide to using the automated OGC API - EDR Part 3 Profile Generator.

## Overview

The profile generator (`create_profile.py`) automates the creation of complete OGC API - EDR Part 3 Service Profiles, including:

- ✅ Requirements and abstract tests with proper Metanorma formatting
- ✅ Requirements classes and conformance classes
- ✅ OpenAPI 3.0 specifications with proper endpoints
- ✅ AsyncAPI 3.0 specifications (optional)
- ✅ Complete documentation structure
- ✅ Makefile for PDF generation
- ✅ Validation scripts

**Time savings**: What used to take days now takes minutes!

## Quick Start

### Interactive Mode

```bash
cd create-profile
./create_profile.py
```

The generator will prompt you for:
1. Profile name and title
2. Collections and query types
3. Output formats
4. GeoJSON properties (if using items query type)
5. AsyncAPI/PubSub support (optional)
6. Filters (optional)

### Configuration File Mode

```bash
cd create-profile
./create_profile.py my_profile/profile_config.yml
```

Regenerates the entire profile from a saved configuration file.

## Features

### Supported Query Types

The generator supports all OGC API - EDR query types:

- **items** - Feature collection queries (generates `/items` and `/items/{featureId}` endpoints)
- **position** - Point queries
- **area** - Polygon/area queries
- **cube** - 3D bounding box queries
- **trajectory** - Path queries
- **corridor** - Corridor queries
- **locations** - Named location queries (generates `/locations` and `/locations/{locationId}` endpoints)
- **instances** - Time instance queries

### Supported Output Formats

- **GeoJSON** - Standard GeoJSON output
- **CoverageJSON** - Coverage data format
- **CSV** - Comma-separated values
- **NetCDF** - Network Common Data Form
- **GRIB/GRIB2** - Gridded binary data
- **Zarr** - Chunked array storage

### Automatic Requirement Generation

The generator creates requirements for:

1. **OpenAPI specification** - Validates API documentation
2. **Collection metadata** - One per collection
3. **Query type support** - One per query type per collection
4. **Output formats** - One per collection with format-specific requirements
5. **AsyncAPI specification** - If PubSub is enabled
6. **Filters** - If filters are defined

### Automatic Test Generation

For each requirement, the generator creates:

- Properly formatted abstract test with `test-method::` and `step::` syntax
- Test steps specific to the query type or feature
- Correct anchor IDs and identifier paths
- Proper linkage to requirements

## Generated Structure

```
my_profile/
├── requirements/
│   ├── core/
│   │   ├── REQ_openapi.adoc
│   │   ├── REQ_collection-my-profile.adoc
│   │   ├── REQ_data-query-items-my-profile.adoc
│   │   └── REQ_output-format-my-profile.adoc
│   └── requirements_class_core.adoc
├── abstract_tests/
│   ├── core/
│   │   ├── ATS_openapi.adoc
│   │   ├── ATS_collection-my-profile.adoc
│   │   ├── ATS_data-query-items-my-profile.adoc
│   │   └── ATS_output-format-my-profile.adoc
│   └── ATS_class_core.adoc
├── sections/
│   ├── clause_0_front_material.adoc
│   ├── clause_1_scope.adoc
│   ├── clause_2_conformance.adoc
│   ├── clause_3_references.adoc
│   ├── clause_4_terms_and_definitions.adoc
│   ├── clause_5_conventions.adoc
│   ├── clause_6_context.adoc
│   ├── clause_7_my_profile.adoc
│   ├── annex-a.adoc
│   ├── annex-history.adoc
│   └── annex-bibliography.adoc
├── custom_amqp_test/
│   └── test_asyncapi_amqp.py
├── openapi.yaml
├── asyncapi.yaml (if enabled)
├── my_profile_profile.adoc
├── Makefile
├── metanorma.yml
├── profile_config.yml
└── README.md
```

## Usage Examples

### Example 1: Simple Items-Only Profile

```bash
./create_profile.py
```

**Prompts:**
```
Profile name: weather_stations
Profile title: Weather Stations
Number of collections: 1
  Collection name: stations
  Query types: items
  Output formats: GeoJSON
GeoJSON Feature properties: station_id,temperature,humidity,timestamp
Include AsyncAPI? n
Use suggested requirements? y
Use suggested tests? y
```

**Result:** Complete profile with items query support, no PubSub.

### Example 2: Multi-Collection Profile with PubSub

```bash
./create_profile.py
```

**Prompts:**
```
Profile name: marine_data
Profile title: Marine Data
Number of collections: 2
  Collection 1 name: buoys
  Query types: items,position
  Output formats: GeoJSON,CSV
  Collection 2 name: ships
  Query types: items,trajectory
  Output formats: GeoJSON
GeoJSON Feature properties: vessel_id,speed,heading,timestamp
Include AsyncAPI? y
Number of filters: 2
  Filter 1 name: vessel_type
  Filter 1 description: Type of vessel
  Filter 1 type: string
  Filter 2 name: speed_threshold
  Filter 2 description: Minimum speed
  Filter 2 type: number
Use suggested requirements? y
Use suggested tests? y
```

**Result:** Complete profile with multiple collections, query types, and PubSub support.

### Example 3: Using Configuration File

After creating a profile, the configuration is saved to `profile_config.yml`:

```yaml
profile_name: weather_stations
profile_title: Weather Stations
collections:
- name: stations
  query_types:
  - items
  formats:
  - GeoJSON
properties:
- station_id
- temperature
- humidity
- timestamp
filters: []
include_asyncapi: false
requirements:
- id: openapi
  statement: OpenAPI specification
  parts:
  - The service SHALL provide an OpenAPI 3.0 specification
  - The OpenAPI SHALL document all collection endpoints
  - The OpenAPI SHALL include GeoJSON schemas
# ... more requirements
tests:
- id: openapi
  req_id: openapi
  steps:
  - Send GET request to /openapi
  - Verify response is valid OpenAPI 3.0 document
  # ... more steps
```

To regenerate from config:
```bash
./create_profile.py weather_stations/profile_config.yml
```

This is useful for:
- Regenerating after template updates
- Version control of profile definitions
- Batch profile generation
- CI/CD integration

## Customization

### After Generation

The generator creates a complete, working profile, but you'll likely want to customize:

1. **Edit requirements** - Add profile-specific details
2. **Enhance tests** - Add more specific test steps
3. **Update sections** - Add narrative documentation
4. **Customize OpenAPI** - Add specific parameters or schemas
5. **Enhance AsyncAPI** - Add message examples

### Modifying Templates

The generator uses modular templates in:
- `templates.py` - Documentation templates
- `query_types.py` - Query type configurations

To add a new query type:

1. Edit `query_types.py`:
```python
QUERY_TYPE_REQUIREMENTS["my_query"] = {
    "statement": "{collection_name} my query support",
    "parts": [
        "The service SHALL provide a /collections/{collection_name}/my_query endpoint",
        "The query SHALL accept custom parameters",
        "The response SHALL return appropriate data"
    ]
}

QUERY_TYPE_TEST_STEPS["my_query"] = [
    "Send GET request to /collections/{collection_name}/my_query",
    "Verify response is valid",
    "Verify custom parameters are supported"
]
```

2. Regenerate profiles with the new query type available

## Workflow Integration

### Development Workflow

```
1. Generate profile
   └─> ./create_profile.py

2. Review generated files
   └─> Check requirements, tests, specs

3. Customize as needed
   └─> Edit .adoc files, YAML specs

4. Generate PDF
   └─> make

5. Validate
   └─> schemathesis, custom tests

6. Iterate
   └─> Update config, regenerate
```

### CI/CD Integration

```yaml
# .github/workflows/profile-validation.yml
name: Validate Profile

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Generate Profile
        run: |
          cd create-profile
          ./create_profile.py ../my_profile/profile_config.yml
      
      - name: Generate PDF
        run: |
          cd my_profile
          make
      
      - name: Validate OpenAPI
        run: |
          pip install schemathesis
          schemathesis run -u http://localhost:5000 my_profile/openapi.yaml
```

## Comparison: Manual vs Automated

### Manual Profile Creation

**Time:** 2-3 days

**Steps:**
1. Create directory structure (30 min)
2. Write requirements (4-6 hours)
3. Write tests (4-6 hours)
4. Create requirements/conformance classes (1 hour)
5. Write documentation sections (2-3 hours)
6. Create OpenAPI spec (2-3 hours)
7. Create AsyncAPI spec (2-3 hours)
8. Debug Metanorma linkage errors (2-4 hours)
9. Create supporting files (1 hour)

**Error-prone areas:**
- Anchor ID formatting
- Requirement/test linkage
- Conformance class structure
- Missing includes in annex-a

### Automated Profile Creation

**Time:** 5-10 minutes

**Steps:**
1. Run generator (2 min)
2. Answer prompts (3-5 min)
3. Review generated files (2-3 min)

**Benefits:**
- ✅ Correct anchor ID format
- ✅ Proper requirement/test linkage
- ✅ Valid conformance class structure
- ✅ All includes properly configured
- ✅ Consistent formatting
- ✅ No Metanorma errors

## Troubleshooting

### Common Issues

**Issue:** "Module not found: templates"
```bash
# Solution: Run from create-profile directory
cd create-profile
./create_profile.py
```

**Issue:** "Permission denied"
```bash
# Solution: Make script executable
chmod +x create_profile.py
```

**Issue:** Generated PDF has errors
```bash
# Solution: Check Metanorma output
cd my_profile
make 2>&1 | grep -i error
```

### Getting Help

1. Check generated `README.md` in profile directory
2. Review [PROFILE_CREATION_GUIDE.md](../PROFILE_CREATION_GUIDE.md) for manual details
3. Examine [water-gauge-profile](../water-gauge-profile/) as reference
4. Check Metanorma logs: `my_profile.asciidoc.log.txt`

## Advanced Usage

### Custom Requirement Templates

Create custom requirements by editing the config file:

```yaml
requirements:
- id: custom-feature
  statement: Custom feature support
  parts:
  - The service SHALL implement custom feature X
  - The feature SHALL support parameter Y
  - The response SHALL include field Z
```

Then regenerate:
```bash
./create_profile.py my_profile/profile_config.yml
```

### Batch Profile Generation

Generate multiple profiles from configs:

```bash
for config in configs/*.yml; do
    ./create_profile.py "$config"
done
```

### Profile Variants

Create variants by modifying config:

```bash
# Base profile
./create_profile.py base_config.yml

# Variant with AsyncAPI
cp base_config.yml variant_config.yml
# Edit variant_config.yml: include_asyncapi: true
./create_profile.py variant_config.yml
```

## Best Practices

1. **Start with generator** - Let it create the structure
2. **Save configuration** - Version control `profile_config.yml`
3. **Customize incrementally** - Small changes, test often
4. **Generate PDF frequently** - Catch errors early
5. **Use water-gauge as reference** - It's a complete example
6. **Document customizations** - Add comments to config file

## Next Steps

1. **Generate your first profile** - Try the quick start
2. **Review generated files** - Understand the structure
3. **Customize as needed** - Add profile-specific details
4. **Generate PDF** - Validate with Metanorma
5. **Create implementation** - Build the actual service
6. **Validate** - Test against specifications

For more details on profile concepts, see [PROFILE_CREATION_GUIDE.md](../PROFILE_CREATION_GUIDE.md).
