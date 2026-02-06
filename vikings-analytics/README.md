# Vikings Analytics

Analyzing Minnesota Vikings play-by-play data to answer real football questions with data.

## The Questions

*To be refined as I explore the data, but starting points:*

- How aggressive are the Vikings on 4th down compared to what the math says they should do?
- Where does the offense break down in the red zone?
- How do key receivers perform in different game situations (ahead, behind, close games)?

## Data Source

Play-by-play data from [nflverse](https://github.com/nflverse/nflverse-data) via the `nfl_data_py` Python package. Every play from every NFL game, ~400 columns of detail.

## Status

**Phase 1: Data Acquisition** - Complete  
**Phase 2: SQL Modeling** - Complete  
**Phase 3: Analysis** - Complete  
**Phase 4: Visualization** - Up Next


## Phases

1. **Data acquisition** - Pull and explore the play-by-play data, filter to Vikings
2. **SQL modeling** - Load into PostgreSQL, build useful views
3. **Analysis** - Dig into the questions above
4. **Visualization** - Charts and dashboards that tell the story
5. **Writeup** - Document findings here
