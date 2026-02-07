# CLAUDE.md

This file gives context to any Claude session working in this repo. Read this first.

## Who This Is For

Wes Brown - IT Business Systems Analyst transitioning into a more technical role. This portfolio exists to demonstrate real analytical thinking, SQL/Python chops, and the ability to bridge business questions with technical solutions. Not trying to cosplay as a senior data engineer. Just showing genuine technical ability and curiosity.

## What's In This Repo

Two projects, each designed to be built in phases so progress is incremental and nothing requires a marathon session.

### 1. `vikings-analytics/` - NFL Vikings Analytics
Analyzing Minnesota Vikings play-by-play data using the nflverse dataset. The goal is to ask interesting football questions and answer them with data.

**Data source:** nflverse (free, open NFL play-by-play data)
- Python package: `nfl_data_py` (pip install nfl_data_py)
- Docs: https://github.com/nflverse/nflverse-data
- This gives you every play from every NFL game with ~400 columns of detail

**Phases:**
1. **Data acquisition** - Pull play-by-play data using nfl_data_py, explore the columns, filter to Vikings games. Save to CSV/parquet for reuse.
2. **Load into SQL** - Create a PostgreSQL schema, load the data, build useful views.
3. **Analysis round 1** - Pick a question (4th down decisions, red zone efficiency, receiving breakdowns) and answer it with SQL + Python.
4. **Visualization** - Build charts/dashboards that tell the story. Can be Power BI, matplotlib, plotly - whatever fits.
5. **Write it up** - Update the project README with findings. Not a paper, just "here's what I asked, here's what the data said."

Each phase is a standalone commit. Don't try to do them all at once.

### 2. `nicotine-in-foods/` - Dietary Nicotine Exposure Analysis
Investigating naturally occurring nicotine in everyday foods (nightshade vegetables like tomatoes, potatoes, eggplant, peppers) and modeling what real dietary exposure looks like compared to smoking.

**Data sources:**
- USDA FoodData Central API (free, requires API key from https://fdc.nal.usda.gov/api-key-signup)
- Published research on nicotine content in nightshade vegetables (several peer-reviewed studies with measured concentrations)
- WHO/FDA reference data on nicotine absorption from tobacco

**Phases:**
1. **Research & data collection** - Gather nicotine concentration data from published studies. Pull nutritional data from USDA API for the relevant foods. Document sources.
2. **Build the dataset** - Combine research data with USDA nutritional profiles into a clean, structured dataset.
3. **Model exposure** - Calculate nicotine intake from common meals and daily diets. Compare to cigarette equivalents.
4. **Visualization** - Make it visual. "One plate of eggplant parm = X% of a cigarette" is the kind of output that makes people stop scrolling.
5. **Write it up** - Project README with methodology and findings.

Same deal - each phase is a commit. Small bites.

## Technical Stack

- **Python 3.12** - Data acquisition, cleaning, analysis (3.14 is too new, causes pip build failures)
- **PostgreSQL 18** - Data storage and SQL analysis (Vikings project primarily)
- **Power BI / matplotlib / plotly** - Visualization (choose per project)
- **Git/GitHub** - Version control with clean, meaningful commits
- **VS Code** - Primary IDE

## Current State

**Vikings Analytics (Complete + MCP Server):**
- Database: `vikings_analytics` (PostgreSQL, local)
- Tables: `plays` (38,869 play-by-play 1999-2025), `moss_1998_games` (Moss rookie season)
- Views: `fourth_down_plays`, `red_zone_plays`, `vikings_offense`
- Data sources: nflreadpy (play-by-play), Pro Football Reference (1998 supplemental)
- Seasons: Moss era (1999-2004, 2010) + Jefferson era (2020-2025) = 13 seasons
- Analysis: 4th down decision-making - found Vikings are conservative in red zone, kicking FGs 2.5x more than going for it on 4th-and-short
- Visualizations: Charts showing 4th down aggression by field position and red zone decisions
- MCP Server: Conversational query interface with access to both play-by-play and game stats
- Scripts: `pull_data.py`, `load_to_db.py`, `load_1998_stats.py`, `create_views.sql`, `analyze_fourth_down.py`, `visualize_fourth_down.py`, `mcp_server.py`

**Nicotine in Foods (Not started):**
- Phase 1 is research and data collection

## Git Guidance

Wes is leveling up on git. Key reminders:

- **Commit messages should say WHY, not WHAT.** Bad: "add files". Good: "pull 2024 Vikings play-by-play data for 4th down analysis"
- **Commit after each meaningful chunk of work.** Finished pulling data? Commit. Wrote a query that works? Commit. Don't wait until everything is done.
- **Never commit sensitive files.** API keys, .env files, virtual environments, IDE configs. The .gitignore handles most of this but double-check.
- **Use branches for experiments.** Want to try something risky? `git checkout -b experiment/whatever`. If it works, merge it. If not, delete the branch. Main stays clean.
- If Wes asks about a git operation he's unsure about, explain what the command does before running it.

## Session Notes

When helping Wes:
- He learns by doing, not by reading walls of text. Keep explanations short, then let him execute.
- Break work into small pieces. If a task has more than 3-4 steps, phase it.
- He'll have blockers - help him through them without just doing everything for him. Guide first, solve if he's stuck.
- Don't over-engineer anything. The goal is demonstrating competence, not building production systems.
- Be direct. He doesn't want sugarcoating.
