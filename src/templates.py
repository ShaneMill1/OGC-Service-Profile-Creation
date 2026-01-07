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
Template strings for OGC API - EDR Part 3 Profile Generator
"""


def get_main_adoc_template(base_name, profile_title):
    """Main AsciiDoc document template."""
    return f"""= OGC API-Environmental Data Retrieval - Part 3: {profile_title}
:doctype: best-practice
:encoding: utf-8
:lang: en
:status: published
:committee: technical
:draft: 1.0
:external-id: http://www.opengis.net/doc/spec/ogcapi-edr-3/1.0
:received-date: 
:issued-date: 
:published-date: 
:fullname: Editor Name (Organization)
:docsubtype: general
:keywords: ogcdoc, OGC document, API, openapi, html, profile, {profile_title.lower()}
:submitting-organizations: Organization Name
:mn-document-class: ogc
:mn-output-extensions: xml,html,doc,pdf
:local-cache-only:
:data-uri-image:
:html-uri: ./{base_name}_profile.html
:pdf-uri: ./{base_name}_profile.pdf
:xml-uri: ./{base_name}_profile.xml
:doc-uri: ./{base_name}_profile.doc
:edition: 1.0

include::sections/clause_0_front_material.adoc[]

include::sections/clause_1_scope.adoc[]

include::sections/clause_2_conformance.adoc[]

include::sections/clause_3_references.adoc[]

include::sections/clause_4_terms_and_definitions.adoc[]

include::sections/clause_5_conventions.adoc[]

include::sections/clause_6_context.adoc[]

include::sections/clause_7_{base_name}.adoc[]

include::sections/annex-a.adoc[]

include::sections/annex-history.adoc[]

include::sections/annex-bibliography.adoc[]
"""


def get_section_templates(base_name, profile_title, collections_text, requirements_text, tests):
    """Get all section templates."""
    test_includes = '\n'.join([f'include::../abstract_tests/core/ATS_{test["id"]}.adoc[]' for test in tests])
    
    return {
        "clause_0_front_material.adoc": f""".Preface

Attention is drawn to the possibility that some of the elements of this document may be the subject of patent rights. The Open Geospatial Consortium shall not be held responsible for identifying any or all such patent rights.

Recipients of this document are requested to submit, with their comments, notification of any relevant patent claims or other intellectual property rights of which they may be aware that might be infringed by any implementation of the standard set forth in this document, and to provide supporting documentation.

[abstract]
== Abstract

The aim of the {profile_title} service profile is to provide a standard interface for accessing {profile_title.lower()} data based on OGC API-EDR standard.

== Preface

[NOTE]
Attention is drawn to the possibility that some of the elements of this document may be the subject of patent rights. The Open Geospatial Consortium shall not be held responsible for identifying any or all such patent rights.

Recipients of this document are requested to submit, with their comments, notification of any relevant patent claims or other intellectual property rights of which they may be aware that might be infringed by any implementation of the standard set forth in this document, and to provide supporting documentation.

== Security considerations

No security considerations have been made for this Service Profile.

== Submitters

All questions regarding this submission should be directed to the editor or the submitters:

.Submitters
|===
|*Editor Name* |*Organization Name*
|===

== Contributors

Additional contributors to this Profile include the following:

Individual name(s), Organization
""",
        "clause_1_scope.adoc": f"""== Scope

This profile extends OGC API - Environmental Data Retrieval (EDR) Part 1 for {profile_title.lower()} applications.

The profile defines:

* Collection structure for {profile_title.lower()} data
* Query patterns and parameters
* Response formats and schemas
""",
        "clause_2_conformance.adoc": f"""== Conformance

Conformance to the {profile_title} (this document) can be tested by inspection. The test suite is provided in <<annex-a>>.

This Standard contains normative language and thus places requirements on conformance, or mechanism for adoption, of candidate standards to which this Standard applies. In particular:

* <<core-section,OGC API-EDR Requirements Class: Core>> specifies the core requirements which shall be met by all standards claiming conformance to this Standard.
""",
        "clause_3_references.adoc": """[bibliography]
== Normative References

The following normative documents contain provisions that, through reference in this text, constitute provisions of this document.

* [[[ogc19-086,OGC 19-086r6]]], OGC API - Environmental Data Retrieval Standard - Part 1: Core
""",
        "clause_4_terms_and_definitions.adoc": """== Terms and Definitions

For the purposes of this document, the terms and definitions given in OGC API - EDR Part 1 apply.
""",
        "clause_5_conventions.adoc": """== Conventions

This document uses the standard conventions defined in OGC API - Common.

=== Identifiers

The normative provisions in this standard are denoted by the URI:

`http://www.opengis.net/spec/ogcapi-edr-3/1.0`
""",
        "clause_6_context.adoc": f"""== Context

=== Overview

This profile addresses {profile_title.lower()} use cases requiring standardized access to environmental data.
""",
        f"clause_7_{base_name}.adoc": f"""[[core-section]]
== {profile_title}

include::../requirements/requirements_class_core.adoc[]

=== Overview

This profile extends OGC API - EDR Part 1 to support {profile_title.lower()} data access patterns.

=== Collections

This profile defines the following collections:

{collections_text}
=== Requirements

{requirements_text}
=== Platform Resources

OGC API — Common defines a set of common capabilities which are applicable to any OGC Web API.

.Platform Resource Paths
[width="100%",options="header,footer"]
|====================
|PATH TEMPLATE |METHOD |RESOURCE
|{{{{root}}}}/ |GET |Landing page
|{{{{root}}}}/api |GET |API Description
|{{{{root}}}}/conformance |GET |Conformance Classes
|====================

=== General Requirements

==== HTTP Status Codes

HTTP response status codes SHALL conform to OGC API - Common standards.

==== Links

Response links SHALL conform to OGC API - Common standards.
""",
        "annex-a.adoc": f"""[[annex-A]]
[appendix]
== Conformance Class Abstract Test Suite (Normative)

=== Conformance Class Core

include::../abstract_tests/ATS_class_core.adoc[]

{test_includes}
""",
        "annex-history.adoc": """[appendix]
== Revision History

.Revision History
[width="90%",options="header"]
|===
|Date |Release |Editor | Primary clauses modified |Description
|2024-XX-XX |0.1 |Editor Name |all |initial version
|===
""",
        "annex-bibliography.adoc": """[bibliography]
== Bibliography

* [[[asyncapi,AsyncAPI]]], AsyncAPI Specification. https://www.asyncapi.com/
* [[[ogc-edr,OGC EDR]]], OGC API - EDR. https://ogcapi.ogc.org/edr/
"""
    }


def get_makefile_template(profile_name):
    """Makefile template."""
    return f"""all: pdf

pdf:
\tdocker run --rm \\
\t  -v "$$(pwd)":/metanorma \\
\t  -v ${{HOME}}/.fontist/fonts/:/config/fonts \\
\t  metanorma/metanorma metanorma compile \\
\t  --agree-to-terms -t ogc -x pdf,html,doc {profile_name}.adoc

clean:
\trm -f {profile_name}.pdf {profile_name}.html {profile_name}.doc {profile_name}.xml

.PHONY: all pdf clean
"""


def get_readme_template(profile_title, collections):
    """README template."""
    collections_list = "\n".join([
        f"- **{c['name']}**: `/collections/{c['name']}/items` (Query types: {', '.join(c['query_types'])}, Formats: {', '.join(c['formats'])})"
        for c in collections
    ])
    return f"""# {profile_title}

OGC API - EDR Part 3 Service Profile

## Structure

- `requirements/` - Requirements definitions
- `abstract_tests/` - Test specifications
- `sections/` - Documentation sections
- `openapi.yaml` - HTTP API specification
- `asyncapi.yaml` - PubSub specification
- `custom_amqp_test/` - Validation scripts

## Generate PDF

```bash
make
```

## Validate

```bash
# OpenAPI
schemathesis run -u http://localhost:5000 openapi.yaml

# AsyncAPI
./custom_amqp_test/test_asyncapi_amqp.py asyncapi.yaml
```

## Collections

{collections_list}
"""


def get_test_script_template():
    """AMQP test script template."""
    return """#!/usr/bin/env python3
import pika
import json
import yaml
import sys

def test_asyncapi_amqp(asyncapi_file):
    with open(asyncapi_file) as f:
        spec = yaml.safe_load(f)
    
    server = spec['servers']['production']
    host = server['host'].split(':')[0]
    
    channels = spec['channels']
    channel_name = list(channels.keys())[0]
    channel_address = channels[channel_name]['address']
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    
    exchange_name = channel_address.split('/#')[0] if '/#' in channel_address else channel_address
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic', passive=True)
    
    print(f"✓ Channel {channel_address} exists")
    connection.close()

if __name__ == '__main__':
    asyncapi_file = sys.argv[1] if len(sys.argv) > 1 else '../asyncapi.yaml'
    test_asyncapi_amqp(asyncapi_file)
"""
