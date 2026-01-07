#!/usr/bin/env python3
# =================================================================
#
# Authors: Shane Mill <shane.mill@example.com>
#
# Copyright (c) 2025 Shane Mill
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
OGC API - EDR Part 3 Profile Generator

Automates profile creation following PROFILE_CREATION_GUIDE.md recommendations.
"""

import os
import sys
import yaml
import json
from pathlib import Path
from templates import (
    get_main_adoc_template,
    get_section_templates,
    get_makefile_template,
    get_readme_template,
    get_test_script_template
)
from query_types import (
    QUERY_TYPE_REQUIREMENTS,
    QUERY_TYPE_TEST_STEPS,
    FORMAT_REQUIREMENTS
)


# ============================================================================
# USER INTERACTION
# ============================================================================

def prompt(message, default=None):
    """Prompt user for input with optional default."""
    if default:
        response = input(f"{message} [{default}]: ").strip()
        return response if response else default
    return input(f"{message}: ").strip()


def prompt_list(message, default=None):
    """Prompt for comma-separated list."""
    if default:
        response = input(f"{message} [{default}]: ").strip()
        response = response if response else default
    else:
        response = input(f"{message}: ").strip()
    return [item.strip() for item in response.split(',') if item.strip()]


# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================

def create_directory_structure(profile_name):
    """Create profile directory structure."""
    base = Path(profile_name)
    dirs = [
        base,
        base / "requirements" / "core",
        base / "abstract_tests" / "core",
        base / "recommendations" / "core",
        base / "sections",
        base / "examples",
        base / "custom_amqp_test",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    return base


# ============================================================================
# CONFIGURATION
# ============================================================================

def save_config(base, config):
    """Save profile configuration to YAML file."""
    config_file = base / "profile_config.yml"
    config_file.write_text(yaml.dump(config, sort_keys=False, default_flow_style=False))
    print(f"✓ Saved configuration to {config_file}")


def load_config(config_path):
    """Load profile configuration from YAML file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


# ============================================================================
# REQUIREMENT AND TEST GENERATION
# ============================================================================

def create_requirement(base, req_id, statement, parts):
    """Create requirement file."""
    anchor_id = f"req_{base.name}_{req_id}".replace('/', '_')
    content = f"""[[{anchor_id}]]
[requirement]
====
[%metadata]
identifier:: /req/{base.name}/{req_id}
statement:: {statement}
"""
    for part in parts:
        content += f"part:: {part}\n"
    content += "====\n"
    
    file_path = base / "requirements" / "core" / f"REQ_{req_id}.adoc"
    file_path.write_text(content)


def create_abstract_test(base, test_id, req_id, steps):
    """Create abstract test file."""
    anchor_id = f"ats_{base.name}_{test_id}".replace('/', '_')
    content = f"""[[{anchor_id}]]
[abstract_test]
====
[%metadata]
identifier:: /conf/{base.name}/{test_id}
target:: /req/{base.name}/{req_id}
test-purpose:: Validate that {test_id.replace('-', ' ')} requirement is correctly implemented.
test-method::
"""
    for step in steps:
        content += f"step:: {step}\n"
    content += "====\n"
    
    file_path = base / "abstract_tests" / "core" / f"ATS_{test_id}.adoc"
    file_path.write_text(content)


def create_requirements_class(base, class_name, requirements):
    """Create requirements class file."""
    anchor_id = f"req_class_{base.name}_{class_name}".replace('-', '_')
    content = f"""[[{anchor_id}]]
[requirements_class]
====
[%metadata]
identifier:: http://www.opengis.net/spec/ogcapi-edr-3/1.0/req/{base.name}
target-type:: {base.name.replace('_', ' ').title()} Profile Standard
"""
    for req in requirements:
        content += f"requirement:: /req/{base.name}/{req['id']}\n"
    content += "====\n"
    
    file_path = base / "requirements" / f"requirements_class_{class_name}.adoc"
    file_path.write_text(content)


def create_conformance_class(base, class_name, tests):
    """Create conformance class file."""
    anchor_id = f"ats_class-{base.name}_{class_name}".replace('-', '_').replace('_class_', '_class-')
    content = f"""[[{anchor_id}]]
[conformance_class]
====
[%metadata]
identifier:: http://www.opengis.net/spec/ogcapi-edr-3/1.0/conf/{base.name}
target:: http://www.opengis.net/spec/ogcapi-edr-3/1.0/req/{base.name}
"""
    for test in tests:
        content += f"abstract-test:: /conf/{base.name}/{test['id']}\n"
    content += "====\n"
    
    file_path = base / "abstract_tests" / f"ATS_class_{class_name}.adoc"
    file_path.write_text(content)



# ============================================================================
# OPENAPI GENERATION
# ============================================================================

def create_openapi(base, collections, properties, include_asyncapi=False):
    """Create OpenAPI specification."""
    paths = {}
    schemas = {}
    
    for coll in collections:
        collection_name = coll['name']
        query_types = coll['query_types']
        
        # Add collection metadata endpoint
        paths[f"/collections/{collection_name}"] = {
            "get": {
                "summary": f"Get {collection_name} metadata",
                "responses": {"200": {"description": "Collection metadata"}}
            }
        }
        
        # Add query type endpoints
        for qt in query_types:
            if qt == "items":
                paths[f"/collections/{collection_name}/items"] = {
                    "get": {
                        "summary": f"Query {collection_name} items",
                        "parameters": [
                            {"name": "datetime", "in": "query", "schema": {"type": "string"}},
                            {"name": "bbox", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {"200": {"description": "GeoJSON FeatureCollection"}}
                    }
                }
                paths[f"/collections/{collection_name}/items/{{featureId}}"] = {
                    "get": {
                        "summary": f"Get specific {collection_name} item",
                        "parameters": [
                            {"name": "featureId", "in": "path", "required": True, "schema": {"type": "string"}}
                        ],
                        "responses": {"200": {"description": "GeoJSON Feature"}}
                    }
                }
            elif qt == "locations":
                paths[f"/collections/{collection_name}/locations"] = {
                    "get": {
                        "summary": f"Get available locations for {collection_name}",
                        "responses": {"200": {"description": "GeoJSON FeatureCollection of available locations"}}
                    }
                }
                paths[f"/collections/{collection_name}/locations/{{locationId}}"] = {
                    "get": {
                        "summary": f"Query {collection_name} data by location",
                        "parameters": [
                            {"name": "locationId", "in": "path", "required": True, "schema": {"type": "string"}},
                            {"name": "datetime", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {"200": {"description": "Query results"}}
                    }
                }
            else:
                paths[f"/collections/{collection_name}/{qt}"] = {
                    "get": {
                        "summary": f"Query {collection_name} by {qt}",
                        "parameters": [
                            {"name": "coords", "in": "query", "required": True, "schema": {"type": "string"}},
                            {"name": "datetime", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {"200": {"description": "Query results"}}
                    }
                }
        
        # Build schema for this collection
        feature_schema = {
            "type": "object",
            "properties": {
                "type": {"type": "string", "const": "Feature"},
                "properties": {
                    "type": "object",
                    "properties": {prop: {"type": "string"} for prop in properties}
                }
            }
        }
        
        if include_asyncapi:
            feature_schema[f"x-ogc-edr-{base.name}-pubsub"] = {
                "asyncapi": "/asyncapi.yaml",
                "channel": f"{collection_name}_notifications"
            }
        
        schemas[f"{collection_name.title().replace('_', '')}Feature"] = feature_schema
    
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": f"{base.name.replace('_', ' ').title()} Profile API",
            "version": "1.0.0",
            "description": f"OGC API - EDR {base.name.replace('_', ' ').title()} Profile"
        },
        "servers": [{"url": "http://localhost:5000", "description": "Development server"}],
        "paths": paths,
        "components": {"schemas": schemas}
    }
    
    file_path = base / "openapi.yaml"
    file_path.write_text(yaml.dump(spec, sort_keys=False, default_flow_style=False))


# ============================================================================
# ASYNCAPI GENERATION
# ============================================================================

def create_asyncapi(base, collections, filters):
    """Create AsyncAPI specification."""
    channels = {}
    operations = {}
    messages = {}
    
    for coll in collections:
        collection_name = coll['name']
        channels[f"{collection_name}_notifications"] = {
            "address": f"collections/{collection_name}/items/#",
            "description": f"{collection_name.replace('_', ' ').title()} observation notifications",
            "x-ogc-subscription": {
                "filters": [
                    {
                        "name": f["name"],
                        "description": f["description"],
                        "schema": {"type": f["type"]}
                    } for f in filters
                ]
            },
            "messages": {
                f"{collection_name}Update": {
                    "$ref": f"#/components/messages/{collection_name.title().replace('_', '')}Observation"
                }
            }
        }
        
        operations[f"receive{collection_name.title().replace('_', '')}Update"] = {
            "action": "receive",
            "channel": {"$ref": f"#/channels/{collection_name}_notifications"},
            "messages": [
                {"$ref": f"#/channels/{collection_name}_notifications/messages/{collection_name}Update"}
            ]
        }
        
        messages[f"{collection_name.title().replace('_', '')}Observation"] = {
            "payload": {
                "type": "object",
                "required": ["type", "properties"],
                "properties": {
                    "type": {"type": "string", "const": "Feature"},
                    "properties": {
                        "type": "object",
                        "required": ["id", "timestamp"],
                        "properties": {
                            "id": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"}
                        }
                    }
                }
            }
        }
    
    spec = {
        "asyncapi": "3.0.0",
        "info": {
            "title": f"{base.name.replace('_', ' ').title()} Profile AsyncAPI",
            "version": "1.0.0",
            "description": f"Real-time notifications for {', '.join([c['name'] for c in collections])}"
        },
        "servers": {
            "production": {
                "host": "localhost:5672",
                "protocol": "amqp",
                "description": "RabbitMQ broker"
            }
        },
        "channels": channels,
        "operations": operations,
        "components": {"messages": messages}
    }
    
    file_path = base / "asyncapi.yaml"
    file_path.write_text(yaml.dump(spec, sort_keys=False, default_flow_style=False))



# ============================================================================
# DOCUMENTATION GENERATION
# ============================================================================

def create_main_adoc(base, profile_title):
    """Create main AsciiDoc file."""
    content = get_main_adoc_template(base.name, profile_title)
    file_path = base / f"{base.name}_profile.adoc"
    file_path.write_text(content)


def create_sections(base, profile_title, collections, requirements, tests):
    """Create section files."""
    # Build collections text
    collections_text = ""
    for coll in collections:
        collections_text += f"""==== {coll['name']}

Query types: {', '.join(coll['query_types'])}

Output formats: {', '.join(coll['formats'])}

"""
    
    # Build requirements text
    requirements_text = ""
    for req in requirements:
        requirements_text += f"include::../requirements/core/REQ_{req['id']}.adoc[]\n\n"
    
    # Get section templates
    sections = get_section_templates(base.name, profile_title, collections_text, requirements_text, tests)
    
    # Write section files
    for filename, content in sections.items():
        file_path = base / "sections" / filename
        file_path.write_text(content)


def create_supporting_files(base, profile_title, collections):
    """Create Makefile, README, metanorma.yml, and test script."""
    # Makefile
    makefile_content = get_makefile_template(f"{base.name}_profile")
    (base / "Makefile").write_text(makefile_content)
    
    # README
    readme_content = get_readme_template(profile_title, collections)
    (base / "README.md").write_text(readme_content)
    
    # metanorma.yml
    metanorma_content = """---
metanorma:
  deploy:
    email: "ci@metanorma.org"
"""
    (base / "metanorma.yml").write_text(metanorma_content)
    
    # Test script
    test_script_content = get_test_script_template()
    test_script_path = base / "custom_amqp_test" / "test_asyncapi_amqp.py"
    test_script_path.write_text(test_script_content)
    test_script_path.chmod(0o755)



# ============================================================================
# REQUIREMENT GENERATION LOGIC
# ============================================================================

def generate_query_type_requirement(collection_name, query_type):
    """Generate requirement for a specific query type."""
    template = QUERY_TYPE_REQUIREMENTS.get(query_type)
    if not template:
        return None
    
    req_id = f"data-query-{query_type}-{collection_name.replace('_', '-')}"
    statement = template["statement"].format(collection_name=collection_name)
    parts = [part.format(collection_name=collection_name) for part in template["parts"]]
    
    return {"id": req_id, "statement": statement, "parts": parts}


def generate_query_type_test(collection_name, query_type, req_id):
    """Generate test for a specific query type."""
    steps_template = QUERY_TYPE_TEST_STEPS.get(query_type, [
        f"Verify {query_type} query is implemented",
        "Test basic functionality",
        "Verify conformance"
    ])
    
    steps = [step.format(collection_name=collection_name) for step in steps_template]
    test_id = req_id  # Test ID matches requirement ID
    
    return {"id": test_id, "req_id": req_id, "steps": steps}


def generate_format_requirement(collection_name, formats):
    """Generate output format requirement for a collection."""
    format_parts = [f"Collection {collection_name} SHALL support the following formats:"]
    
    for fmt in formats:
        fmt_lower = fmt.lower()
        if fmt_lower in FORMAT_REQUIREMENTS:
            format_parts.extend(FORMAT_REQUIREMENTS[fmt_lower])
        else:
            format_parts.append(f"A format with the label {fmt_lower} SHALL be supported")
    
    return {
        "id": f"output-format-{collection_name.replace('_', '-')}",
        "statement": f"Output format support for {collection_name}",
        "parts": format_parts
    }


def generate_suggested_requirements(collections, include_asyncapi, filters):
    """Generate suggested requirements based on profile configuration."""
    requirements = [
        {
            "id": "openapi",
            "statement": "OpenAPI specification",
            "parts": [
                "The service SHALL provide an OpenAPI 3.0 specification",
                "The OpenAPI SHALL document all collection endpoints",
                "The OpenAPI SHALL include GeoJSON schemas"
            ]
        }
    ]
    
    # Add collection requirements
    for coll in collections:
        requirements.append({
            "id": f"collection-{coll['name'].replace('_', '-')}",
            "statement": f"{coll['name']} collection metadata",
            "parts": [
                f"The service SHALL provide a /collections/{coll['name']} endpoint",
                "The endpoint SHALL return collection metadata including extent and available query types",
                "The response SHALL conform to OGC API - EDR collection schema"
            ]
        })
    
    # Add query type requirements
    for coll in collections:
        for qt in coll['query_types']:
            req = generate_query_type_requirement(coll['name'], qt)
            if req:
                requirements.append(req)
    
    # Add format requirements
    for coll in collections:
        req = generate_format_requirement(coll['name'], coll['formats'])
        requirements.append(req)
    
    # Add AsyncAPI requirements
    if include_asyncapi:
        for coll in collections:
            requirements.append({
                "id": f"asyncapi-{coll['name'].replace('_', '-')}",
                "statement": f"AsyncAPI specification and PubSub messaging for {coll['name']}",
                "parts": [
                    "The service SHALL provide an AsyncAPI 3.0 specification",
                    f"The AsyncAPI SHALL define {coll['name']} notification channels",
                    "The service SHALL support AMQP protocol",
                    f"The service SHALL publish messages to collections/{coll['name']}/items/# channel",
                    "Messages SHALL conform to the AsyncAPI schema"
                ]
            })
    
    # Add filter requirements
    if filters:
        requirements.append({
            "id": "filters",
            "statement": "Filter support",
            "parts": [
                "The service SHALL support subscription filters",
                f"The service SHALL support filtering by {', '.join([f['name'] for f in filters])}",
                "Filters SHALL be defined in x-ogc-subscription extension"
            ]
        })
    
    return requirements


def generate_suggested_tests(requirements):
    """Generate suggested tests for requirements."""
    tests = []
    test_templates = {
        "openapi": [
            "Send GET request to /openapi",
            "Verify response is valid OpenAPI 3.0 document",
            "Verify all collection endpoints are documented",
            "Verify GeoJSON schemas are defined"
        ],
        "asyncapi": [
            "Send GET request to /asyncapi.yaml",
            "Verify response is valid AsyncAPI 3.0 document",
            "Verify channels are defined for notifications",
            "Verify AMQP server is configured",
            "Connect to AMQP broker",
            "Subscribe to notification channel",
            "Verify messages are received",
            "Verify messages conform to AsyncAPI schema"
        ],
        "filters": [
            "Verify x-ogc-subscription extension exists in AsyncAPI",
            "Verify all filters are documented",
            "Create subscription with filter",
            "Verify only matching messages are received"
        ]
    }
    
    for req in requirements:
        # Check if it's a query type requirement
        for qt in QUERY_TYPE_TEST_STEPS.keys():
            if f"data-query-{qt}-" in req['id']:
                collection_name = req['id'].split(f"data-query-{qt}-")[1].replace('-', '_')
                test = generate_query_type_test(collection_name, qt, req['id'])
                tests.append(test)
                break
        else:
            # Use template or default steps
            base_id = req['id'].split('-')[0] if '-' in req['id'] else req['id']
            steps = test_templates.get(base_id, [
                f"Verify requirement {req['id']} is implemented",
                "Test basic functionality",
                "Verify conformance"
            ])
            tests.append({"id": req['id'], "req_id": req['id'], "steps": steps})
    
    return tests



# ============================================================================
# INTERACTIVE CONFIGURATION
# ============================================================================

def get_interactive_config():
    """Get profile configuration interactively from user."""
    # Basic info
    profile_name = prompt("Profile name (e.g., water_gauge)", "my_profile")
    profile_title = prompt("Profile title", profile_name.replace('_', ' ').title())

    # Collections configuration
    num_collections = int(prompt("Number of collections", "1"))
    collections = []
    
    for i in range(num_collections):
        print(f"\n--- Collection {i+1} ---")
        coll_name = prompt("  Collection name", profile_name if i == 0 else f"{profile_name}_{i+1}")
        
        print("  Available query types: items, position, area, cube, trajectory, corridor, locations, instances")
        coll_query_types = prompt_list("  Query types (comma-separated)", "items")
        if not coll_query_types:
            coll_query_types = ["items"]
        
        print("  Common formats: GeoJSON, CoverageJSON, CSV, NetCDF, GRIB, Zarr")
        coll_formats = prompt_list("  Output formats (comma-separated)", "GeoJSON")
        if not coll_formats:
            coll_formats = ["GeoJSON"]
        
        collections.append({
            "name": coll_name,
            "query_types": coll_query_types,
            "formats": coll_formats
        })
    
    print()
    print("--- GeoJSON Feature Properties ---")
    has_items = any('items' in coll['query_types'] for coll in collections)
    if has_items:
        properties = prompt_list("GeoJSON Feature properties (comma-separated, e.g., station_id,value,timestamp)")
    else:
        properties = []
    
    print()
    print("--- PubSub Support (Optional) ---")
    print("Include AsyncAPI/PubSub? (OGC API - EDR Part 2)")
    include_asyncapi = prompt("Include AsyncAPI specification? (y/n)", "n").lower() == 'y'
    
    if include_asyncapi:
        print()
        print("--- Filters ---")
        num_filters = int(prompt("Number of filters", "0"))
        filters = []
        for i in range(num_filters):
            print(f"\nFilter {i+1}:")
            f_name = prompt("  Name")
            f_desc = prompt("  Description")
            f_type = prompt("  Type (string/array/number)", "string")
            filters.append({"name": f_name, "description": f_desc, "type": f_type})
    else:
        filters = []
    
    print()
    print("--- Requirements ---")
    print("\nSuggested requirements based on your profile:")
    print("  1. openapi - OpenAPI specification")
    print("  2. collection - Collection and query endpoints")
    if include_asyncapi:
        print("  3. asyncapi - AsyncAPI/PubSub specification (optional)")
    if filters:
        print(f"  {4 if include_asyncapi else 3}. filters - Filter support")
    print()
    use_suggested = prompt("Use suggested requirements? (y/n)", "y").lower() == 'y'
    
    if use_suggested:
        requirements = generate_suggested_requirements(collections, include_asyncapi, filters)
        print(f"✓ Using {len(requirements)} suggested requirements")
    else:
        num_reqs = int(prompt("Number of requirements", "2"))
        requirements = []
        for i in range(num_reqs):
            print(f"\nRequirement {i+1}:")
            req_id = prompt("  ID (e.g., asyncapi)")
            req_statement = prompt("  Statement")
            num_parts = int(prompt("  Number of parts", "2"))
            parts = [prompt(f"    Part {j+1}") for j in range(num_parts)]
            requirements.append({"id": req_id, "statement": req_statement, "parts": parts})
    
    print()
    print("--- Abstract Tests ---")
    print("\nSuggested tests will be generated for each requirement.")
    use_suggested_tests = prompt("Use suggested tests? (y/n)", "y").lower() == 'y'
    
    if use_suggested_tests:
        tests = generate_suggested_tests(requirements)
        print(f"✓ Using {len(tests)} suggested tests")
    else:
        tests = []
        for req in requirements:
            print(f"\nTest for requirement '{req['id']}':")
            test_id = req['id']
            num_steps = int(prompt("  Number of test steps", "3"))
            steps = [prompt(f"    Step {j+1}") for j in range(num_steps)]
            tests.append({"id": test_id, "req_id": req['id'], "steps": steps})
    
    return {
        'profile_name': profile_name,
        'profile_title': profile_title,
        'collections': collections,
        'properties': properties,
        'filters': filters,
        'include_asyncapi': include_asyncapi,
        'requirements': requirements,
        'tests': tests
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("OGC API - EDR Part 3 Profile Generator")
    print("=" * 60)
    print()
    
    # Check for existing config
    config_file = prompt("Load from config file? (path or 'n' for new)", "n")
    if config_file != "n" and Path(config_file).exists():
        print(f"Loading configuration from {config_file}...")
        config = load_config(config_file)
        print(f"✓ Loaded configuration for '{config['profile_title']}'")
        print("Regenerating all files from config...")
    else:
        config = get_interactive_config()
    
    profile_name = config['profile_name']
    profile_title = config['profile_title']
    collections = config['collections']
    properties = config['properties']
    filters = config['filters']
    include_asyncapi = config['include_asyncapi']
    requirements = config['requirements']
    tests = config['tests']
    
    print()
    print("=" * 60)
    print("Creating profile...")
    print("=" * 60)
    
    # Create structure
    base = create_directory_structure(profile_name)
    print(f"✓ Created directory structure: {base}")
    
    # Create requirements and tests
    for req in requirements:
        create_requirement(base, req['id'], req['statement'], req['parts'])
    print(f"✓ Created {len(requirements)} requirements")
    
    create_requirements_class(base, "core", requirements)
    
    for test in tests:
        create_abstract_test(base, test['id'], test['req_id'], test['steps'])
    print(f"✓ Created {len(tests)} abstract tests")
    
    create_conformance_class(base, "core", tests)
    
    # Create specifications
    create_openapi(base, collections, properties, include_asyncapi)
    print("✓ Created openapi.yaml")
    
    if include_asyncapi:
        create_asyncapi(base, collections, filters)
        print("✓ Created asyncapi.yaml")
    else:
        print("✓ Skipped asyncapi.yaml (not included)")
    
    # Create documentation
    create_main_adoc(base, profile_title)
    create_sections(base, profile_title, collections, requirements, tests)
    print("✓ Created documentation sections")
    
    # Create supporting files
    create_supporting_files(base, profile_title, collections)
    print("✓ Created Makefile, README, metanorma.yml, and test script")
    
    # Save configuration
    save_config(base, config)
    
    print()
    print("=" * 60)
    print(f"Profile created successfully: {base}")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"1. cd {base}")
    print("2. Review and edit generated files")
    print("3. make  # Generate PDF")
    print("4. Validate specifications")


if __name__ == "__main__":
    main()
