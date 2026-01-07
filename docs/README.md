# OGC API - EDR Part 3 Profile Creation

Documentation for creating OGC API - Environmental Data Retrieval (EDR) Part 3 Service Profiles.

## Overview

This documentation covers the tools, processes, and best practices for creating standards-compliant OGC API - EDR Part 3 Service Profiles.

## Documentation

### Getting Started

- **[Quick Start](QUICK_REFERENCE.md)** - 5-minute quick reference guide
- **[Automated Generator Guide](GENERATOR_GUIDE.md)** - Complete guide to using the automated profile generator (recommended)
- **[Manual Creation Guide](PROFILE_CREATION_GUIDE.md)** - Step-by-step manual profile creation guide

### What are OGC API - EDR Profiles?

OGC API - Environmental Data Retrieval (EDR) Part 3 defines Service Profiles as a way to extend the base EDR standard for specific use cases. A profile specifies:

- **Requirements** - Normative statements about what implementations MUST do
- **Abstract Tests** - How to verify conformance to requirements
- **Recommendations** - Best practices (SHOULD statements)
- **API Specifications** - Machine-readable OpenAPI and AsyncAPI documents
- **Documentation** - Narrative explanations and examples

### Why Create a Profile?

Profiles provide:

1. **Standardization** - Common interface for specific use cases
2. **Interoperability** - Different implementations work together
3. **Testability** - Clear conformance criteria
4. **Documentation** - Formal specifications and guides

### Profile Creation Approaches

#### Automated (Recommended)

Use the profile generator tool:

```bash
cd create-profile
./create_profile.py
```

**Time:** 5-10 minutes  
**Difficulty:** Easy  
**Output:** Complete, standards-compliant profile

See [GENERATOR_GUIDE.md](GENERATOR_GUIDE.md) for details.

#### Manual

Create profile structure by hand following OGC standards.

**Time:** 2-3 days  
**Difficulty:** Advanced  
**Output:** Custom profile with full control

See [PROFILE_CREATION_GUIDE.md](PROFILE_CREATION_GUIDE.md) for details.

## Profile Components

### Requirements

Requirements define what implementations MUST do. Written in AsciiDoc using Metanorma syntax:

```asciidoc
[[req_feature]]
[requirement]
====
[%metadata]
identifier:: /req/profile/feature
part:: The service SHALL provide endpoint X
part:: The service SHALL return format Y
====
```

### Abstract Tests

Tests verify conformance to requirements:

```asciidoc
[[ats_feature]]
[abstract_test]
====
[%metadata]
identifier:: /conf/profile/feature
target:: /req/profile/feature
test-method::
step:: Send GET request to endpoint X
step:: Verify response format is Y
====
```

### OpenAPI Specification

Machine-readable HTTP API definition:

```yaml
openapi: 3.0.3
paths:
  /collections/{collectionId}/items:
    get:
      summary: Query items
      responses:
        '200':
          description: GeoJSON FeatureCollection
```

### AsyncAPI Specification (Optional)

Machine-readable PubSub messaging definition:

```yaml
asyncapi: 3.0.0
channels:
  notifications:
    address: collections/{collectionId}/items/#
    messages:
      update:
        payload:
          type: object
```

## Workflow

```
1. Define Use Case
   ↓
2. Generate Profile (automated) or Create Manually
   ↓
3. Customize Requirements & Tests
   ↓
4. Create API Specifications
   ↓
5. Generate PDF Documentation
   ↓
6. Implement Service
   ↓
7. Validate Conformance
```

## Standards Compliance

Profiles conform to:

- **OGC API - Common Part 1: Core** - Base API patterns
- **OGC API - EDR Part 1: Core** - Environmental data retrieval
- **OGC API - EDR Part 3: Service Profiles** - Profile structure (draft)
- **OpenAPI 3.0** - HTTP API specification
- **AsyncAPI 3.0** - PubSub messaging specification (optional)

## Example Profiles

### Water Gauge Profile

Real-time water gauge notifications with PubSub support.

**Features:**
- Items and instances query types
- GeoJSON output format
- AMQP/MQTT messaging
- Email subscriptions with filtering
- Dynamic UI generation

**Documentation:** See [Water Gauge Profile Documentation](../water-gauge-profile/docs/)

## Tools

### Profile Generator

Automated tool for creating complete profiles.

**Location:** `create-profile/`

**Features:**
- Interactive configuration
- Automatic requirement generation
- Proper Metanorma formatting
- OpenAPI/AsyncAPI generation
- Configuration file support

**Documentation:** [GENERATOR_GUIDE.md](GENERATOR_GUIDE.md)

### Metanorma

Documentation generation tool for OGC standards.

**Usage:**
```bash
make  # In profile directory
```

**Output:** PDF, HTML, DOC formats

### Validation Tools

- **Schemathesis** - OpenAPI validation
- **AsyncAPI CLI** - AsyncAPI validation
- **Custom tests** - Profile-specific validation

## Resources

### OGC Standards

- [OGC API - EDR Part 1](https://docs.ogc.org/is/19-086r5/19-086r5.html)
- [OGC API - Common](https://docs.ogc.org/is/19-072/19-072.html)
- [OGC API - Features](https://docs.ogc.org/is/17-069r4/17-069r4.html)

### Specifications

- [OpenAPI 3.0](https://spec.openapis.org/oas/v3.0.3)
- [AsyncAPI 3.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0)

### Tools

- [Metanorma](https://www.metanorma.org/)
- [Schemathesis](https://schemathesis.readthedocs.io/)
- [AsyncAPI CLI](https://www.asyncapi.com/tools/cli)

## Next Steps

1. **Read the Quick Start** - [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Try the Generator** - `cd create-profile && ./create_profile.py`
3. **Study the Example** - Review the Water Gauge Profile
4. **Create Your Profile** - Follow [GENERATOR_GUIDE.md](GENERATOR_GUIDE.md)
5. **Implement** - Build your service
6. **Validate** - Test conformance

## Contributing

To contribute to profile creation tools or documentation:

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Questions?

- **Generator usage:** See [GENERATOR_GUIDE.md](GENERATOR_GUIDE.md)
- **Manual creation:** See [PROFILE_CREATION_GUIDE.md](PROFILE_CREATION_GUIDE.md)
- **Quick reference:** See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Example profile:** See [Water Gauge Profile](../water-gauge-profile/docs/)
