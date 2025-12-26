# 2025 Coding Artifact: Developer Commit Heatmap Skill

Generate a standalone React component for developer activity analysis. This skill guides agents to query `mergestat`, format the data, and render a Jinja2 template via Python to produce a self-contained JSX artifact.

## Features

-   **Interactive Heatmap**: Visualize commit activity by day of the week and hour.
-   **Contribution Graph**: View annual contributions in a grid format.
-   **Insights & Stats**: Automated highlights of developer contribution patterns.
-   **Slack Integration**: Generates Block Kit JSON for easy sharing of results on Slack.

## Philosophy

This project follows a **Data -> Template -> Artifact** workflow:
1.  **Extract**: SQL queries against `mergestat` (via MCP) gather raw commit data.
2.  **Transform**: Data is structured into a JSON format defined by the template schema.
3.  **Render**: A Python script hydrates the Jinja2 template with the JSON data.
4.  **Produce**: The final output is a standalone JSX file ready for use.

## Project Structure

-   `assets/heatmap.jsx.j2`: Jinja2 template for the React component.
-   `scripts/render_heatmap.py`: Python script to render the template.
-   `SKILL.md`: Detailed documentation for the Claude Skill.
-   `2025-coding-artifact.skill`: Claude Skill definition.

## Getting Started

### Prerequisites

-   Python 3.x
-   `jinja2` Python package
-   [mergestat-mcp](https://github.com/alc0der/mergestat-mcp) (Required for data extraction)

### Usage

1.  **Prepare your data**: Create a JSON file (e.g., `data.json`) based on the structure in `assets/sample_data.json`.
2.  **Render the heatmap**:

    ```bash
    # Read from a file
    python3 scripts/render_heatmap.py data.json > MyHeatmap.jsx

    # Or pipe from stdin
    cat data.json | python3 scripts/render_heatmap.py > MyHeatmap.jsx
    ```

3.  **Use the artifact**: The resulting `MyHeatmap.jsx` is a self-contained React component.

## More Information

For more details on SQL queries and data schemas, please refer to [SKILL.md](SKILL.md).
