#!/usr/bin/env python3
"""
Script to validate OpenAPI schema generation.
"""
import json
import sys
from pathlib import Path

from app.main import app


def validate_openapi_schema():
    """Validate that OpenAPI schema is generated correctly."""
    try:
        # Generate OpenAPI schema
        schema = app.openapi()

        # Basic validation
        assert "openapi" in schema, "Missing 'openapi' field"
        assert "info" in schema, "Missing 'info' field"
        assert "paths" in schema, "Missing 'paths' field"
        assert "components" in schema, "Missing 'components' field"

        # Validate info
        assert "title" in schema["info"], "Missing 'title' in info"
        assert "version" in schema["info"], "Missing 'version' in info"

        # Validate paths exist
        expected_paths = [
            "/api/v1/health",
            "/api/v1/chat/stream",
            "/api/v1/auth/login",
            "/api/v1/auth/callback",
            "/api/v1/auth/me",
        ]

        for path in expected_paths:
            assert path in schema["paths"], f"Missing path: {path}"

        # Validate schemas exist
        expected_schemas = [
            "ChatMessage",
            "ChatRequest",
            "HealthResponse",
            "OAuthTokenResponse",
            "UserInfoResponse",
        ]

        schemas = schema.get("components", {}).get("schemas", {})
        for schema_name in expected_schemas:
            assert schema_name in schemas, f"Missing schema: {schema_name}"

        # Validate schema structure
        for schema_name, schema_def in schemas.items():
            assert "type" in schema_def or "$ref" in str(
                schema_def
            ), f"Invalid schema: {schema_name}"

        print("✅ OpenAPI schema validation passed!")
        print(f"   - OpenAPI version: {schema['openapi']}")
        print(f"   - Title: {schema['info']['title']}")
        print(f"   - Version: {schema['info']['version']}")
        print(f"   - Paths: {len(schema['paths'])}")
        print(f"   - Schemas: {len(schemas)}")

        # Save schema for inspection
        output_file = Path("openapi_schema.json")
        with open(output_file, "w") as f:
            json.dump(schema, f, indent=2)
        print(f"   - Schema saved to: {output_file}")

        return True

    except AssertionError as e:
        print(f"❌ OpenAPI validation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating OpenAPI schema: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = validate_openapi_schema()
    sys.exit(0 if success else 1)
