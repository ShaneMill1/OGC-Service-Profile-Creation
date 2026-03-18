# =================================================================
#
# Authors: Shane Mill <shane.mill@noaa.gov>
#
# Copyright (c) 2026 Shane Mill
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
OGC API - EDR Part 3: Service Profile — Authoritative Pydantic Models

These models ARE the schema. Instantiating a ServiceProfile validates the
entire profile structure before any files are written.

Collections are modelled using edr-pydantic (https://github.com/KNMI/edr-pydantic)
so that EDR data model types are authoritative and shared with the broader ecosystem.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from edr_pydantic.collections import Collection as EDRCollection
from pydantic import BaseModel, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# Enumerations (profile-specific; EDR data model enums live in edr-pydantic)
# ---------------------------------------------------------------------------

class FilterType(str, Enum):
    string = "string"
    number = "number"
    array = "array"
    boolean = "boolean"


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------

class Requirement(BaseModel):
    id: Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9\-]*$")]
    statement: str
    parts: list[str] = Field(min_length=1)

    @field_validator("id")
    @classmethod
    def no_trailing_dash(cls, v: str) -> str:
        if v.endswith("-"):
            raise ValueError("requirement id must not end with a dash")
        return v


class AbstractTest(BaseModel):
    id: str  # mirrors the requirement id it tests
    requirement_id: str
    steps: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def ids_must_match(self) -> AbstractTest:
        if self.id != self.requirement_id:
            raise ValueError("AbstractTest.id must equal requirement_id")
        return self


class SubscriptionFilter(BaseModel):
    name: str
    description: str
    type: FilterType = FilterType.string


class ExtentRequirements(BaseModel):
    """Profile-level extent restrictions per OGC API - EDR Part 3."""
    minimum_bbox: list[float] = Field(min_length=4, max_length=4, description="Minimum spatial bounds [minLon, minLat, maxLon, maxLat]")
    allowed_crs: list[str] | None = Field(default=None, description="Enumerated list of valid CRS values")
    crs_pattern: str | None = Field(default=None, description="Regular expression defining valid CRS string patterns")
    allowed_trs: list[str] | None = Field(default=None, description="Enumerated list of valid TRS values")
    trs_pattern: str | None = Field(default=None, description="Regular expression defining valid TRS string patterns")
    allowed_vrs: list[str] | None = Field(default=None, description="Enumerated list of valid VRS values")
    vrs_pattern: str | None = Field(default=None, description="Regular expression defining valid VRS string patterns")

    @model_validator(mode="after")
    def validate_crs_specification(self) -> ExtentRequirements:
        if self.allowed_crs is None and self.crs_pattern is None:
            raise ValueError("Either allowed_crs or crs_pattern must be specified")
        return self


class OutputFormat(BaseModel):
    """Output format with schema reference per OGC API - EDR Part 3."""
    name: str = Field(description="Format name (e.g., GeoJSON, CoverageJSON)")
    media_type: str = Field(description="MIME type (e.g., application/geo+json)")
    schema_ref: str | None = Field(default=None, description="URL to schema definition")


# Collection IS the edr-pydantic Collection — no wrapper needed.
# edr_pydantic.collections.Collection models id, extent, data_queries,
# output_formats, parameter_names, links — all authoritative EDR fields.
Collection = EDRCollection


class DocumentMetadata(BaseModel):
    """Metanorma/OGC document header metadata for PDF compilation."""
    doc_number: str
    doc_subtype: Literal["implementation", "best-practice", "engineering-report"] = "implementation"
    editors: list[str] = Field(default_factory=list)
    submitting_orgs: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    copyright_year: int = Field(default=2026)
    external_id: str | None = None


class PubSubServer(BaseModel):
    """A single pub/sub server endpoint."""
    name: str
    description: str = ""
    host: str
    port: int | None = None
    protocol: Literal["amqp", "mqtt", "kafka", "ws", "wss"] = "amqp"
    pathname: str | None = None


class CollectionPubSub(BaseModel):
    """Per-collection pub/sub filter overrides."""
    filters: list[SubscriptionFilter] = Field(default_factory=list)


class PubSubConfig(BaseModel):
    """Optional OGC API - EDR Part 2 (PubSub) configuration."""
    broker_host: str = "localhost"
    broker_port: int = Field(default=5672, ge=1, le=65535)
    protocol: Literal["amqp", "mqtt", "kafka"] = "amqp"
    collections: list[str] = Field(default_factory=list, description="Collection IDs that support PubSub")
    filters: list[SubscriptionFilter] = Field(default_factory=list)
    servers: list[PubSubServer] = Field(default_factory=list, description="Additional server endpoints (ws, wss)")
    collection_filters: dict[str, CollectionPubSub] = Field(default_factory=dict, description="Per-collection filter overrides")


# ---------------------------------------------------------------------------
# Root model — the authoritative profile definition
# ---------------------------------------------------------------------------

class ServiceProfile(BaseModel):
    """
    OGC API - EDR Part 3 Service Profile.

    Instantiating this model validates the entire profile. Export to dict/JSON
    for downstream serialization (OpenAPI, AsyncAPI, AsciiDoc, YAML config).
    """

    name: Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]
    title: str
    version: str = "1.0"
    server_url: str | None = Field(default=None, description="Base URL for implementation (not used in profile OpenAPI per standard)")
    collections: list[Collection] = Field(min_length=1)
    collection_examples: dict[str, dict] = Field(default_factory=dict)
    requirements: list[Requirement] = Field(default_factory=list)
    abstract_tests: list[AbstractTest] = Field(default_factory=list)
    pubsub: PubSubConfig | None = None
    processes: list[dict] = Field(default_factory=list)
    document_metadata: DocumentMetadata | None = None
    
    # OGC API - EDR Part 3 specific fields
    required_conformance_classes: list[str] = Field(
        default_factory=lambda: [
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core"
        ],
        description="Conformance classes that implementations must declare"
    )
    extent_requirements: ExtentRequirements | None = Field(
        default=None,
        description="Profile-level extent restrictions"
    )
    output_formats: list[OutputFormat] = Field(
        default_factory=list,
        description="Profile-level output format definitions with schema references"
    )
    collection_id_pattern: str | None = Field(
        default=None,
        description="Regex pattern for valid collection IDs"
    )

    # OGC identifiers derived from name — not user-supplied
    @property
    def req_uri(self) -> str:
        return f"http://www.opengis.net/spec/ogcapi-edr-3/1.0/req/{self.name}"

    @property
    def conf_uri(self) -> str:
        return f"http://www.opengis.net/spec/ogcapi-edr-3/1.0/conf/{self.name}"

    @model_validator(mode="after")
    def tests_reference_valid_requirements(self) -> ServiceProfile:
        req_ids = {r.id for r in self.requirements}
        for test in self.abstract_tests:
            if test.requirement_id not in req_ids:
                raise ValueError(
                    f"AbstractTest '{test.id}' references unknown requirement '{test.requirement_id}'"
                )
        return self

    @model_validator(mode="after")
    def no_duplicate_collection_ids(self) -> ServiceProfile:
        ids = [c.id for c in self.collections]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate collection ids in profile")
        return self

    @model_validator(mode="after")
    def validate_parameter_completeness(self) -> ServiceProfile:
        """Validate parameter_names completeness per OGC API - EDR Part 3 REQ_parameter-names."""
        for coll in self.collections:
            if not coll.parameter_names:
                continue
            for param_name, param in coll.parameter_names.root.items():
                # Check if unit is specified
                if not hasattr(param, 'unit') or param.unit is None:
                    raise ValueError(
                        f"Parameter '{param_name}' in collection '{coll.id}' must specify unit "
                        f"(required by OGC API - EDR Part 3 REQ_parameter-names)"
                    )
                # Check if observedProperty is specified (already required by edr-pydantic)
                if not hasattr(param, 'observedProperty') or param.observedProperty is None:
                    raise ValueError(
                        f"Parameter '{param_name}' in collection '{coll.id}' must specify observedProperty"
                    )
        return self

    @model_validator(mode="after")
    def validate_pubsub_conformance(self) -> ServiceProfile:
        """Ensure pub/sub requirements include Part 2 conformance per REQ_pubsub."""
        if self.pubsub:
            # Check if there's a requirement for Part 2 conformance
            has_part2_req = any(
                "part 2" in req.statement.lower() or "part-2" in req.statement.lower() or "pubsub" in req.statement.lower()
                for req in self.requirements
            )
            if not has_part2_req:
                # Auto-add the requirement
                self.requirements.append(
                    Requirement(
                        id="pubsub-part2-conformance",
                        statement="The service SHALL conform to OGC API - EDR Part 2: Publish-Subscribe",
                        parts=[
                            "The service SHALL implement the channels defined in the AsyncAPI document",
                            "The service SHALL support the message payloads defined for each channel"
                        ]
                    )
                )
        return self
