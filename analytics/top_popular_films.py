from db import conn, cursor
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

# SQL-запрос: Топ-20 фильмов с наибольшим доходом и высоким рейтингом
query = """
SELECT 
    original_title,
    popularity
FROM movies
ORDER BY popularity DESC
LIMIT 20
"""

# Загружаем данные в DataFrame
df = pd.read_sql(query, conn)
conn.close()

# Сортировка по прибыли (по возрастанию)
df = df.sort_values(by='popularity')

# Создаём график
trace = go.Bar(
    x=df['original_title'],
    y=df['popularity'],
    marker=dict(color='#4A628A'),
    hovertemplate='<b>%{y}</b>'
)

layout = go.Layout(
    title='Топ-20 фильмов (по популярности)',
    xaxis=dict(title='Фильм'),
    yaxis=dict(title='Популярность', automargin=True),
    height=800
)

fig = go.Figure(data=[trace], layout=layout)


pyo.plot(fig, filename='html/top_popular_films.html', auto_open=True)
