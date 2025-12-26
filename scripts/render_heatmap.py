#!/usr/bin/env python3
import json
import sys
import os
import argparse
from jinja2 import Template, Environment, FileSystemLoader

def render_heatmap(data):
    """
    Renders the heatmap JSX template using the provided data.
    """
    # Setup Jinja2 environment
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, '../assets')
    env = Environment(
        loader=FileSystemLoader(template_dir),
        variable_start_string='[[',
        variable_end_string=']]',
        block_start_string='[%',
        block_end_string='%]',
    )
    env.filters['tojson'] = json.dumps
    
    # Load the template
    try:
        template = env.get_template('heatmap.jsx.j2')
    except Exception as e:
        print(f"Error loading template: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Render the template
    try:
        output = template.render(**data)
        return output
    except Exception as e:
        print(f"Error rendering template: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Render Commit Heatmap JSX component with dynamic data.")
    parser.add_argument('input_file', nargs='?', help="Path to input JSON file. If not provided, reads from stdin.")
    
    args = parser.parse_args()
    
    if args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
             print("Please provide input JSON via stdin or filename.", file=sys.stderr)
             parser.print_help()
             sys.exit(1)
        try:
            data = json.load(sys.stdin)
        except Exception as e:
            print(f"Error parsing JSON from stdin: {e}", file=sys.stderr)
            sys.exit(1)

    result = render_heatmap(data)
    print(result)

if __name__ == "__main__":
    main()
