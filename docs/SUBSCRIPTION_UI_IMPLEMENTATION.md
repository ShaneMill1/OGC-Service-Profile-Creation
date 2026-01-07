# Building Email Subscription UIs from Service Profile OpenAPI Specifications

## Overview

This document explains how to develop dynamic user interfaces by consuming OpenAPI specification extensions defined in an OGC API Service Profile. The Water Gauge Service Profile demonstrates this approach with an email subscription form that automatically generates from the Service Profile's `openapi.yaml` schema.

**Audience**: Developers implementing Service Profile-compliant UIs

**Key Concept**: Instead of hardcoding HTML forms, read the Service Profile's OpenAPI schema at runtime and generate UI elements from Service Profile-specific specification metadata.

## What Users See

The Water Gauge Profile provides an email subscription form at `/subscribe` that allows users to:

1. **Enter their email address** to receive notifications
2. **Select flood stages** to monitor (Below Action, Action, Minor, Moderate, Major)
3. **Filter by station IDs** (optional, comma-separated like "STATION1,STATION2")
4. **Filter by Weather Forecast Office** (optional, comma-separated like "PHI,AKQ,OKX")

The form validates input, provides helpful descriptions for each flood stage, and submits subscriptions to the API.

## Why It's Dynamic

Unlike traditional web forms with hardcoded HTML fields, this subscription form is **generated automatically** from the Service Profile's OpenAPI specification. This means:

- **No manual HTML updates**: Add a new field to the Service Profile spec, the form updates automatically
- **Always in sync**: The form always matches the current Service Profile capabilities
- **Self-documenting**: The same specification drives the UI, validation, and API documentation

## How It Works

### Step 1: Specification Extensions

The OpenAPI specification (`openapi.yaml`) defines the subscription schema with special UI extensions:

```yaml
subscriptionRequest:
  type: object
  required:
    - email
    - flood_stages
  properties:
    email:
      type: string
      format: email
      title: Email Address
      description: Email address for receiving notifications
      x-ogc-edr-water-gauge-profile-email-subscription-ui:
        order: 1
        inputType: email
    
    flood_stages:
      type: array
      title: Flood Stages
      description: Alert for selected flood stages
      minItems: 1
      items:
        type: string
        enum:
          - below_action
          - action
          - minor
          - moderate
          - major
      x-ogc-edr-water-gauge-profile-email-subscription-ui:
        order: 2
        inputType: checkbox-group
        labels:
          below_action: Below Action
          action: Action
          minor: Minor
          moderate: Moderate
          major: Major
        descriptions:
          below_action: Water level is below action stage
          action: Minor flooding begins at some locations
          minor: Minimal or no property damage, but some public threat
          moderate: Some inundation of structures and roads near streams
          major: Extensive inundation of structures and roads
    
    stations:
      type: string
      title: Station IDs
      description: Comma-separated station IDs or leave blank for all stations
      default: all
      pattern: '^([A-Z0-9]+,)*[A-Z0-9]+$|^all$|^$'
      x-ogc-edr-water-gauge-profile-email-subscription-ui:
        order: 3
        inputType: text
        placeholder: "e.g., STATION1,STATION2 or leave blank"
    
    wfo:
      type: string
      title: Weather Forecast Office
      description: Comma-separated WFO codes (e.g., PHI, AKQ, OKX)
      pattern: '^([A-Z]{3},)*[A-Z]{3}$|^$'
      x-ogc-edr-water-gauge-profile-email-subscription-ui:
        order: 4
        inputType: text
        placeholder: "e.g., PHI, AKQ, OKX (comma-separated)"
  
  x-ogc-edr-water-gauge-profile-pubsub:
    asyncapi: /static/profiles/water-gauge-profile/asyncapi.yaml
    channel: notify-collections-water-gauge
```

### Step 2: UI Extension Properties

The `x-ogc-edr-water-gauge-profile-email-subscription-ui` extension tells the form generator:

- **order**: Which position the field appears in (1, 2, 3, 4)
- **inputType**: What HTML input to render (`email`, `text`, `checkbox-group`)
- **labels**: Human-readable labels for enum values (for checkboxes)
- **descriptions**: Explanatory text for each option
- **placeholder**: Hint text shown in text inputs

### Step 3: Dynamic Form Generation

The subscription page (`subscriptions.html`) uses JavaScript to:

1. **Fetch the schema**: `GET /api/subscribe?f=json` returns the full JSON Schema
2. **Parse UI extensions**: Extract `x-ogc-edr-water-gauge-profile-email-subscription-ui` metadata from each field
3. **Sort by order**: Arrange fields according to the `order` property
4. **Render inputs**: Create appropriate HTML elements based on `inputType`:
   - `email` → `<input type="email">`
   - `text` → `<input type="text">`
   - `checkbox-group` → Multiple `<input type="checkbox">` with labels/descriptions
5. **Apply validation**: Use JSON Schema `pattern`, `minItems`, `required` for client-side validation
6. **Submit**: POST validated data to `/api/subscribe`

**Key Features**:
- Zero hardcoded form fields
- Automatic field ordering via `order` property
- Type-specific rendering based on `inputType`
- Placeholder text support for input guidance
- Client-side validation from JSON Schema
- Graceful fallbacks for missing UI metadata

## Specification Standards

This implementation follows OGC API best practices for machine-readable specifications:

### OpenAPI Extensions

- **Extension naming**: Uses `x-ogc-edr-water-gauge-profile-*` prefix for profile-specific properties
- **JSON Schema**: Standard validation (OGC approved)
- **REST principles**: GET for schema retrieval, POST for subscription creation
- **Content negotiation**: Supports `application/schema+json`

### AsyncAPI Integration

The schema includes a link to the AsyncAPI specification:

```yaml
x-ogc-edr-water-gauge-profile-pubsub:
  asyncapi: /static/profiles/water-gauge-profile/asyncapi.yaml
  channel: notify-collections-water-gauge
```

This connects the HTTP subscription API to the message broker channel, enabling:
- Discovery of PubSub capabilities
- Message format documentation
- Channel routing information

## Benefits

### For End Users:
- **Always current**: Form reflects latest API capabilities
- **Clear guidance**: Descriptions and placeholders explain each field
- **Validation feedback**: Immediate error messages for invalid input

### For Service Profile Authors:
- **Single source of truth**: Update OpenAPI, UI updates automatically
- **No HTML maintenance**: Add fields without touching UI code
- **Consistency**: Same schema drives UI, validation, and documentation

### For API Consumers:
- **Self-documenting**: Machine-readable subscription capabilities
- **Interoperability**: Standard JSON Schema enables tool integration
- **Discoverability**: GET endpoint reveals available filters

### For Developers:
- **Maintainability**: Change schema, not HTML
- **Extensibility**: Add fields without UI code changes
- **Testing**: Schema-driven validation

## Practical Guide

### Adding a New Subscription Field

1. **Edit openapi.yaml** - Add to `subscriptionRequest.properties`:
   ```yaml
   severity_threshold:
     type: string
     title: "Severity Threshold"
     description: "Minimum severity level for alerts"
     enum:
       - low
       - medium
       - high
     x-ogc-edr-water-gauge-profile-email-subscription-ui:
       order: 5
       inputType: select
       labels:
         low: Low
         medium: Medium
         high: High
   ```

2. **UI automatically updates** on next page load - no HTML changes needed

### Adding Flood Stage Values

1. Update `flood_stages.items.enum` in openapi.yaml:
   ```yaml
   enum:
     - below_action
     - action
     - minor
     - moderate
     - major
     - record  # New value
   ```

2. Add label and description:
   ```yaml
   labels:
     record: Record
   descriptions:
     record: Water level approaching or exceeding historical records
   ```

3. Form renders new checkbox automatically

### Changing Field Order

Simply update the `order` values in the UI extensions:
```yaml
email:
  x-ogc-edr-water-gauge-profile-email-subscription-ui:
    order: 1  # Change to reorder
```

## Testing

1. **Verify schema endpoint**: `GET /api/subscribe?f=json`
2. **Check form rendering**: Visit `/subscribe` and verify all fields appear
3. **Test validation**: Submit invalid data, confirm error messages
4. **Test submission**: `POST /api/subscribe` with valid data
5. **Verify AsyncAPI**: Confirm message flow documented correctly

## Files

- `openapi.yaml`: Subscription schema with UI extensions
- `asyncapi.yaml`: PubSub channel and message definitions
- `subscriptions.html`: Dynamic form generator (JavaScript)
- `flask_app.py`: API endpoints for schema retrieval and subscription creation
