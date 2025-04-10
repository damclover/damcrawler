#!/usr/bin/env python3

import pyfiglet
import argparse
import subprocess
import sys
import re


def banner():
    banner = pyfiglet.figlet_format("ParamFinder", font="big")

    print(f"\n\n{banner}")
    print("                       by DamClover")
    print("---------------------------------------------------------------\n\n")


def show_help():
    print("Usage:")
    print("  python3 paramfinder.py -u <url> [-o <output_file>]\n")
    print("Options:")
    print("  -u, --url       Target URL to extract parameters from")
    print("  -o, --output    Save the found parameters to a file")
    print("  -h, --help      Show this help message\n")
    print("Examples:")
    print("  python3 paramfinder.py -u https://example.com")
    print("  python3 paramfinder.py --url https://example.com --output params.txt")
    sys.exit(0)


def error(msg):
    print(f"Error: {msg}")
    print("Use -h or --help to see usage instructions.")
    sys.exit(1)


def find_params(url, output):
    if not re.match(r'^https?://', url):
        error("Invalid URL. Make sure to use the correct format (http:// or https://).")

    try:
        result = subprocess.run(['gau', url], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        error("'gau' is not installed or not found in PATH.")
    except subprocess.CalledProcessError as e:
        error(f"Error running gau: {e}")

    found_params = set()

    for line in result.stdout.splitlines():
        if '.php?' in line and '=' in line:
            try:
                base, query = line.split('?', 1)
                for param in query.split('&'):
                    key = param.split('=')[0]
                    found_params.add(f"{base}?{key}=")
            except Exception:
                continue

    sorted_params = sorted(found_params)

    if output:
        try:
            with open(output, 'w') as f:
                f.write('\n'.join(sorted_params))
            print(f"Parameters saved to: {output}")
        except Exception as e:
            error(f"Failed to write output file: {e}")
    else:
        for param in sorted_params:
            print(param)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    args = parser.parse_args()

    banner()

    if args.help:
        show_help()

    if not args.url:
        error("URL is required. Use -u or --url to provide it.")

    find_params(args.url, args.output)


if __name__ == '__main__':
    main()
