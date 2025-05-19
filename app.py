"""
9강: 데이터 시각화 I - 예제 코드
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib import font_manager

# 페이지 설정
st.set_page_config(page_title="날씨 데이터 시각화", layout="wide")
st.title("서울시 날씨 데이터 시각화")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('data/weather.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# NanumGothic 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = font_manager.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False

# 1. 월별 기온 변화 (선 그래프)
st.subheader("1. 월별 기온 변화")
fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(df['date'], df['temperature'], marker='o', linestyle='-', color='#b3b3b3')
ax1.set_xlabel('날짜', fontproperties=fontprop)
ax1.set_ylabel('기온, (°C)', fontproperties=fontprop)
ax1.set_title('2023 서울시 기온 변화', fontproperties=fontprop)
ax1.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45, fontproperties=fontprop)
st.pyplot(fig1)

# 2. 강수량 분포 (히스토그램)
st.subheader("2. 강수량 분포")
fig2, ax2 = plt.subplots(figsize=(10,6))
ax2.hist(df['precipitation'], bins=20, color='#40e0d0', alpha=0.7, edgecolor='black')
ax2.set_xlabel('강수량, (mm)', fontproperties=fontprop)
ax2.set_ylabel('빈도', fontproperties=fontprop)
ax2.set_title('2023 서울시 강수량 분포', fontproperties=fontprop)
ax2.grid(True, linestyle=':', alpha=0.5)
st.pyplot(fig2)

# 3. 기온과 습도의 관계 (산점도)
st.subheader("3. 기온과 습도의 관계")
fig3, ax3 = plt.subplots(figsize=(10,6))
scatter = ax3.scatter(df['temperature'], df['humidity'], c=df['precipitation'], cmap='cividis', alpha=0.7, s=100)
plt.colorbar(scatter, label='강수량, (mm)')
ax3.set_xlabel('기온, (°C)', fontproperties=fontprop)
ax3.set_ylabel('습도, (%)', fontproperties=fontprop)
ax3.set_title('기온과 습도의 관계', fontproperties=fontprop)
ax3.grid(True, linestyle=':', alpha=0.5)
st.pyplot(fig3)

# 4. 계절별 날씨 유형 (파이 차트)
st.subheader("4. 계절별 날씨 유형")

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return '겨울'
    elif month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    else:
        return '가을'

df['season'] = df['date'].apply(get_season)
weather_by_season = df.groupby(['season', 'weather_type']).size().unstack(fill_value=0).T

fig4, ((ax4_1, ax4_2), (ax4_3, ax4_4)) = plt.subplots(2, 2, figsize=(12, 8))
fig4.suptitle('계절별 날씨 유형 분포', fontproperties=fontprop)

colors = ['#FFC0CB', '#87CEEB', '#98FB98', '#DDA0DD']
for ax, season in zip([ax4_1, ax4_2, ax4_3, ax4_4], ['봄', '여름', '가을', '겨울']):
    ax.pie(weather_by_season[season], labels=weather_by_season.index,
           autopct='%1.1f%%', startangle=140, colors=colors,
           textprops={'fontproperties': fontprop})
    ax.set_title(season, fontproperties=fontprop)

st.pyplot(fig4)

# 5. 인터랙티브 그래프 선택
st.subheader("5. 인터랙티브 그래프 선택")

data_mapping = {
    "기온": "temperature",
    "강수량": "precipitation",
    "습도": "humidity"
}

col1, col2 = st.columns(2)

with col1:
    selected_data = st.selectbox("확인할 데이터", list(data_mapping.keys()))

with col2:
    chart_type = st.selectbox("그래프 유형", ["선 그래프", "히스토그램"])

fig5, ax5 = plt.subplots(figsize=(10,6))

if chart_type == "선 그래프":
    ax5.plot(df['date'], df[data_mapping[selected_data]], marker='o')
    ax5.set_xlabel('날짜', fontproperties=fontprop)
else:
    ax5.hist(df[data_mapping[selected_data]], bins=20, color='#40e0d0', alpha=0.7, edgecolor='black')
    ax5.set_xlabel(selected_data, fontproperties=fontprop)

ax5.set_ylabel(selected_data, fontproperties=fontprop)
ax5.set_title(f'{selected_data} 변화', fontproperties=fontprop)
ax5.grid(True, linestyle=':', alpha=0.5)
if chart_type == "선 그래프":
    plt.xticks(rotation=45, fontproperties=fontprop)
st.pyplot(fig5)

# 6. 원본 데이터 표시
st.subheader("6. 원본 데이터")
st.dataframe(df)
