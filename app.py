import streamlit as st
import pandas as pd
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

url = 'https://movie.naver.com/movie/point/af/list.naver'
webpage =  urlopen(url).read().decode()
nv =  bs(webpage, 'html.parser')
trs = nv.select('#old_content > table  tr')[1:]

#1. 비어 있는 데이터프레임을 만듬
df = pd.DataFrame(columns={'col1', 'col2', 'col3', 'col4', 'col5', 'col6'})

for item in trs :
  #2. 데이터프레임에 넣을 리스트 생성 (열의 개수만큼 항목을 가지는 리스트)
  lt = []
   
  #파싱
  tds = item.find_all('td')

  no = tds[0].text
  writer = tds[1].find('a').text
  em = tds[1].find('em').text
  netizen = tds[1].text.split('\n')[5:-2]
  netizen = ' '.join(netizen).strip()
  author = tds[2].text 

  #2 리스트에 추가
  lt.append(no)
  lt.append(writer)
  lt.append(em)
  lt.append(netizen)
  lt.append(author[:-8])
  lt.append(author[-8:])

  #3. 데이터프레임에 추가 
  #3-1. 인덱스값 생성
  idx = df.index.max()
  if np.isnan(idx) : idx = 0
  else : idx = idx + 1
  
  df.loc[idx] = lt
  print(lt)
  #print(f'{no}, {writer}, {em},{netizen}, {author[:-8]}, {author[-8:]}')
  
;

df.columns = ['번호', '영화명', '평점', '리부', '아이디', '작성일']

st.title('네이버 영화')
st.dataframe(df)