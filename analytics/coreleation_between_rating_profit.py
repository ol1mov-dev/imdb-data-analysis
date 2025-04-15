from db import conn, cursor
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

# SQL-запрос: Фильмы с рейтингом и доходом
query = """
SELECT 
    original_title,
    vote_average,
    revenue
FROM movies
ORDER BY vote_average DESC
LIMIT 500
"""

# Загружаем данные в DataFrame
df = pd.read_sql(query, conn)
conn.close()

# Построение графика: Диаграмма рассеяния для зависимости рейтинга и дохода
trace = go.Scatter(
    x=df['vote_average'],
    y=df['revenue'],
    mode='markers',
    marker=dict(
        color=df['vote_average'],  # Цвет маркеров зависит от рейтинга
 # Шкала цветов
        size=12,
        colorbar=dict(title="Рейтинг"),  # Подпись шкалы цвета
        line=dict(width=2, color='rgba(50, 171, 96, 1)'),
    ),
    hovertemplate='<b>%{text}</b><br>Рейтинг: %{x}<br>Доход: %{y}',
    text=df['original_title'],  # Названия фильмов для подсказок
)

# Оформление графика
layout = go.Layout(
    title='Связь между рейтингом и успехом фильма (доходом) на основе 500 фильмов',
    xaxis=dict(title='Рейтинг', range=[0, 10]),
    yaxis=dict(title='Доход (в миллионах)', automargin=True),
    height=800,
    showlegend=False,
)

# Создание фигуры и отображение графика
fig = go.Figure(data=[trace], layout=layout)
pyo.plot(fig, filename='html/rating_vs_success.html', auto_open=True)
