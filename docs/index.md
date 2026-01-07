# OGC API - EDR Profile Generator

Welcome to the OGC API - Environmental Data Retrieval (EDR) Part 3 Service Profile Generator!

## What is This?

This repository provides tools and documentation for creating **OGC API - EDR Part 3 Service Profiles** - formal specifications that define how to implement OGC APIs for specific use cases.

---

<div class="grid cards" markdown>

-   :rocket: __Quick Start__

    ---

    Get started in minutes with the automated profile generator.

    **Time:** 5-10 minutes  
    **Difficulty:** Easy

    [:octicons-arrow-right-24: Generator Guide](GENERATOR_GUIDE.md)

-   :books: __Documentation__

    ---

    Complete guides for creating profiles manually or with automation.

    - [Quick Reference](QUICK_REFERENCE.md)
    - [Manual Creation Guide](PROFILE_CREATION_GUIDE.md)

    [:octicons-arrow-right-24: Overview](README/)

-   :material-code-braces: __API Reference__

    ---

    Technical reference for the profile generator API.

    - Command-line options
    - Query type configurations
    - Template system

    [:octicons-arrow-right-24: API Docs](api-reference.md)

-   :material-file-document-multiple: __Examples__

    ---

    Real-world examples and use cases.

    - Water Gauge Profile
    - Aviation Weather
    - Marine Observations

    [:octicons-arrow-right-24: View Examples](examples.md)

</div>

---

## Features

- **Automated Profile Generator** - Create complete profiles in minutes
- **Comprehensive Documentation** - Step-by-step guides for manual and automated creation
- **Standards Compliant** - Generates Metanorma-compatible documentation
- **Query Type Support** - Items, Position, Area, Radius, Cube, Trajectory, Corridor, Locations, and Instances
- **Testing Support** - Includes abstract test suites and conformance classes

## Quick Start

## Installation

```bash
# Clone the repository
git clone https://github.com/ShaneMill1/OGC-Service-Profile-Creation.git
cd OGC-Service-Profile-Creation

# Install dependencies
pip install -r requirements.txt
```

### Generate Your First Profile

```bash
python src/create_profile.py \
  --name "my-profile" \
  --title "My EDR Profile" \
  --query-types items,position \
  --output ./my-profile
```

See the [Generator Guide](GENERATOR_GUIDE.md) for detailed usage.

## Documentation

- **[Getting Started](../overview/)** - Overview and introduction
- **[Quick Reference](QUICK_REFERENCE.md)** - Quick reference for common tasks
- **[Generator Guide](GENERATOR_GUIDE.md)** - Automated profile generation
- **[Manual Creation Guide](PROFILE_CREATION_GUIDE.md)** - Step-by-step manual creation

## Use Cases

### Water Gauge Profile Example

This generator was used to create the [Water Gauge Profile](https://edr-api-c.mdl.nws.noaa.gov/water_pygeoapi/), which demonstrates:

- Real-time water gauge observations
- PubSub messaging with AsyncAPI
- Email subscription capabilities
- Dynamic UI generation from OpenAPI

## What is an OGC API - EDR Profile?

An **OGC API - EDR Part 3 Service Profile** is a formal specification that:

1. **Defines a specific use case** - e.g., "Water Gauge Data Access"
2. **Specifies query types** - Which EDR query patterns to support
3. **Documents requirements** - What implementations must do
4. **Provides tests** - How to verify conformance
5. **Enables interoperability** - Standard way to access specific data types

## Repository Structure

```
ogc-edr-profile-generator/
├── src/                    # Profile generator code
│   ├── create_profile.py   # Main generator script
│   ├── templates.py        # Documentation templates
│   └── query_types.py      # Query type configurations
├── docs/                   # Documentation (this site)
├── examples/               # Example profiles
├── mkdocs.yml             # Documentation configuration
└── README.md              # Repository README
```

## Standards Compliance

This tool generates profiles that conform to:

- ✅ OGC API - EDR Part 1: Core
- ✅ OGC API - EDR Part 2: PubSub
- ✅ OGC API - EDR Part 3: Service Profiles (draft)
- ✅ Metanorma documentation format
- ✅ OpenAPI 3.0
- ✅ AsyncAPI 3.0

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Support

- **Issues**: [GitHub Issues](https://github.com/ShaneMill1/OGC-Service-Profile-Creation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ShaneMill1/OGC-Service-Profile-Creation/discussions)
- **Email**: shane.mill@noaa.gov

## Acknowledgments

Developed by NOAA/NWS/Meteorological Development Laboratory (MDL) to support OGC API standards adoption.
