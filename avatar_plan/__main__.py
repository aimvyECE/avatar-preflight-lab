"""Usage: python -m avatar_plan manifest.json"""
import argparse
import json
import sys
from .core import plan


def reject_constant(value):
    raise ValueError(f"non-standard JSON numeric constant: {value}")


def main():
    parser = argparse.ArgumentParser(description="Validate an offline avatar plan; does not generate media.")
    parser.add_argument("manifest")
    args = parser.parse_args()
    try:
        with open(args.manifest, encoding="utf-8") as source:
            data = json.load(source, parse_constant=reject_constant)
        result = plan(data)
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print(json.dumps({"status": "input_error", "message": str(error)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "declarations_valid" else 1


if __name__ == "__main__":
    sys.exit(main())
