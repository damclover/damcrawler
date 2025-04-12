#!/usr/bin/env python3

import pyfiglet
import argparse
import subprocess
import sys
import re
import requests


def banner():
    banner = pyfiglet.figlet_format("DamCrawler", font="big")
    print('\n\n---------------------------------------------------------------')
    print(f"{banner}")
    print("                       by DamClover")
    print("---------------------------------------------------------------\n\n")


def show_help():
    print("PS.: Automation of the gau tool to find parameters possibly vulnerable to SQLi, XSS or LFI and some others, depending on your creativity.\n")
    print("Usage:")
    print("  python3 DamCrawler.py -u <url> [options]\n")
    print("Options:")
    print("  -u, --url         Target URL to extract parameters from")
    print("  -p, --param       Filter by specific parameters (comma-separated, e.g. id,page)")
    print("  -o, --output      Save the found results to a file")
    print("  -np, --no-param   Show only .php links without parameters")
    print("  -f, --file        Filter links with file extensions (comma-separated, e.g. html,php,txt)")
    print("  -kw, --key-words  Search for keywords inside the URLs (comma-separated, e.g. upload,files,admin)")
    print("  -g, --generic     Search for generic parameters like ?q=, ?search=, ?s= etc")
    print("  -un, --unique     Show only one URL per unique parameter")
    print("  -s, --silent      Silent mode: only shows scanning message")
    print("  -h, --help        Show this help message\n")
    print("Examples:")
    print("  python3 DamCrawler.py -u https://example.com")
    print("  python3 DamCrawler.py -u https://example.com -p id,page")
    print("  python3 DamCrawler.py -u https://example.com -np")
    print("  python3 DamCrawler.py -u https://example.com -f php,html")
    print("  python3 DamCrawler.py -u https://example.com -kw upload,files")
    print("  python3 DamCrawler.py -u https://example.com -g")
    print("  python3 DamCrawler.py -u https://example.com -un")
    print("  python3 DamCrawler.py -u https://example.com -s")
    sys.exit(0)


def error(msg):
    print(f"\n[ERROR] {msg}")
    print("Use -h or --help to see usage instructions.\n")
    sys.exit(1)


def show_inputs(url, filters, file_filter, keywords, no_param, generic, unique):
    print(f"Target: {url}")
    if filters:
        print("Params:", ', '.join(filters))
    if keywords:
        print("Key words:", ', '.join(keywords))
    if file_filter:
        print("Extensions:", ', '.join(file_filter))
    if generic:
        print("Generic params enabled (e.g. ?q=, ?search=)")
    if unique:
        print("Unique param mode: ON")
    if no_param:
        print("Only .php files without parameters")
    print("\n")


def find_params(url, output, filters, no_param, file_filter, keywords, generic, unique):
    if not re.match(r'^https?://', url):
        error("Invalid URL. Make sure to use the correct format (http:// or https://).")

    try:
        result = subprocess.run(['gau', url], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        error("'gau' is not installed or not found in PATH.")
    except subprocess.CalledProcessError as e:
        error(f"Error running gau: {e}")

    found = dict() if unique else set()

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
            # Adicionar filtro para excluir links com .php quando usar -g
            if '.php' not in line.lower() and re.search(r'[?&](q|s|search|query|keyword|term)=', line, re.IGNORECASE):
                matched = True

        elif filters:
            if '?' in line and '=' in line:
                base, query = line.split('?', 1)
                for param in query.split('&'):
                    key = param.split('=')[0]
                    if key in filters:
                        if unique:
                            if key not in found:
                                found[key] = f"{base}?{key}="
                        else:
                            found.add(f"{base}?{key}=")
                        matched = False

        elif not no_param and not file_filter and not keywords and not filters and not generic:
            if '.php?' in line and '=' in line:
                try:
                    base, query = line.split('?', 1)
                    for param in query.split('&'):
                        key = param.split('=')[0]
                        if unique:
                            if key not in found:
                                found[key] = f"{base}?{key}="
                        else:
                            found.add(f"{base}?{key}=")
                except Exception:
                    continue

        if matched and not filters:
            if unique:
                # Tenta pegar o primeiro parâmetro da URL
                if '?' in line and '=' in line:
                    try:
                        _, query = line.split('?', 1)
                        param = query.split('&')[0].split('=')[0]
                        if param not in found:
                            found[param] = line
                    except:
                        continue
            else:
                found.add(line)

    sorted_output = sorted(found.values() if unique else found)

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
    parser.add_argument('-un', '--unique', action='store_true', help='Show only one URL per unique parameter')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')

    # Primeiro validar todos os argumentos
    args = sys.argv[1:]  # Ignorar o nome do script
    valid_opts = []
    for action in parser._actions:
        if action.option_strings:
            valid_opts.extend(action.option_strings)
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        # Verificar se é um argumento válido
        if arg in valid_opts:
            # Pular o valor do argumento se necessário
            if not arg.startswith('--') and len(arg) == 2:  # Argumento curto (-x)
                if i+1 < len(args) and not args[i+1].startswith('-'):
                    i += 1
            i += 1
            continue
            
        # Bloqueio explícito para -gs/--gs
        if arg in ('-gs', '--gs'):
            banner()
            error("Invalid argument: -gs/--gs is not a valid option")
            
        # Verificar se é um valor (não um argumento)
        if not arg.startswith('-'):
            i += 1
            continue
            
        # Argumento inválido encontrado
        banner()
        error(f"Invalid argument: {arg} is not a valid option")

    # Agora parsear os argumentos válidos
    known_args = parser.parse_args()

    if known_args.help:
        banner()
        show_help()

    if not known_args.url:
        banner()
        error("URL is required. Use -u or --url to provide it.")

    filters = known_args.param.split(',') if known_args.param else None
    file_filter = known_args.file.split(',') if known_args.file else None
    keywords = known_args.key_words.split(',') if known_args.key_words else None

    # Argument validation
    active_filters = sum([
        bool(known_args.param),
        bool(known_args.file),
        bool(known_args.key_words),
        bool(known_args.generic)
    ])

    if known_args.no_param and active_filters > 0:
        banner()
        error("--no-param (-np) cannot be used with --param (-p), --file (-f), --key-words (-kw) or --generic (-g).")

    if active_filters > 1:
        banner()
        error("Use only one of: --param (-p), --file (-f), --key-words (-kw), or --generic (-g).")

    if known_args.silent:
        pass
    else:
        banner()
        show_inputs(known_args.url, filters, file_filter, keywords, known_args.no_param, known_args.generic, known_args.unique)

    find_params(known_args.url, known_args.output, filters, known_args.no_param, file_filter, keywords, known_args.generic, known_args.unique)


if __name__ == '__main__':
    main()
