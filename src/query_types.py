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
Query type configurations for OGC API - EDR Part 3 Profile Generator
"""

# Query type requirement templates
QUERY_TYPE_REQUIREMENTS = {
    "items": {
        "statement": "{collection_name} items query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/items endpoint",
            "The Items query SHALL return GeoJSON FeatureCollection formatted data",
            "The Items query SHALL support GET method",
            "Each Feature SHALL contain the required properties defined in the profile",
            "The service SHALL provide a /collections/{collection_name}/items/{{featureId}} endpoint for individual items"
        ]
    },
    "position": {
        "statement": "{collection_name} position query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/position endpoint",
            "The Position query SHALL accept coords parameter with POINT geometry",
            "The Position query SHALL support datetime parameter",
            "The response SHALL return data for the specified position"
        ]
    },
    "area": {
        "statement": "{collection_name} area query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/area endpoint",
            "The Area query SHALL accept coords parameter with POLYGON or MULTIPOLYGON geometry",
            "The Area query SHALL support datetime parameter",
            "The response SHALL return data within the specified area"
        ]
    },
    "cube": {
        "statement": "{collection_name} cube query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/cube endpoint",
            "The Cube query SHALL accept bbox parameter",
            "The Cube query SHALL support datetime and z parameters",
            "The response SHALL return data within the specified cube"
        ]
    },
    "trajectory": {
        "statement": "{collection_name} trajectory query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/trajectory endpoint",
            "The Trajectory query SHALL accept coords parameter with LINESTRING geometry",
            "The Trajectory query SHALL support datetime parameter",
            "The response SHALL return data along the specified trajectory"
        ]
    },
    "corridor": {
        "statement": "{collection_name} corridor query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/corridor endpoint",
            "The Corridor query SHALL accept coords and corridor-width parameters",
            "The Corridor query SHALL support datetime parameter",
            "The response SHALL return data within the specified corridor"
        ]
    },
    "locations": {
        "statement": "{collection_name} locations query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/locations endpoint",
            "The Locations query SHALL accept locationId parameter",
            "The Locations query SHALL support datetime parameter",
            "The response SHALL return data for the specified location"
        ]
    },
    "instances": {
        "statement": "{collection_name} instances query support",
        "parts": [
            "The service SHALL provide a /collections/{collection_name}/instances endpoint",
            "The Instances endpoint SHALL list available time instances",
            "Each instance SHALL support the same query types as the collection"
        ]
    }
}

# Test step templates for query types
QUERY_TYPE_TEST_STEPS = {
    "items": [
        "Send GET request to /collections/{collection_name}/items",
        "Verify response is valid GeoJSON FeatureCollection",
        "Verify response contains required properties",
        "Send GET request to /collections/{collection_name}/items/{{featureId}}",
        "Verify response is valid GeoJSON Feature"
    ],
    "position": [
        "Send GET request to /collections/{collection_name}/position with coords parameter",
        "Verify response contains data for the specified position",
        "Verify datetime parameter is supported"
    ],
    "area": [
        "Send GET request to /collections/{collection_name}/area with coords parameter",
        "Verify response contains data within the specified area",
        "Verify POLYGON and MULTIPOLYGON geometries are supported"
    ],
    "cube": [
        "Send GET request to /collections/{collection_name}/cube with bbox parameter",
        "Verify response contains data within the specified cube",
        "Verify datetime and z parameters are supported"
    ],
    "trajectory": [
        "Send GET request to /collections/{collection_name}/trajectory with coords parameter",
        "Verify response contains data along the trajectory",
        "Verify LINESTRING geometry is supported"
    ],
    "corridor": [
        "Send GET request to /collections/{collection_name}/corridor with coords and corridor-width parameters",
        "Verify response contains data within the corridor",
        "Verify datetime parameter is supported"
    ],
    "locations": [
        "Send GET request to /collections/{collection_name}/locations",
        "Verify response lists available locations",
        "Send GET request to /collections/{collection_name}/locations/{{locationId}}",
        "Verify response contains data for the specified location"
    ],
    "instances": [
        "Send GET request to /collections/{collection_name}/instances",
        "Verify response lists available time instances",
        "Verify each instance supports the collection's query types"
    ]
}

# Format requirement parts
FORMAT_REQUIREMENTS = {
    "geojson": [
        "A format with the label json SHALL provide GeoJSON output",
        "The GeoJSON output SHALL include standard GeoJSON properties: type, features, geometry, properties, and id",
        "The GeoJSON output SHALL include pagination metadata: numberMatched, numberReturned, and links array"
    ],
    "coveragejson": [
        "A format with the label covjson SHALL provide CoverageJSON output conforming to the CoverageJSON specification"
    ],
    "csv": [
        "A format with the label csv SHALL provide CSV output with appropriate headers"
    ],
    "netcdf": [
        "A format with the label netcdf SHALL provide NetCDF output conforming to CF conventions"
    ],
    "grib": [
        "A format with the label grib SHALL provide GRIB2 output conforming to WMO GRIB2 specification"
    ],
    "grib2": [
        "A format with the label grib SHALL provide GRIB2 output conforming to WMO GRIB2 specification"
    ],
    "zarr": [
        "A format with the label zarr SHALL provide Zarr output conforming to Zarr specification"
    ]
}
