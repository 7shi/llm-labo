#!/usr/bin/env python3

import argparse
import re
import sys

def convert_bold_sequences(text):
    """Convert TTY bold control sequences to Markdown bold markers."""
    # Convert hex sequences to actual escape sequences
    # 1b 5b 31 6d = \x1b[1m (bold start)
    # 1b 5b 32 32 6d = \x1b[22m (bold end)
    
    # Replace both bold start and end sequences with **
    text = re.sub(r'\x1b\[1m', '**', text)
    text = re.sub(r'\x1b\[22m', '**', text)
    
    return text

def main():
    parser = argparse.ArgumentParser(description='Convert TTY bold control sequences to Markdown bold markers')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('input', nargs='?', help='Input file path (optional, uses stdin if not provided)')
    
    args = parser.parse_args()
    
    try:
        # Read input
        if args.input:
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = sys.stdin.read()
        
        # Convert sequences
        converted = convert_bold_sequences(content)
        
        # Write output
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(converted)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()