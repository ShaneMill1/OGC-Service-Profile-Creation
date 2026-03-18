# CHANGELOG - OGC API - EDR Part 3 Compliance

## [Unreleased] - 2025-01-30

### Added - OGC API - EDR Part 3 Compliance

#### New Models (`src/ogc_edr_profile/models.py`)
- `ExtentRequirements`: Profile-level extent restrictions with CRS/TRS/VRS validation
- `OutputFormat`: Output format definitions with schema references

#### New ServiceProfile Fields
- `required_conformance_classes`: Conformance classes implementations must declare (defaults to EDR Core)
- `extent_requirements`: Profile-level extent restrictions
- `output_formats`: Profile-level output format definitions with schema references
- `collection_id_pattern`: Regex pattern for valid collection IDs

#### New Validators
- `validate_parameter_completeness()`: Ensures all parameters have `unit` and `observedProperty` (per REQ_parameter-names)
- `validate_pubsub_conformance()`: Auto-adds Part 2 requirement when pubsub is present (per REQ_pubsub)

### Changed

#### OpenAPI Generation (`src/ogc_edr_profile/generate.py`)
- **BREAKING**: `servers` array now always empty (per REQ_publishing) - profile OpenAPI is implementation-independent
- Landing page response schema now requires `profile` link relation (per REQ_publishing)
- Conformance endpoint response schema now specifies required conformance classes (per REQ_api)
- Added `_landing_page_schema()` function
- Added `_R200_CONFORMANCE` response schema
- Updated `_core_paths()` to accept profile parameter

#### Documentation (`README.md`)
- Added "OGC API - EDR Part 3 Compliance" section
- Documented new configuration fields
- Updated `server_url` description (now for documentation only)
- Added compliance matrix

### Migration Guide

#### For Profile Authors

1. **Add units to all parameters** (now required):
   ```yaml
   parameter_names:
     temp:
       observedProperty:
         label: Temperature
       unit:              # REQUIRED
         label: Celsius
         symbol: C
   ```

2. **Remove manual Part 2 requirements** (auto-added when `pubsub` present)

3. **Regenerate OpenAPI documents**:
   ```bash
   ogc-edr-profile generate --config my_profile.yaml --output ./output
   ```

#### For Implementation Developers

1. **Add profile link to landing page**:
   ```json
   {
     "links": [
       {
         "href": "http://www.opengis.net/spec/ogcapi-edr-3/1.0/req/my_profile",
         "rel": "profile"
       }
     ]
   }
   ```

2. **Declare all required conformance classes** at `/conformance`

### Compliance Matrix

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| REQ_modspec | ✅ | AsciiDoc structure follows ModSpec |
| REQ_edr-conformant | ✅ | Uses edr-pydantic for authoritative EDR models |
| REQ_parameter-names | ✅ | Validator ensures unit, observedProperty specified |
| REQ_root | ✅ | Landing page schema requires profile link |
| REQ_publishing | ✅ | OpenAPI servers empty, profile link required |
| REQ_api | ✅ | Conformance endpoint specifies required classes |
| REQ_extent | ✅ | ExtentRequirements model with CRS/TRS/VRS rules |
| REQ_output-format | ✅ | OutputFormat model with schema references |
| REQ_pubsub | ✅ | Auto-adds Part 2 requirement, AsyncAPI generated |
| REQ_collectionid | ✅ | collection_id_pattern field for restrictions |

### Testing

All tests passing:
- ✅ Model validation
- ✅ OpenAPI generation (servers empty, profile link present)
- ✅ Parameter validation (catches missing units)
- ✅ PubSub auto-requirement

### References

- OGC API - EDR Part 1: Core (19-086r6)
- OGC API - EDR Part 3: Service Profiles (draft)
- Redmine ticket: `/tmp/ogc-edr-profile-alignment-issues.textile`
