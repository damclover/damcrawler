#!/usr/bin/env python3

import pyfiglet
import argparse
import subprocess
import sys
import re
import requests


def banner():
    banner = pyfiglet.figlet_format("ParamFinder", font="big")
    print('\n\n---------------------------------------------------------------')
    print(f"{banner}")
    print("                       by DamClover")
    print("---------------------------------------------------------------\n\n")


def show_help():
    print("PS.: Automation of the gau tool to find parameters possibly vulnerable to SQLi, XSS or LFI and some others, depending on your creativity.\n")
    print("Usage:")
    print("  python3 paramfinder.py -u <url> [options]\n")
    print("Options:")
    print("  -u, --url         Target URL to extract parameters from")
    print("  -p, --param       Filter by specific parameters (comma-separated, e.g. id,page)")
    print("  -o, --output      Save the found results to a file")
    print("  -np, --no-param   Show only .php links without parameters")
    print("  -f, --file        Filter links with file extensions (comma-separated, e.g. html,php,txt)")
    print("  -kw, --key-words  Search for keywords inside the URLs (comma-separated, e.g. upload,files,admin)")
    print("  -g, --generic     Search for generic parameters like ?q=, ?search=, ?s= etc")
    print("  -t, --title       Filter by page title keywords (comma-separated, e.g. login,admin)")
    print("  -s, --silent      Silent mode: only shows scanning message")
    print("  -h, --help        Show this help message\n")
    print("Examples:")
    print("  python3 paramfinder.py -u https://example.com")
    print("  python3 paramfinder.py -u https://example.com -p id,page")
    print("  python3 paramfinder.py -u https://example.com -np")
    print("  python3 paramfinder.py -u https://example.com -f php,html")
    print("  python3 paramfinder.py -u https://example.com -kw upload,files")
    print("  python3 paramfinder.py -u https://example.com -g")
    print("  python3 paramfinder.py -u https://example.com -g -t login,admin")
    print("  python3 paramfinder.py -u https://example.com -s")
    sys.exit(0)


def error(msg):
    print(f"\n[ERROR] {msg}")
    print("Use -h or --help to see usage instructions.\n")
    sys.exit(1)


def show_inputs(url, filters, file_filter, keywords, no_param, generic, titles):
    print(f"Target: {url}")
    if filters:
        print("Params:", ', '.join(filters))
    if keywords:
        print("Key words:", ', '.join(keywords))
    if file_filter:
        print("Extensions:", ', '.join(file_filter))
    if generic:
        print("Generic params enabled (e.g. ?q=, ?search=)")
    if titles:
        print("Title filters:", ', '.join(titles))
    if no_param:
        print("Only .php files without parameters")
    print("\n")


def title_matches(url, title_filters):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=3)
        if "<title>" in response.text.lower():
            title = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
            if title:
                page_title = title.group(1).lower()
                return any(t.lower() in page_title for t in title_filters)
    except:
        pass
    return False


def find_params(url, output, filters, no_param, file_filter, keywords, generic, title_filters):
    if not re.match(r'^https?://', url):
        error("Invalid URL. Make sure to use the correct format (http:// or https://).")

    try:
        result = subprocess.run(['gau', url], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        error("'gau' is not installed or not found in PATH.")
    except subprocess.CalledProcessError as e:
        error(f"Error running gau: {e}")

    found = set()

    for line in result.stdout.splitlines():
        matched = False

        if no_param and line.endswith('.php') and '?' not in line:
            matched = True

        elif file_filter:
            for ext in file_filter:
                if line.lower().endswith(f".{ext.lower()}"):
                    matched = True

        elif keywords:
            for kw in keywords:
                if kw.lower() in line.lower():
                    matched = True

        elif generic and '?' in line and '=' in line:
            if re.search(r'[?&](q|s|search|query|keyword|term)=', line, re.IGNORECASE):
                matched = True

        elif filters:
            if '?' in line and '=' in line:
                base, query = line.split('?', 1)
                for param in query.split('&'):
                    key = param.split('=')[0]
                    if key in filters:
                        found.add(f"{base}?{key}=")
                        matched = False  # already added above

        elif not no_param and not file_filter and not keywords and not filters and not generic:
            if '.php?' in line and '=' in line:
                try:
                    base, query = line.split('?', 1)
                    for param in query.split('&'):
                        key = param.split('=')[0]
                        found.add(f"{base}?{key}=")
                except Exception:
                    continue

        if matched:
            if title_filters:
                if title_matches(line, title_filters):
                    found.add(line)
            else:
                found.add(line)

    sorted_output = sorted(found)

    if output:
        try:
            with open(output, 'w') as f:
                f.write('\n'.join(sorted_output))
            print(f"Results saved to: {output}")
        except Exception as e:
            error(f"Failed to write output file: {e}")
    else:
        for item in sorted_output:
            print(item)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-p', '--param', help='Comma-separated list of parameters to filter')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-np', '--no-param', action='store_true', help='Only show .php files without parameters')
    parser.add_argument('-f', '--file', help='File extensions to look for (e.g. php,html)')
    parser.add_argument('-kw', '--key-words', help='Keywords to search in URLs (e.g. upload,files)')
    parser.add_argument('-g', '--generic', action='store_true', help='Include generic param URLs like ?q=, ?s=')
    parser.add_argument('-t', '--title', help='Filter by page title keywords (e.g. login,admin)')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    args = parser.parse_args()

    if args.help:
        banner()
        show_help()

    if not args.url:
        banner()
        error("URL is required. Use -u or --url to provide it.")

    filters = args.param.split(',') if args.param else None
    file_filter = args.file.split(',') if args.file else None
    keywords = args.key_words.split(',') if args.key_words else None
    titles = args.title.split(',') if args.title else None

    # Argument validation
    active_filters = sum([
        bool(args.param),
        bool(args.file),
        bool(args.key_words),
        bool(args.generic)
    ])

    if args.no_param and (args.param or args.file or args.key_words or args.generic):
        banner()
        error("--no-param (-np) cannot be used with --param (-p), --file (-f), --key-words (-kw) or --generic (-g).")

    if active_filters > 1:
        banner()
        error("Use only one of: --param (-p), --file (-f), --key-words (-kw), or --generic (-g).")

    if args.title and args.no_param:
        banner()
        error("--title (-t) cannot be used with --no-param (-np).")

    if args.silent:
        print(f"\nScanning {args.url}...\n\n")
    else:
        banner()
        show_inputs(args.url, filters, file_filter, keywords, args.no_param, args.generic, titles)

    find_params(args.url, args.output, filters, args.no_param, file_filter, keywords, args.generic, titles)


if __name__ == '__main__':
    main()
