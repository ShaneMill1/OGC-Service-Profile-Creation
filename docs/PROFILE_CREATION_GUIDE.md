# Profile Creation Guide

Complete guide to creating OGC API - EDR Part 3 Service Profiles.

## Table of Contents

1. [Overview](#overview)
2. [The Profile Creation Workflow](#the-profile-creation-workflow)
3. [Step 1: Requirements & Abstract Tests](#step-1-requirements--abstract-tests)
4. [Step 2: Recommendations & Sections](#step-2-recommendations--sections)
5. [Step 3: Generate PDF Documentation](#step-3-generate-pdf-documentation)
6. [Step 4: Create API Specifications](#step-4-create-api-specifications)
7. [Step 5: Validate Implementation](#step-5-validate-implementation)
8. [Best Practices](#best-practices)
9. [Examples](#examples)

## Overview

An OGC API - EDR Part 3 Service Profile defines:
- **Requirements**: What implementations MUST do
- **Abstract Tests**: How to verify conformance
- **Recommendations**: Best practices
- **Sections**: Narrative documentation
- **Specifications**: Machine-readable API definitions (OpenAPI, AsyncAPI)

## The Profile Creation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Requirements & Abstract Tests                       │
│ Define what implementations must do and how to test         │
│ Files: requirements/*, abstract_tests/*                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Recommendations & Sections                          │
│ Add best practices and narrative documentation              │
│ Files: recommendations/*, sections/*                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Generate PDF                                        │
│ Compile formal documentation using Metanorma                │
│ Input: water_gauge_profile.adoc                             │
│ Output: water_gauge_profile.pdf                             │
│ Also validates: OGC document structure, requirements format │
│ Command: docker run metanorma/metanorma ...                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Create API Specifications                           │
│ Build OpenAPI and AsyncAPI specs with OGC extensions        │
│ Files: openapi.yaml, asyncapi.yaml                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Validate                                            │
│ Test against implementation using schemathesis & custom     │
│ Commands: schemathesis, custom_amqp_test                    │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Requirements & Abstract Tests

Requirements and tests are the foundation of your profile. They define what implementations must do and how to verify conformance.

### Requirements Structure

Requirements are organized into:
- **Requirements Classes**: Groups of related requirements
- **Individual Requirements**: Specific testable statements

#### Creating a Requirements Class

File: `requirements/requirements_class_feature.adoc`

```asciidoc
[[rc_feature]]
[requirements_class]
====
[%metadata]
identifier:: http://www.opengis.net/spec/ogcapi-edr-3/1.0/req/profile/feature
subject:: Implementation
inherit:: {ogcapi-edr-1}
====
```

#### Creating Individual Requirements

File: `requirements/core/REQ_feature.adoc`

```asciidoc
[[req_feature]]
[requirement]
====
[%metadata]
identifier:: /req/profile/feature
part:: The service SHALL provide endpoint X
part:: The service SHALL return format Y
part:: The service SHALL support parameter Z
====
```

**Key Points:**
- Use `SHALL` for mandatory requirements
- Each requirement should be testable
- Break complex requirements into parts
- Use clear, unambiguous language

### Abstract Tests Structure

Tests verify that implementations meet requirements.

#### Creating a Test Class

File: `abstract_tests/ATS_class_feature.adoc`

```asciidoc
[[ats_feature]]
[conformance_class]
====
[%metadata]
identifier:: http://www.opengis.net/spec/ogcapi-edr-3/1.0/conf/profile/feature
subject:: Implementation
inherit:: {ogcapi-edr-1}
====
```

#### Creating Individual Tests

File: `abstract_tests/core/ATS_feature.adoc`

```asciidoc
[[ats_feature_test]]
[abstract_test]
====
[%metadata]
identifier:: /conf/profile/feature
target:: /req/profile/feature

[.component,class=test method]
--
1. Send GET request to endpoint X
2. Verify response status is 200
3. Verify response format is Y
4. Verify parameter Z is supported
--
====
```

**Key Points:**
- Each test targets a specific requirement
- Tests should be reproducible
- Include expected results
- Use numbered steps for clarity

### Example: Water Gauge Requirements

**Requirement:**
```asciidoc
[[req_asyncapi]]
[requirement]
====
[%metadata]
identifier:: /req/water-gauge-profile/asyncapi

part:: The service SHALL provide an AsyncAPI 3.0 specification
part:: The AsyncAPI SHALL define water gauge notification channels
part:: The service SHALL support AMQP protocol
====
```

**Test:**
```asciidoc
[[ats_asyncapi]]
[abstract_test]
====
[%metadata]
identifier:: /conf/water-gauge-profile/asyncapi
target:: /req/water-gauge-profile/asyncapi

[.component,class=test method]
--
1. Send GET request to /asyncapi.yaml
2. Verify response is valid AsyncAPI 3.0 document
3. Verify channels are defined for water gauge notifications
4. Verify AMQP server is configured
--
====
```

## Step 2: Recommendations & Sections

### Recommendations

Recommendations provide best practices using `SHOULD` statements.

File: `recommendations/core/REC_feature.adoc`

```asciidoc
[[rec_feature]]
[recommendation]
====
[%metadata]
identifier:: /rec/profile/feature

statement:: The service SHOULD cache responses for improved performance
statement:: The service SHOULD provide pagination for large result sets
====
```

### Sections

Sections contain narrative documentation that explains the profile.

#### Key Sections

**Conformance** (`sections/clause_2_conformance.adoc`):
```asciidoc
== Conformance

This profile defines the following conformance classes:

* Core
* AsyncAPI Support
* Subscription Schema
```

**Profile Description** (`sections/clause_7_water-gauge-profile.adoc`):
```asciidoc
== Water Gauge Profile

=== Overview
This profile extends OGC API - EDR for water gauge notifications...

=== Requirements
include::../requirements/requirements_class_core.adoc[]
include::../requirements/core/REQ_*.adoc[]

=== Abstract Tests
include::../abstract_tests/ATS_class_core.adoc[]
include::../abstract_tests/core/ATS_*.adoc[]
```

**Annexes** (`sections/annex-a.adoc`):
```asciidoc
[appendix]
== Abstract Test Suite

include::../abstract_tests/ATS_class_*.adoc[]
```

## Step 3: Generate PDF Documentation

Once requirements, tests, and sections are complete, generate formal documentation.

### Main Document

File: `water_gauge_profile.adoc`

```asciidoc
= OGC API - Environmental Data Retrieval - Part 3: Service Profiles
:doctype: standard
:encoding: utf-8
:lang: en
:status: draft
:committee: technical
:edition: 1.0
:docnumber: 24-XXX
:published-date: 2024-XX-XX

include::sections/clause_0_front_material.adoc[]
include::sections/clause_1_scope.adoc[]
include::sections/clause_2_conformance.adoc[]
include::sections/clause_3_references.adoc[]
include::sections/clause_4_terms_and_definitions.adoc[]
include::sections/clause_5_conventions.adoc[]
include::sections/clause_6_context.adoc[]
include::sections/clause_7_water-gauge-profile.adoc[]
include::sections/clause_8_media_types.adoc[]
include::sections/annex-a.adoc[]
include::sections/annex-bibliography.adoc[]
```

### Generate PDF with Docker

```bash
docker run --rm \
  -v "$(pwd)":/metanorma \
  -v ${HOME}/.fontist/fonts/:/config/fonts \
  metanorma/metanorma metanorma compile \
  --agree-to-terms -t ogc -x pdf water_gauge_profile.adoc
```

**Input:** `water_gauge_profile.adoc`
**Output:** `water_gauge_profile.pdf`

**What this does:**
- Mounts current directory to `/metanorma` in container
- Mounts font cache for consistent rendering
- Compiles AsciiDoc to OGC-formatted PDF
- Validates OGC document structure
- Validates requirements and test formatting
- Generates `water_gauge_profile.pdf`

### Using Makefile

Create `Makefile`:
```makefile
all: pdf

pdf:
	docker run --rm \
	  -v "$$(pwd)":/metanorma \
	  -v $${HOME}/.fontist/fonts/:/config/fonts \
	  metanorma/metanorma metanorma compile \
	  --agree-to-terms -t ogc -x pdf water_gauge_profile.adoc

clean:
	rm -f water_gauge_profile.pdf
```

Then simply run:
```bash
make
```

## Step 4: Create API Specifications

After documenting requirements, create machine-readable specifications.

### OpenAPI Specification

OpenAPI defines the HTTP REST API.

File: `openapi.yaml`

```yaml
openapi: 3.0.3
info:
  title: Water Gauge Profile API
  version: 1.0.0
  description: OGC API - EDR Water Gauge Profile

servers:
  - url: http://localhost:5000
    description: Development server

paths:
  /collections/water_gauge/items:
    get:
      summary: Query water gauge items
      parameters:
        - name: datetime
          in: query
          schema:
            type: string
        - name: bbox
          in: query
          schema:
            type: string
      responses:
        '200':
          description: GeoJSON FeatureCollection

  /collections/water_gauge/items/{featureId}:
    get:
      summary: Get specific water gauge observation
      parameters:
        - name: featureId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: GeoJSON Feature

components:
  schemas:
    WaterGaugeFeature:
      type: object
      properties:
        type:
          type: string
          const: Feature
        properties:
          type: object
          properties:
            station_id:
              type: string
            flood_stage:
              type: string
              enum: [action, minor, moderate, major]
            wfo:
              type: string
            value:
              type: number
            timestamp:
              type: string
              format: date-time
        x-ogc-edr-water-gauge-profile-pubsub:
          asyncapi: /asyncapi.yaml
          channel: water_gauge_notifications
```

**OGC Extensions:**
- `x-ogc-edr-water-gauge-profile-pubsub`: Links to AsyncAPI channel

**Optional: Subscription Management Endpoint**

If your implementation provides HTTP-based subscription management (e.g., for email notifications), you can add:

```yaml
paths:
  /api/subscribe:
    get:
      summary: Get subscription schema
      responses:
        '200':
          description: JSON Schema for subscriptions
          content:
            application/schema+json:
              schema:
                $ref: '#/components/schemas/SubscriptionRequest'
    post:
      summary: Create subscription
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SubscriptionRequest'
      responses:
        '201':
          description: Subscription created

components:
  schemas:
    SubscriptionRequest:
      type: object
      required:
        - email
      properties:
        email:
          type: string
          format: email
        flood_stages:
          type: array
          items:
            type: string
            enum: [action, minor, moderate, major]
```

This is implementation-specific and not required by the core profile.

### AsyncAPI Specification

AsyncAPI defines the PubSub messaging interface.

File: `asyncapi.yaml`

```yaml
asyncapi: 3.0.0
info:
  title: Water Gauge Profile AsyncAPI
  version: 1.0.0
  description: Real-time water gauge notifications

servers:
  production:
    host: localhost:5672
    protocol: amqp
    description: RabbitMQ broker

channels:
  water_gauge_notifications:
    address: collections/water_gauge/items/#
    description: Water gauge observation notifications
    x-ogc-subscription:
      filters:
        - name: flood_stages
          description: Filter by flood stage
          schema:
            type: array
            items:
              type: string
              enum:
                - value: action
                  title: Action Stage
                - value: minor
                  title: Minor Flooding
                - value: moderate
                  title: Moderate Flooding
                - value: major
                  title: Major Flooding
        - name: station_ids
          description: Filter by station ID
          schema:
            type: array
            items:
              type: string
        - name: wfo
          description: Filter by Weather Forecast Office
          schema:
            type: string
    messages:
      waterGaugeUpdate:
        $ref: '#/components/messages/WaterGaugeObservation'

operations:
  receiveWaterGaugeUpdate:
    action: receive
    channel:
      $ref: '#/channels/water_gauge_notifications'
    messages:
      - $ref: '#/channels/water_gauge_notifications/messages/waterGaugeUpdate'

components:
  messages:
    WaterGaugeObservation:
      payload:
        type: object
        required:
          - type
          - properties
        properties:
          type:
            type: string
            const: Feature
          properties:
            type: object
            required:
              - station_id
              - value
              - timestamp
            properties:
              station_id:
                type: string
              flood_stage:
                type: string
                enum: [action, minor, moderate, major]
              wfo:
                type: string
              value:
                type: number
              timestamp:
                type: string
                format: date-time
```

**OGC Extensions:**
- `x-ogc-subscription`: Defines available filters for subscriptions

**Optional: Link to HTTP Subscription API**

If your implementation provides HTTP-based subscription management, you can add:

```yaml
info:
  x-ogc-subscription-api: /api/subscribe
```

This links to an optional HTTP endpoint for managing subscriptions (e.g., email notifications). Not required by the core profile.

### Linking Specifications

The specifications link together:

```
OpenAPI (WaterGaugeFeature schema)
    ↓ x-ogc-edr-water-gauge-profile-pubsub
AsyncAPI (water_gauge_notifications)
```

This creates discoverability where:
1. Clients discover AsyncAPI from OpenAPI schema
2. Clients discover available filters from AsyncAPI

**Optional:** If using HTTP subscription management:
```
AsyncAPI (info)
    ↓ x-ogc-subscription-api
OpenAPI (/api/subscribe)
```

## Step 5: Validate Implementation

### Validate OpenAPI with Schemathesis

Schemathesis tests your API against the OpenAPI specification.

```bash
# Install
pip install schemathesis

# Run tests
schemathesis run -u http://localhost:5000 /path/to/openapi.yaml

# Exclude specific paths
schemathesis run \
  --exclude-path="/collections/cwa/items" \
  --exclude-path="/collections/states/items" \
  -u http://localhost:5400 \
  /path/to/openapi.yaml
```

**What it tests:**
- Response status codes match spec
- Response schemas match definitions
- Required parameters are enforced
- Data types are correct

### Validate AsyncAPI with Custom Tests

File: `custom_amqp_test/test_asyncapi_amqp.py`

```python
import pika
import json
import yaml
import sys

def test_asyncapi_amqp(asyncapi_file):
    # Load AsyncAPI spec
    with open(asyncapi_file) as f:
        spec = yaml.safe_load(f)
    
    # Extract connection details
    server = spec['servers']['production']
    host = server['host']
    
    # Extract channel address
    channels = spec['channels']
    channel_name = list(channels.keys())[0]
    channel_address = channels[channel_name]['address']
    
    # Connect to broker
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host.split(':')[0])
    )
    channel = connection.channel()
    
    # Verify channel exists
    exchange_name = channel_address.split('/#')[0] if '/#' in channel_address else channel_address
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='topic',
        passive=True  # Verify exists
    )
    
    # Get expected message schema
    message_schema = channels[channel_name]['messages']
    
    # Consume message
    def callback(ch, method, properties, body):
        message = json.loads(body)
        
        # Validate against schema
        assert message['type'] == 'Feature'
        assert 'properties' in message
        assert 'station_id' in message['properties']
        
        print("✓ Message valid")
        ch.stop_consuming()
    
    channel.basic_consume(
        queue='test_queue',
        on_message_callback=callback,
        auto_ack=True
    )
    
    print(f"Waiting for messages on {channel_address}...")
    channel.start_consuming()

if __name__ == '__main__':
    asyncapi_file = sys.argv[1] if len(sys.argv) > 1 else '../asyncapi.yaml'
    test_asyncapi_amqp(asyncapi_file)
```

Run:
```bash
./custom_amqp_test/test_asyncapi_amqp.py asyncapi.yaml
```

### Complete Validation Checklist

- [ ] **OpenAPI validation**: `schemathesis run -u http://localhost:5000 /path/to/openapi.yaml`
- [ ] **AsyncAPI validation**: `npx @asyncapi/cli validate asyncapi.yaml`
- [ ] **AMQP connectivity**: `./custom_amqp_test/test_asyncapi_amqp.py asyncapi.yaml`
- [ ] **Schema validation**: Verify data schemas are valid
- [ ] **Subscription creation**: Test PubSub client connections
- [ ] **Message filtering**: Verify filters work as specified
- [ ] **Requirements coverage**: All requirements have corresponding tests
- [ ] **PDF generation**: `make` produces valid PDF

## Best Practices

### Requirements Writing

1. **Be specific**: "SHALL return GeoJSON" not "SHALL return data"
2. **Be testable**: Each requirement should map to a test
3. **Use parts**: Break complex requirements into testable parts
4. **Reference standards**: Link to OGC/IETF specifications

### Test Writing

1. **One test per requirement**: Clear traceability
2. **Include setup**: Document prerequisites
3. **Define success**: Clear pass/fail criteria
4. **Be reproducible**: Anyone should get same results

### Specification Design

1. **Start simple**: Basic functionality first
2. **Use extensions**: Prefix with `x-ogc-`
3. **Link specs**: Use cross-references
4. **Provide examples**: Include sample requests/responses

### Documentation

1. **Write requirements first**: They drive everything else
2. **Keep sections focused**: One topic per section
3. **Use includes**: Modular, reusable content
4. **Generate often**: Catch errors early

## Examples

### Example 1: Adding a New Filter

**Requirement:**
```asciidoc
[[req_region_filter]]
[requirement]
====
[%metadata]
identifier:: /req/water-gauge-profile/region-filter

part:: The service SHALL support filtering by region
part:: Valid regions SHALL be: north, south, east, west
====
```

**Test:**
```asciidoc
[[ats_region_filter]]
[abstract_test]
====
[%metadata]
identifier:: /conf/water-gauge-profile/region-filter
target:: /req/water-gauge-profile/region-filter

[.component,class=test method]
--
1. Subscribe with region filter set to "north"
2. Publish message with region "north"
3. Verify notification received
4. Publish message with region "south"
5. Verify notification NOT received
--
====
```

**AsyncAPI:**
```yaml
x-ogc-subscription:
  filters:
    - name: region
      description: Geographic region
      schema:
        type: string
        enum:
          - value: north
            title: Northern Region
          - value: south
            title: Southern Region
          - value: east
            title: Eastern Region
          - value: west
            title: Western Region
```

**OpenAPI:**
```yaml
region:
  type: string
  enum: [north, south, east, west]
  x-ogc-edr-water-gauge-profile-email-subscription-ui:
    order: 4
    inputType: select
    label: Region
```

### Example 2: Adding a New Endpoint

**Requirement:**
```asciidoc
[[req_status_endpoint]]
[requirement]
====
[%metadata]
identifier:: /req/water-gauge-profile/status

part:: The service SHALL provide a /status endpoint
part:: The endpoint SHALL return current system status
part:: The response SHALL include broker connectivity
====
```

**Test:**
```asciidoc
[[ats_status_endpoint]]
[abstract_test]
====
[%metadata]
identifier:: /conf/water-gauge-profile/status
target:: /req/water-gauge-profile/status

[.component,class=test method]
--
1. Send GET request to /status
2. Verify response status is 200
3. Verify response includes "broker_connected" field
4. Verify field is boolean
--
====
```

**OpenAPI:**
```yaml
/status:
  get:
    summary: System status
    responses:
      '200':
        description: Status information
        content:
          application/json:
            schema:
              type: object
              properties:
                broker_connected:
                  type: boolean
                uptime:
                  type: number
```

## Summary

### The Complete Workflow

1. **Define requirements** in `requirements/`
2. **Write tests** in `abstract_tests/`
3. **Add recommendations** in `recommendations/`
4. **Write sections** in `sections/`
5. **Generate PDF** with Docker/Metanorma
6. **Create openapi.yaml** with OGC extensions
7. **Create asyncapi.yaml** with OGC extensions
8. **Validate with schemathesis** for OpenAPI
9. **Validate with custom tests** for AsyncAPI

### Key Principles

- **Requirements drive everything**: Start here
- **Tests verify requirements**: One-to-one mapping
- **Specifications implement requirements**: Machine-readable
- **Validation confirms conformance**: Automated testing

### Resources

- [Metanorma Documentation](https://www.metanorma.org/)
- [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/v3.0.0)
- [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3)
- [Schemathesis Documentation](https://schemathesis.readthedocs.io/)
- [OGC API - EDR](https://docs.ogc.org/is/19-086r5/19-086r5.html)

### Next Steps

1. Review existing water gauge profile as example
2. Define your use case and data model
3. Write requirements and tests
4. Generate documentation
5. Create specifications
6. Implement and validate

For quick reference, see [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
