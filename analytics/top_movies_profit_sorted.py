from db import conn, cursor
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

query = """
SELECT 
    original_title,
    budget,
    revenue,
    (revenue - budget) AS profit,
    vote_average
FROM movies
WHERE vote_average >= 7.0 
ORDER BY revenue DESC
LIMIT 20
"""

df = pd.read_sql(query, conn)
conn.close()

# Добавляем расчетные колонки
df['roi'] = (df['profit'] / df['budget']) * 100  # Return on Investment
df['budget_millions'] = df['budget'] / 1_000_000
df['revenue_millions'] = df['revenue'] / 1_000_000
df['profit_millions'] = df['profit'] / 1_000_000

# Сортировка по убыванию прибыли
df = df.sort_values(by='profit_millions', ascending=True)

# Создание графика
trace = go.Bar(
    x=df['profit_millions'],
    y=df['original_title'],
    orientation='h',
    marker=dict(color='#006A71'),
    hovertemplate='<b>%{y}</b><br>Прибыль: %{x:.2f} млн $<extra></extra>'
)
layout = go.Layout(
    title='Топ-20 прибыльных фильмов (по прибыли)',
    xaxis=dict(title='Прибыль (млн $)'),
    yaxis=dict(
        title='Фильм',
        automargin=True
    ),
    height=600
)

fig = go.Figure(data=[trace], layout=layout)

# Сохраняем как HTML
pyo.plot(fig, filename='html/top_movies_profit_sorted.html', auto_open=True)