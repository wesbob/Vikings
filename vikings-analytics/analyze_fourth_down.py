import os
import pandas as pd
from sqlalchemy import create_engine, text

# Database connection
password = os.environ.get('POSTGRES_PASSWORD')
connection_string = f'postgresql://postgres:{password}@localhost:5432/vikings_analytics'
engine = create_engine(connection_string)

# Query: Overall 4th down decision breakdown
query = """
SELECT 
    play_type,
    COUNT(*) as total
FROM fourth_down_plays
WHERE posteam = 'MIN'
GROUP BY play_type
ORDER BY total DESC;
"""

df = pd.read_sql(text(query), engine.connect())
# print(df)

# Query 2: 4th down decisions by field position
query_field_position = """
SELECT 
    CASE 
        WHEN yardline_100 > 60 THEN 'Own territory'
        WHEN yardline_100 > 40 THEN 'Midfield'
        WHEN yardline_100 > 20 THEN 'Opponent territory'
        ELSE 'Red zone'
    END as field_position,
    COUNT(*) as total_4th_downs,
    SUM(CASE WHEN play_type IN ('pass', 'run') THEN 1 ELSE 0 END) as go_for_it,
    ROUND(100.0 * SUM(CASE WHEN play_type IN ('pass', 'run') THEN 1 ELSE 0 END) / COUNT(*), 1) as go_for_it_pct
FROM fourth_down_plays
WHERE posteam = 'MIN'
GROUP BY field_position
ORDER BY MIN(yardline_100) DESC;
"""

df_field_pos = pd.read_sql(text(query_field_position), engine.connect())
# print("\n=== 4th Down Aggression by Field Position ===")
# print(df_field_pos)


# Query 3: Red zone 4th-and-short (1-3 yards)
query_rz_short = """
SELECT 
    ydstogo,
    COUNT(*) as total,
    SUM(CASE WHEN play_type = 'field_goal' THEN 1 ELSE 0 END) as field_goals,
    SUM(CASE WHEN play_type IN ('pass', 'run') THEN 1 ELSE 0 END) as go_for_it,
    SUM(CASE WHEN fourth_down_converted = 1 THEN 1 ELSE 0 END) as converted
FROM fourth_down_plays
WHERE posteam = 'MIN' 
  AND yardline_100 <= 20 
  AND ydstogo <= 3
GROUP BY ydstogo
ORDER BY ydstogo;
"""

df_rz_short = pd.read_sql(text(query_rz_short), engine.connect())
# print("\n=== Red Zone 4th-and-Short (1-3 yards) ===")
# print(df_rz_short)


# === Analysis Summary ===
print("\n" + "="*50)
print("KEY FINDINGS")
print("="*50)

# Finding 1: Overall conservatism
total_4th = df['total'].sum()
print(f"\nTotal 4th down plays: {total_4th}")

# Finding 2: Red zone field goal preference
rz_fg_rate = (df_rz_short['field_goals'].sum() / df_rz_short['total'].sum()) * 100
print(f"Red zone 4th-and-short: {rz_fg_rate:.1f}% field goal attempts")

# Finding 3: Conversion rate when they DO go for it
total_attempts = df_rz_short['go_for_it'].sum()
total_converted = df_rz_short['converted'].sum()
conversion_rate = (total_converted / total_attempts) * 100 if total_attempts > 0 else 0
print(f"When they go for it in RZ 4th-and-short: {conversion_rate:.1f}% success rate ({total_converted}/{total_attempts})")
