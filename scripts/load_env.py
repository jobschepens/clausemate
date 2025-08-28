#!/usr/bin/env python3
"""Load environment variables from .env file into the system environment."""

import os
from pathlib import Path


def load_env_file(env_path: str = ".env") -> dict[str, str]:
    """Load environment variables from a .env file.

    Args:
        env_path: Path to the .env file (default: ".env")

    Returns:
        Dictionary of environment variables loaded

    Raises:
        FileNotFoundError: If the .env file doesn't exist
    """
    env_file = Path(env_path)

    if not env_file.exists():
        raise FileNotFoundError(f"Environment file not found: {env_path}")

    loaded_vars = {}

    with open(env_file, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Parse KEY=VALUE format
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if (
                    value.startswith('"')
                    and value.endswith('"')
                    or value.startswith("'")
                    and value.endswith("'")
                ):
                    value = value[1:-1]

                # Set environment variable
                os.environ[key] = value
                loaded_vars[key] = value
                print(f"✅ Loaded: {key}")
            else:
                print(f"⚠️  Skipping invalid line {line_num}: {line}")

    return loaded_vars


def main():
    """Main function to load environment variables."""
    try:
        print("🔧 Loading environment variables from .env file...")
        loaded_vars = load_env_file()

        print("\n📊 Summary:")
        print(f"   • Loaded {len(loaded_vars)} environment variables")
        print(f"   • Variables: {', '.join(loaded_vars.keys())}")

        print("\n🔍 Current environment variables:")
        for key in loaded_vars:
            # Mask sensitive values for display
            value = os.environ.get(key, "")
            if any(
                sensitive in key.lower()
                for sensitive in ["key", "token", "secret", "password"]
            ):
                masked_value = (
                    value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                )
                print(f"   • {key}={masked_value}")
            else:
                print(f"   • {key}={value}")

        print("\n✅ Environment variables successfully loaded and available for use!")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
