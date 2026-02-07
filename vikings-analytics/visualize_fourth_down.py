import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

# Database connection
password = os.environ.get('POSTGRES_PASSWORD')
connection_string = f'postgresql://postgres:{password}@localhost:5432/vikings_analytics'
engine = create_engine(connection_string)

# Query: Field position aggression
query_field_pos = """
SELECT 
    CASE 
        WHEN yardline_100 > 60 THEN 'Own territory'
        WHEN yardline_100 > 40 THEN 'Midfield'
        WHEN yardline_100 > 20 THEN 'Opponent territory'
        ELSE 'Red zone'
    END as field_position,
    ROUND(100.0 * SUM(CASE WHEN play_type IN ('pass', 'run') THEN 1 ELSE 0 END) / COUNT(*), 1) as go_for_it_pct
FROM fourth_down_plays
WHERE posteam = 'MIN'
GROUP BY field_position
ORDER BY MIN(yardline_100) DESC;
"""

df = pd.read_sql(text(query_field_pos), con=engine.connect())
# print(df)

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(df['field_position'], df['go_for_it_pct'], color='#4C1D95')  # Vikings purple
plt.xlabel('Field Position', fontsize=12)
plt.ylabel('Go-For-It Rate (%)', fontsize=12)
plt.title('Vikings 4th Down Aggression by Field Position (2023-2025)', fontsize=14, fontweight='bold')
plt.ylim(0, 35)  # Set y-axis to show the full scale

# Add percentage labels on top of bars
for i, v in enumerate(df['go_for_it_pct']):
    plt.text(i, v + 1, f"{v}%", ha='center', fontsize=11)

plt.tight_layout()
plt.savefig('fourth_down_aggression.png', dpi=300, bbox_inches='tight')
print("\nChart saved: fourth_down_aggression.png")

# Query 2: Red zone 4th-and-short decisions
query_rz = """
SELECT 
    ydstogo,
    SUM(CASE WHEN play_type = 'field_goal' THEN 1 ELSE 0 END) as field_goals,
    SUM(CASE WHEN play_type IN ('pass', 'run') THEN 1 ELSE 0 END) as go_for_it
FROM fourth_down_plays
WHERE posteam = 'MIN' 
  AND yardline_100 <= 20 
  AND ydstogo <= 3
GROUP BY ydstogo
ORDER BY ydstogo;
"""

df_rz = pd.read_sql(text(query_rz), con=engine.connect())

# Create stacked bar chart
fig, ax = plt.subplots(figsize=(10, 6))

x = df_rz['ydstogo']
width = 0.6

ax.bar(x, df_rz['field_goals'], width, label='Field Goal', color='#FFC72C')  # Gold
ax.bar(x, df_rz['go_for_it'], width, bottom=df_rz['field_goals'], label='Go For It', color='#4C1D95')  # Purple

ax.set_xlabel('Yards to Go', fontsize=12)
ax.set_ylabel('Number of Plays', fontsize=12)
ax.set_title('Red Zone 4th Down Decisions: Field Goal vs Go For It (2023-2025)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['4th-and-1', '4th-and-2', '4th-and-3'])
ax.legend()

plt.tight_layout()
plt.savefig('red_zone_fourth_down.png', dpi=300, bbox_inches='tight')
print("Chart saved: red_zone_fourth_down.png")
