#!/usr/bin/env python3
import argparse
import json
import sys
import isbnlib




def classify_isbn(raw: str):
    canonical = isbnlib.canonical(raw)
    if not canonical:
        return None, None

    if isbnlib.is_isbn10(canonical):
        return canonical, "ISBN-10"
    if isbnlib.is_isbn13(canonical):
        return canonical, "ISBN-13"
    return None, None


def fetch_metadata(canonical: str):
    # Try the provided ISBN first, then its converted counterpart.
    candidates = [canonical]
    if isbnlib.is_isbn10(canonical):
        converted = isbnlib.to_isbn13(canonical)
        if converted:
            candidates.append(converted)
    elif isbnlib.is_isbn13(canonical):
        converted = isbnlib.to_isbn10(canonical)
        if converted:
            candidates.append(converted)

    for candidate in candidates:
        try:
            data = isbnlib.meta(candidate)
            if data:
                return data
        except Exception:
            continue
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Validate an ISBN-10/ISBN-13 and retrieve metadata using isbnlib."
    )
    parser.add_argument("isbn", help="ISBN input (with or without hyphens/spaces)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print metadata as JSON",
    )
    args = parser.parse_args()

    canonical, isbn_type = classify_isbn(args.isbn)
    if not canonical:
        print("Invalid ISBN: input is not a valid ISBN-10 or ISBN-13.", file=sys.stderr)
        sys.exit(1)

    isbn10 = isbnlib.to_isbn10(canonical) if isbnlib.is_isbn13(canonical) else canonical
    isbn13 = isbnlib.to_isbn13(canonical) if isbnlib.is_isbn10(canonical) else canonical

    metadata = fetch_metadata(canonical)
    if metadata is None:
        print(f"Valid {isbn_type}, but no metadata found.")
        print(f"Canonical: {canonical}")
        if isbn10:
            print(f"ISBN-10 : {isbnlib.clean(isbn10)}")
        if isbn13:
            print(f"ISBN-13 : {isbnlib.clean(isbn13)}")
        sys.exit(2)

    if args.json:
        output = {
            "input": args.isbn,
            "canonical": canonical,
            "type": isbn_type,
            "isbn10": isbn10,
            "isbn13": isbn13,
            "metadata": metadata,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Valid {isbn_type}")
        print(f"Canonical: {canonical}")
        if isbn10:
            print(f"ISBN-10 : {isbnlib.clean(isbn10)}")
        if isbn13:
            print(f"ISBN-13 : {isbnlib.clean(isbn13)}")
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"- {key}: {value}")


if __name__ == "__main__":
    main()