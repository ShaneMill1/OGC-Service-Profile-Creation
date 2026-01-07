# Profile Creation Quick Reference

## Overview

Create OGC API - EDR Part 3 profiles with requirements, tests, and machine-readable specifications.

## The Process

```
1. Requirements & Tests → 2. Generate PDF → 3. Create Specs → 4. Validate
   (requirements/)          (water_gauge_     (openapi.yaml,    (schemathesis,
   (abstract_tests/)         profile.adoc →    asyncapi.yaml)    custom tests)
   (sections/)               water_gauge_
                             profile.pdf +
                             OGC validation)
```

## File Structure

```
your-profile/
├── requirements/
│   ├── requirements_class_*.adoc
│   └── core/REQ_*.adoc
├── abstract_tests/
│   ├── ATS_class_*.adoc
│   └── core/ATS_*.adoc
├── recommendations/
│   └── core/REC_*.adoc
├── sections/
│   ├── clause_2_conformance.adoc
│   └── clause_7_*.adoc
├── water_gauge_profile.adoc
├── openapi.yaml
└── asyncapi.yaml
```

## Step 1: Requirements & Tests

**Requirements** define what implementations MUST do:
```asciidoc
[[req_feature]]
[requirement]
====
identifier:: /req/profile/feature
statement:: The service SHALL implement feature X
====
```

**Abstract Tests** define how to verify:
```asciidoc
[[ats_feature]]
[abstract_test]
====
identifier:: /conf/profile/feature
target:: /req/profile/feature
test-purpose:: Verify feature X works
test-method:: Steps to test
====
```

**Recommendations** provide best practices:
```asciidoc
[[rec_feature]]
[recommendation]
====
identifier:: /rec/profile/feature
statement:: The service SHOULD optimize for Y
====
```

**Sections** contain narrative documentation in `sections/` directory.

## Step 2: Generate PDF

```bash
docker run --rm -v "$(pwd)":/metanorma \
  -v ${HOME}/.fontist/fonts/:/config/fonts \
  metanorma/metanorma metanorma compile \
  --agree-to-terms -t ogc -x pdf water_gauge_profile.adoc
```

Input: `water_gauge_profile.adoc`
Output: `water_gauge_profile.pdf`

This process also validates OGC documentation structure and requirements formatting.

## Step 3: Create Specifications

### openapi.yaml
HTTP API specification with OGC extensions:
```yaml
paths:
  /collections/water_gauge/items/{featureId}:
    get:
      parameters:
        - name: featureId
          in: path
          required: true
      responses:
        '200':
          description: GeoJSON Feature

components:
  schemas:
    WaterGaugeFeature:
      type: object
      x-ogc-edr-water-gauge-profile-pubsub:
        asyncapi: /asyncapi.yaml
        channel: water_gauge_notifications
```

### asyncapi.yaml
PubSub specification with OGC extensions:
```yaml
channels:
  water_gauge_notifications:
    address: collections/water_gauge/items/#
    x-ogc-subscription:
      filters:
        - name: flood_stage
          schema:
            type: string
            enum: [action, minor, moderate, major]
```

**Optional:** Link to HTTP subscription endpoint:
```yaml
info:
  x-ogc-subscription-api: /api/subscribe
```

## Step 4: Validate

### OpenAPI Validation
```bash
pip install schemathesis
schemathesis run -u http://localhost:5000 /path/to/openapi.yaml

# Exclude specific paths if needed
schemathesis run \
  --exclude-path="/collections/cwa/items" \
  -u http://localhost:5000 \
  /path/to/openapi.yaml
```

### AsyncAPI Validation
```bash
./custom_amqp_test/test_asyncapi_amqp.py asyncapi.yaml
```

## Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| Requirements | What MUST be done | `requirements/core/REQ_*.adoc` |
| Abstract Tests | How to verify | `abstract_tests/core/ATS_*.adoc` |
| Recommendations | Best practices | `recommendations/core/REC_*.adoc` |
| Sections | Narrative docs | `sections/clause_*.adoc` |
| OpenAPI | HTTP API spec | `openapi.yaml` |
| AsyncAPI | PubSub spec | `asyncapi.yaml` |

## Quick Commands

```bash
# Generate PDF
docker run --rm -v "$(pwd)":/metanorma \
  -v ${HOME}/.fontist/fonts/:/config/fonts \
  metanorma/metanorma metanorma compile \
  --agree-to-terms -t ogc -x pdf water_gauge_profile.adoc

# Validate OpenAPI
schemathesis run -u http://localhost:5000 /path/to/openapi.yaml

# Validate AsyncAPI
./custom_amqp_test/test_asyncapi_amqp.py asyncapi.yaml

# View specs
cat openapi.yaml
cat asyncapi.yaml
```

## Next Steps

For detailed guidance, see [PROFILE_CREATION_GUIDE.md](PROFILE_CREATION_GUIDE.md)
