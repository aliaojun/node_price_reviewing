import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
import sqlite3

st.title('节点电价分析工具')

# 读取数据

TIME_COLUMNS = ['00:00','00:15','00:30','00:45','01:00','01:15','01:30','01:45','02:00','02:15','02:30','02:45','03:00','03:15','03:30','03:45','04:00','04:15','04:30','04:45','05:00','05:15','05:30','05:45',
                '06:00','06:15','06:30','06:45','07:00','07:15','07:30','07:45','08:00','08:15','08:30','08:45','09:00','09:15','09:30','09:45','10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45',
                '12:00','12:15','12:30','12:45','13:00','13:15','13:30','13:45','14:00','14:15','14:30','14:45','15:00','15:15','15:30','15:45','16:00','16:15','16:30','16:45','17:00','17:15','17:30','17:45',
                '18:00','18:15','18:30','18:45','19:00','19:15','19:30','19:45','20:00','20:15','20:30','20:45','21:00','21:15','21:30','21:45','22:00','22:15','22:30','22:45','23:00','23:15','23:30','23:45']

@st.cache_data
def load_initial_db():
    conn = sqlite3.connect('fulldata.db')
    # 读取2024-09-01的数据
    query = "select * from fulldata "
    data = pd.read_sql(query, conn)
    data = data.drop(columns=['index'])
    return data

def load_select_db(select_date):
    conn = sqlite3.connect('fulldata.db')
    # 读取2024-09-01的数据
    query = "select * from fulldata "+ "where 日期 = '"+select_date+"'"
    data = pd.read_sql(query, conn)
    data = data.drop(columns=['index'])
    return data



# create data view select box,if select all, then show all data, if select a datetime then show the data of the datetime

select_mode = st.selectbox('选择数据查看模式', ['查看所有数据', '查看指定日期数据'])
if select_mode == '查看所有数据':
    data = load_initial_db()
if select_mode == '查看指定日期数据':
    # create st select datetime slider
    select_date = st.date_input('选择日期', value=pd.to_datetime('2024-09-01'))
    select_date = select_date.strftime('%Y-%m-%d')
    #print(select_date)
    data = load_select_db(select_date)

data['mean_value'] = data[TIME_COLUMNS].mean(axis=1)
data['std_value'] = data[TIME_COLUMNS].std(axis=1)
DAY_MEAN = data['mean_value'].mean()
DAY_STD = data['std_value'].mean()
# return the data where the mean value is greater than the mean value + 3std_value (or less than) of the day
selected_data = data[ ( data['mean_value'] > DAY_MEAN + DAY_STD ) | ( data['mean_value'] < DAY_MEAN - DAY_STD ) ]

fig = go.Figure()
for i in range(len(selected_data)):
    fig.add_trace(go.Scatter(x=TIME_COLUMNS, y=selected_data.iloc[i][TIME_COLUMNS], mode='lines', name=selected_data.iloc[i]['节点名称']))

st.plotly_chart(fig)
