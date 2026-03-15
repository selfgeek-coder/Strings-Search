import re
import sys
import argparse
from pathlib import Path

def extract_strings(file_path, min_length=4):
    strings = []
    current = []

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            for byte in data:
                if 32 <= byte <= 126:
                    current.append(chr(byte))
                else:
                    if len(current) >= min_length:
                        strings.append(''.join(current))
                    current = []

            if len(current) >= min_length:
                strings.append(''.join(current))

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    return strings

def main():
    parser = argparse.ArgumentParser(
        description="Extract strings from a binary file with optional regex filtering",
        epilog="Example: python restrings.py program.exe 'http[s]?://\\S+'"
    )
    parser.add_argument('file', help='Path to the binary file')
    parser.add_argument('regex', nargs='?', default='.*',
                        help='Regex pattern to filter strings (default: all strings)')
    parser.add_argument('-m', '--min-length', type=int, default=4,
                        help='Minimum string length (default: 4)')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='Ignore case when matching regex')

    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: File '{args.file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        flags = re.IGNORECASE if args.ignore_case else 0
        pattern = re.compile(args.regex, flags)
    except re.error as e:
        print(f"Invalid regex: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Searching file: {args.file}")
    print(f"Regex pattern: {args.regex}")
    print(f"Minimum string length: {args.min_length}")
    print("-" * 50)

    strings = extract_strings(file_path, args.min_length)

    matches = [s for s in strings if pattern.search(s)]
    for s in matches:
        print(s)

    print("-" * 50)
    print(f"Strings found: {len(matches)}")

    if not matches:
        print("No matches found.")
        sys.exit(1)

if __name__ == "__main__":
    main()