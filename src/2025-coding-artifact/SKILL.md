---
name: 2025-coding-artifact
description: Generate a standalone React component for developer activity analysis by querying mergestat, formatting data, and rendering a Jinja2 template via Python. Creates a fully self-contained JSX artifact with interactive heatmaps and Slack sharing capabilities.
---

# Developer Insights Scheme

Generate comprehensive developer activity analysis and visual commit heatmaps by combining SQL queries with template-based code generation.

## Philosophy

This skill follows a **Data -> Template -> Artifact** philosophy:
1. **Query**: Extract raw data using `mergestat` (SQL).
2. **Transform**: Structure the data into a JSON payload matching the template schema.
3. **Render**: Use the provided Python script to hydrate the Jinja2 template (`assets/heatmap.jsx.j2`).
4. **Deliver**: Present the resulting standalone JSX file as the final artifact.

### 1. Query Commits

Use the `mergestat` MCP tool to query commit data. 
*Note: Always check `references/author-mapping.md` (if available) to normalize author names.*

**Query for `daily_commits`:**
```sql
SELECT 
  strftime('%Y-%m-%d', author_when) AS date,
  COUNT(*) AS count
FROM commits
WHERE author_name IN ('Target Developer', 'Alias')
  AND author_when >= '2025-01-01'
GROUP BY 1
ORDER BY 1 ASC
```

**Query for `raw_data` (Day x Hour buckets):**
```sql
SELECT 
  CAST(strftime('%w', author_when) AS INTEGER) AS day,
  CAST(strftime('%H', author_when) AS INTEGER) AS hour,
  COUNT(*) AS commits
FROM commits
WHERE author_name IN ('Target Developer', 'Alias')
  AND author_when >= '2025-01-01'
GROUP BY 1, 2
ORDER BY 1, 2
```

### 2. Prepare Data Payload
Construct a JSON object that satisfies the variables in `assets/heatmap.jsx.j2`.

**Required JSON Structure:**
```json
{
  "component_name": "DeveloperCommitHeatmap",
  "user_full_name": "Jane Doe",
  "user_first_name": "Jane",
  "repo_name": "my-project",
  "year": 2025,
  "last_refreshed_date": "Jan 1, 2025",
  "raw_data": [
    { "day": 0, "hour": 14, "commits": 5 },
    { "day": 1, "hour": 9, "commits": 12 }
  ],
  "daily_commits": {
    "2025-01-01": 15,
    "2025-01-02": 3
  }
}
```

**Field Guide:**
- `day`: 0 (Sunday) to 6 (Saturday)
- `hour`: 0 to 23
- `daily_commits`: Map of "YYYY-MM-DD" strings to integer counts.
- `raw_data`: Aggregated commit counts per day-of-week/hour slot.

### 3. Generate Artifact
Pass the JSON data to the python rendering script.

**Command:**
```bash
# Via stdin
echo '{"component_name": "..."}' | python3 scripts/render_heatmap.py

# Or via temporary file
python3 scripts/render_heatmap.py data.json
```

The script will output the full `import React ...` source code.

### 4. Output
Save and present the generated JSX content. This component is self-contained and includes:
- Interactive Heatmap (Day x Hour)
- Annual Contribution Graph
- Statistics & Insights
- "Share on Slack" functionality (generates Block Kit JSON)

## Usage Example

**User:** "Analyze recent activity for @username"

**Agent Actions:**
1.  **SQL**: 
    - Query `daily_commits` (sum commits per date).
    - Query `raw_data` (bucket commits by day-of-week and hour).
2.  **Processing**: 
    - The SQL output already contains the aggregated data. Simply format it into the required JSON structure.
3.  **JSON Construction**: Create the JSON payload.
4.  **Render**: Run `python3 scripts/render_heatmap.py` with the payload.
5.  **Result**: Create a new file `ActivityHeatmap.jsx` with the script output and show it to the user.