# Testing and Validating OGC API Profiles

## Overview

This guide covers testing and validation approaches for OGC API - EDR Part 3 Service Profiles, focusing on automated testing with Schemathesis and manual validation techniques.

## Why Test Profiles?

Profile testing ensures:

- **Conformance** - Implementation matches specification
- **Interoperability** - Different clients can consume the API
- **Quality** - API behaves as documented
- **Regression Prevention** - Changes don't break existing functionality

## Testing Approaches

### 1. OpenAPI Validation with Schemathesis

**Schemathesis** is a property-based testing tool that automatically generates test cases from OpenAPI specifications.

#### Installation

```bash
pip install schemathesis
```

#### Basic Usage

```bash
# Test against OpenAPI spec
schemathesis run openapi.yaml --base-url https://your-api.example.com

# Test specific endpoints
schemathesis run openapi.yaml \
  --base-url https://your-api.example.com \
  --endpoint /collections/water_gauge/items

# Generate detailed report
schemathesis run openapi.yaml \
  --base-url https://your-api.example.com \
  --report report.html
```

#### Advanced Options

```bash
# Test with authentication
schemathesis run openapi.yaml \
  --base-url https://your-api.example.com \
  --header "Authorization: Bearer TOKEN"

# Limit request rate
schemathesis run openapi.yaml \
  --base-url https://your-api.example.com \
  --max-response-time 5000

# Test specific HTTP methods
schemathesis run openapi.yaml \
  --base-url https://your-api.example.com \
  --method GET --method POST
```

#### What Schemathesis Tests

- **Schema Compliance** - Responses match OpenAPI schema
- **Status Codes** - Correct HTTP status codes returned
- **Content Types** - Proper content-type headers
- **Required Fields** - All required fields present
- **Data Types** - Field types match specification
- **Constraints** - Min/max values, patterns, enums

### 2. AsyncAPI Validation

For profiles with PubSub messaging, validate AsyncAPI specifications.

#### Installation

```bash
npm install -g @asyncapi/cli
```

#### Validation

```bash
# Validate AsyncAPI spec
asyncapi validate asyncapi.yaml

# Generate documentation
asyncapi generate fromTemplate asyncapi.yaml @asyncapi/html-template -o ./asyncapi-docs
```

### 3. Manual Testing

#### Test Checklist

**Core Functionality:**
- [ ] Landing page returns valid JSON
- [ ] Collections endpoint lists all collections
- [ ] Items endpoint returns GeoJSON
- [ ] Query parameters work correctly
- [ ] Error responses include proper error messages

**Profile-Specific:**
- [ ] Required query types implemented
- [ ] Custom parameters work as specified
- [ ] Output formats match requirements
- [ ] Extensions properly documented

**Standards Compliance:**
- [ ] OGC API - Common conformance
- [ ] OGC API - EDR conformance
- [ ] Profile-specific conformance classes

#### Manual Test Examples

```bash
# Test landing page
curl https://your-api.example.com/

# Test collections
curl https://your-api.example.com/collections

# Test items query
curl https://your-api.example.com/collections/water_gauge/items

# Test with parameters
curl "https://your-api.example.com/collections/water_gauge/items?limit=10&bbox=-180,-90,180,90"

# Test error handling
curl https://your-api.example.com/collections/invalid
```

## Profile-Specific Testing

### Testing Generated Profiles

After generating a profile with `create_profile.py`:

1. **Build Documentation**
   ```bash
   cd output/my-profile
   make
   ```

2. **Validate OpenAPI**
   ```bash
   schemathesis run openapi.yaml --base-url http://localhost:5000
   ```

3. **Check Requirements**
   - Review generated requirements in `requirements/`
   - Verify abstract tests in `abstract_tests/`
   - Ensure conformance classes are complete

### Custom Test Scripts

Create profile-specific test scripts:

```python
# test_profile.py
import requests

BASE_URL = "https://your-api.example.com"

def test_items_endpoint():
    """Test items query returns GeoJSON"""
    response = requests.get(f"{BASE_URL}/collections/water_gauge/items")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert "features" in data

def test_custom_parameter():
    """Test profile-specific parameter"""
    response = requests.get(
        f"{BASE_URL}/collections/water_gauge/items",
        params={"flood_stage": "major"}
    )
    assert response.status_code == 200
    # Verify filtering worked
    data = response.json()
    for feature in data["features"]:
        assert feature["properties"]["flood_stage"] == "major"

if __name__ == "__main__":
    test_items_endpoint()
    test_custom_parameter()
    print("All tests passed!")
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test Profile

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install schemathesis
      
      - name: Run Schemathesis tests
        run: |
          schemathesis run openapi.yaml \
            --base-url ${{ secrets.API_BASE_URL }} \
            --report report.html
      
      - name: Upload test report
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: report.html
```

## Best Practices

### 1. Test Early and Often

- Test during development, not just at the end
- Run tests on every commit
- Automate testing in CI/CD pipeline

### 2. Test Multiple Scenarios

- Valid requests
- Invalid requests (error handling)
- Edge cases (empty results, large datasets)
- Different query parameters
- Various output formats

### 3. Document Test Results

- Keep test reports
- Track conformance over time
- Document known issues

### 4. Version Your Tests

- Keep tests in version control
- Update tests when spec changes
- Tag tests with profile version

## Troubleshooting

### Common Issues

**Schemathesis fails with schema errors:**
- Verify OpenAPI spec is valid: `openapi-spec-validator openapi.yaml`
- Check for missing required fields
- Ensure examples match schema

**Tests timeout:**
- Increase `--max-response-time`
- Check API performance
- Reduce test scope with `--endpoint`

**False positives:**
- Review OpenAPI spec for accuracy
- Add examples to clarify expected behavior
- Use `--hypothesis-max-examples` to adjust test generation

## Resources

- [Schemathesis Documentation](https://schemathesis.readthedocs.io/)
- [AsyncAPI CLI](https://www.asyncapi.com/tools/cli)
- [OGC API Testing Guide](https://docs.ogc.org/DRAFTS/20-009.html)
- [OpenAPI Validator](https://github.com/p1c2u/openapi-spec-validator)

## Next Steps

1. **Install Schemathesis**: `pip install schemathesis`
2. **Run basic tests**: `schemathesis run openapi.yaml --base-url YOUR_URL`
3. **Review results**: Check for failures and fix issues
4. **Automate**: Add tests to CI/CD pipeline
5. **Expand coverage**: Add custom tests for profile-specific features
