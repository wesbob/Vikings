# Vikings Analytics

Analyzing Minnesota Vikings play-by-play data to answer real football questions with data.

## The Question

**Are the Vikings too conservative on 4th down, especially in scoring situations?**

Using three seasons of play-by-play data (2023-2025), I analyzed every 4th down decision to see how field position and game situation affect their go-for-it vs punt/kick choices.

## Findings

### 4th Down Decision-Making (2023-2025)

Analyzed 375 Vikings 4th down situations across three seasons to understand how aggressive the team is in different scenarios.

**Key Finding: Vikings play conservatively in the red zone**

When faced with 4th-and-short (1-3 yards) inside the opponent's 20-yard line, the Vikings kick field goals 2.5x more often than they go for it, despite being in prime scoring position.

![4th Down Aggression by Field Position](fourth_down_aggression.png)

The data shows the Vikings are least aggressive in the red zone (25.7% go-for-it rate), even though:
- They're close to the end zone
- Short-yardage situations have decent conversion odds
- A touchdown is worth more than a field goal

**Red Zone Conservatism**

On 4th-and-1, 4th-and-2, and 4th-and-3 inside the 20:
- **47 field goal attempts**
- **19 go-for-it attempts**
- 50% conversion rate when they do go for it (7 of 14 converted)

![Red Zone 4th Down Decisions](red_zone_fourth_down.png)

**What This Means**

The Vikings are leaving points on the table by prioritizing guaranteed field goals over potential touchdowns in high-value situations. Analytics-driven teams are more aggressive in these spots, treating 4th-and-short as an opportunity rather than a risk.

---

## Data Source

Play-by-play data from [nflverse](https://github.com/nflverse/nflverse-data) via the `nfl_data_py` Python package.

## Tech Stack

- **Python 3.12** - Data acquisition, analysis, visualization
- **PostgreSQL 18** - Data storage and SQL analysis
- **pandas** - Data manipulation
- **matplotlib** - Charts
- **SQLAlchemy** - Database connectivity

## Project Structure

```
vikings-analytics/
├── pull_data.py              # Download play-by-play data from nflverse
├── load_to_db.py             # Load data into PostgreSQL
├── create_views.sql          # Create analysis views
├── analyze_fourth_down.py    # Run 4th down analysis
├── visualize_fourth_down.py  # Generate charts
├── fourth_down_aggression.png
└── red_zone_fourth_down.png
```

## How to Run

1. **Pull data:**
   ```bash
   python pull_data.py
   ```

2. **Load into PostgreSQL:**
   ```bash
   POSTGRES_PASSWORD=yourpassword python load_to_db.py
   ```

3. **Create views:**
   ```bash
   psql -U postgres -d vikings_analytics -f create_views.sql
   ```

4. **Run analysis:**
   ```bash
   POSTGRES_PASSWORD=yourpassword python analyze_fourth_down.py
   ```

5. **Generate charts:**
   ```bash
   POSTGRES_PASSWORD=yourpassword python visualize_fourth_down.py
   ```

## Interactive Querying (MCP Server)

**Why build this?**

Static analysis answers specific questions, but I wanted to make the Vikings database *conversational*. Instead of writing SQL every time I have a question, I built an MCP (Model Context Protocol) server that lets me ask questions in plain English.

**How it works:**
1. Ask: "How often do the Vikings convert 4th-and-1 in the red zone?"
2. MCP server converts question → SQL query
3. Executes against PostgreSQL database
4. Returns results in natural language

This runs locally and integrates with Claude Desktop, turning three seasons of play-by-play data into an interactive knowledge base.

**Setup:**
- `mcp_server.py` - MCP server connecting to vikings_analytics database
- Configured in Claude Desktop settings for local use
