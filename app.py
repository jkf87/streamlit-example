"""
9강: 데이터 시각화 I - 예제 코드
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="날씨 데이터 시각화", layout="wide")
st.title("서울시 날씨 데이터 시각화")

# 데이터 로드
@st.cache_data #파이썬에서 @는 데코레이터라고 부른다. 데코레이터는 함수에 기능을 추가하는 기능이다. st.cache_data는 데이터를 캐시에 저장하는 기능이다.
def load_data():
    df = pd.read_csv('data/weather.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()


# 한글 깨짐 수정을 위해 matplotlib 폰트 지정하기
plt.rcParams['font.family'] = 'AppleGothic'  # Mac OS용 한글 폰트 , 윈도우는 Malgun Gothic
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 기호 깨짐 방지

# 1. 월별 기온 변화 (선 그래프)
st.subheader("1. 월별 기온 변화")
fig1, ax1 = plt.subplots(figsize=(10,6)) #fig1은 전체 그래프를 관리하는 Figure 객체 10*6 크기, ax1은 실제로 그래프를 그리는 Axes 객체를 받음  

ax1.plot(df['date'], df['temperature'], marker='o', linestyle='-', color='#b3b3b3')

# 축 레이블 설정
ax1.set_xlabel('날짜')
ax1.set_ylabel('기온, (°C)')
ax1.set_title('2023 서울시 기온 변화') 

ax1.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
st.pyplot(fig1)



# 2. 강수량 분포 (히스토그램)
st.subheader("2. 강수량 분포")
fig2, ax2 = plt.subplots(figsize=(10,6))
ax2.hist(df['precipitation'], bins=20, color='#40e0d0', alpha=0.7, edgecolor='black')

# 가로 세로 레이블 , 제목, 그리드 설정
ax2.set_xlabel('강수량, (mm)')
ax2.set_ylabel('빈도')
ax2.set_title('2023 서울시 강수량 분포')
ax2.grid(True, linestyle=':', alpha=0.5)
st.pyplot(fig2)

# 3. 기온과 습도의 관계 (산점도)
st.subheader("3. 기온과 습도의 관계")
fig3, ax3 = plt.subplots(figsize=(10,6))

scatter = ax3.scatter(df['temperature'], df['humidity'], c=df['precipitation'], cmap='cividis', alpha=0.7, s=100) # cmap은 색상 맵을 지정하는 옵션 viridis는 디폴트 색상 맵, yl0rRd는 빨간색과 초록색의 조합, 그 외 많은 색상 맵이 있음 , s는 점의 크기 , 투명도
plt.colorbar(scatter, label='강수량, (mm)', ax=ax3) # 색상 바를 추가
ax3.set_xlabel('기온, (°C)')
ax3.set_ylabel('습도, (%)')
ax3.set_title('기온과 습도의 관계')
ax3.grid(True, linestyle=':', alpha=0.5)
st.pyplot(fig3)


# 4. 계절별 날씨 유형 (파이 차트)
st.subheader("4. 계절별 날씨 유형")
#데이터 전처리하기
# 계절 먼저 정의하기(봄 3-5월, 여름 6-8월, 가을 9-11월, 겨울 12-2월)

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return '겨울'
    elif month in [3,4,5]:
        return '봄'
    elif month in [6,7,8]:
        return '여름'
    else:
        return '가을'

df['season'] = df['date'].apply(get_season) # 계절 데이터를 추가해준다.

# groupby를 이용해서 계절별 날씨 유형 데이터 추출
weather_by_season = df.groupby(['season', 'weather_type']).size().unstack(fill_value=0).T  # 계절별 날씨 유형 데이터 추출, unstack은 데이터를 컬럼으로 변환하는 기능, fill_value=0은 빈 값을 0으로 채워준다. .T는 데이터를 전치하는 기능

# 4개의 서브플롯 생성
fig4, ((ax4_1, ax4_2), (ax4_3, ax4_4)) = plt.subplots(2,2, figsize=(12,8)) # 2,2형태의 서브플롯 생성

fig4.suptitle('계절별 날씨 유형 분포')

# 계절별 파이 차트 그리기
ax4_1.pie(weather_by_season['봄'], labels=weather_by_season.index, autopct='%1.1f%%', startangle=140, colors=['#FFC0CB', '#87CEEB', '#98FB98', '#DDA0DD']) # autopct는 퍼센트 표시 
ax4_1.set_title('봄')

ax4_2.pie(weather_by_season['여름'], labels=weather_by_season.index, autopct='%1.1f%%', startangle=140, colors=['#FFC0CB', '#87CEEB', '#98FB98', '#DDA0DD']) # autopct는 퍼센트 표시 
ax4_2.set_title('여름')

ax4_3.pie(weather_by_season['가을'], labels=weather_by_season.index, autopct='%1.1f%%', startangle=140, colors=['#FFC0CB', '#87CEEB', '#98FB98', '#DDA0DD']) # autopct는 퍼센트 표시 
ax4_3.set_title('가을')

ax4_4.pie(weather_by_season['겨울'], labels=weather_by_season.index, autopct='%1.1f%%', startangle=140, colors=['#FFC0CB', '#87CEEB', '#98FB98', '#DDA0DD']) # autopct는 퍼센트 표시 
ax4_4.set_title('겨울')

st.pyplot(fig4)


# 5. 인터랙티브 그래프 선택
st.subheader("5. 인터랙티브 그래프 선택")

# 한글-영문 컬럼명 매핑 딕셔너리
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
else:
    ax5.hist(df[data_mapping[selected_data]], bins=20, color='#40e0d0', alpha=0.7, edgecolor='black')

ax5.set_xlabel('날짜' if chart_type == "선 그래프" else selected_data)
ax5.set_ylabel(selected_data)
ax5.set_title(f'{selected_data} 변화')
ax5.grid(True, linestyle=':', alpha=0.5)
if chart_type == "선 그래프":
    plt.xticks(rotation=45)
st.pyplot(fig5)


# 6. 데이터 테이블 표시
st.subheader("6. 원본 데이터")
st.dataframe(df)


# 데이터 테이블 표시
st.subheader("6. 원본 데이터")
st.dataframe(df)
