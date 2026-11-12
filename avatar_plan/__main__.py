"""Usage: python -m avatar_plan manifest.json"""
import argparse
import json
import sys
from .audit import audit, unique_object


def reject_constant(value):
    raise ValueError(f"non-standard JSON numeric constant: {value}")


def main():
    parser = argparse.ArgumentParser(description="Validate an offline avatar plan; does not generate media.")
    parser.add_argument("manifest")
    parser.add_argument("--compare", help="Previous manifest; report changed JSON Pointer paths without values")
    args = parser.parse_args()
    try:
        with open(args.manifest, encoding="utf-8") as source:
            data = json.load(source, parse_constant=reject_constant, object_pairs_hook=unique_object)
        previous = None
        if args.compare:
            with open(args.compare, encoding="utf-8") as source:
                previous = json.load(source, parse_constant=reject_constant, object_pairs_hook=unique_object)
            if previous is None:
                raise ValueError("previous manifest cannot be null")
        result = audit(data, previous)
    except (OSError, ValueError, TypeError, RecursionError) as error:
        print(json.dumps({"status": "input_error", "message": str(error)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "declarations_valid" else 1


if __name__ == "__main__":
    sys.exit(main())
