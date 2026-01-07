# OGC API - EDR Profile Generator

Tools and documentation for creating OGC API - Environmental Data Retrieval (EDR) Part 3 Service Profiles.

## Overview

This repository provides an automated tool for generating OGC API - EDR Part 3 Service Profiles, which are formal specifications that define how to implement EDR APIs for specific use cases.

## Features

- **Automated Generation** - Create complete profiles with a single command
- **Multiple Query Types** - Support for Items, Position, Area, Radius, Cube, Trajectory, Corridor, Locations, and Instances
- **Standards Compliant** - Generates Metanorma-compatible documentation
- **Abstract Tests** - Includes conformance classes and test suites
- **Comprehensive Documentation** - Step-by-step guides and examples

## Quick Start

### Installation

```bash
git clone https://github.com/ShaneMill1/OGC-Service-Profile-Creation.git
cd ogc-edr-profile-generator
pip install -r requirements.txt
```

### Generate a Profile

```bash
python src/create_profile.py \
  --name "my-profile" \
  --title "My EDR Profile" \
  --query-types items,position \
  --output ./my-profile
```

## Documentation

Full documentation is available at: **https://ShaneMill1.github.io/ogc-edr-profile-generator/**

Or build locally:

```bash
mkdocs serve
```

Then visit http://localhost:8000

## Repository Structure

```
ogc-edr-profile-generator/
├── src/                    # Profile generator source code
│   ├── create_profile.py   # Main generator script
│   ├── templates.py        # Documentation templates
│   └── query_types.py      # Query type configurations
├── docs/                   # MkDocs documentation
├── examples/               # Example profiles
├── mkdocs.yml             # Documentation configuration
└── requirements.txt       # Python dependencies
```

## Example: Water Gauge Profile

This tool was used to create the [Water Gauge Profile](https://edr-api-c.mdl.nws.noaa.gov/water_pygeoapi/), which demonstrates:

- Real-time water gauge observations
- PubSub messaging with AsyncAPI
- Email subscription capabilities
- Dynamic UI generation from OpenAPI

## Standards

Generates profiles conforming to:

- OGC API - EDR Part 1: Core
- OGC API - EDR Part 2: PubSub
- OGC API - EDR Part 3: Service Profiles (draft)
- Metanorma documentation format
- OpenAPI 3.0 / AsyncAPI 3.0

## Contributing

Contributions welcome! Please open an issue or pull request.

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Contact

- **Author**: Shane Mill (NOAA/NWS/MDL)
- **Email**: shane.mill@noaa.gov
- **Issues**: https://github.com/ShaneMill1/OGC-Service-Profile-Creation/issues

## Acknowledgments

Developed by NOAA/NWS/Meteorological Development Laboratory (MDL) to support OGC API standards adoption.

