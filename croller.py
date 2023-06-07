from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import pymysql
from selenium.webdriver.common.alert import Alert
import time
import pymysql
import random
# 각종 패키지 선언
# 개인적으로 크롤링 시에 사용하는 기본 스켈레톤 코드

# mysql 서버 접속하기
conn = pymysql.connect(host='localhost', user='root', password='root', charset='utf8', database='quake') 
cursor = conn.cursor() 

# 셀레니움 옵션 할당
option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
option.add_argument('user-agent=' + user_agent)
option.add_argument('disable-gpu')
option.add_argument('incognito')
option.add_argument('headless')
# 원래 셀레니움의 경우 경로를 할당해야 하지만 DRIVER_MANAGER 패키지를 통해서 자동 설치
# 별도로 변수로 경로 할당 필요 없음 ( 자동 할당 + 자동 설치 )
s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s, options=option)

# "DEV" 인 이유는 실제로 데이터 분석을 진행한 SERVICE 테이블과 달리 테스트 용도로 사용하기 적합
# AUTO_INCREMENTS 값에 의해서 영향을 받을 수 있음 ( EQ_COUNT )
sql = "INSERT INTO dev (eq_count, eq_date, eq_time, eq_level, eq_addr1, eq_addr2, eq_location) VALUES (NULL, %s, %s, %s, %s, %s, %s)" 
j = 1
while True:
    # 기상청 접속 후 데이터 가져오기
    url = f"https://www.weather.go.kr/w/eqk-vol/search/korea.do?startSize=1.0&endSize=999.0&pNo={j}&startLat=999.0&endLat=999.0&startLon=999.0&endLon=999.0&lat=999.0&lon=999.0&dist=999.0&keyword=&startTm=2018-12-11&endTm=2023-05-29&dpType=a"
    browser.get(url)
    # tbody select
    # LOCA 객체에 EXCEL_BODY 태그 할당
    loca = browser.find_element(By.CSS_SELECTOR, '#excel_body > tbody')
    # "TR" 태그를 가진 객체 찾아서 반복문 처리
    for i in loca.find_elements(By.TAG_NAME, 'tr'):
        # cursor.execute(sql, ())
        # 데이터 가져오기 ( 텍스트 )
        date = i.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span').text
        date = str(date).split(" ")
        eq_date = date[0]
        eq_time = date[1]
        # 데이터 분할
        eq_level = str(i.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span').text)
        eq_addr1 = i.find_element(By.CSS_SELECTOR, 'td:nth-child(6) > span').text
        eq_addr2 = i.find_element(By.CSS_SELECTOR, 'td:nth-child(7) > span').text
        eq_location = i.find_element(By.CSS_SELECTOR, 'td:nth-child(8) > span').text
        # 크롤링 상태 확인용 코드
        print({"j":j, "date": eq_date, "time":eq_time, "level":eq_level, "addr1":eq_addr1, "addr2":eq_addr2, "location":eq_location})
        cursor.execute(sql, (eq_date, eq_time, eq_level, eq_addr1, eq_addr2, eq_location))
        # SQL 명령어 실행으로 데이터 집어넣기
    # 커밋, 데이터 수정 완료 공지
    conn.commit() 
    try:
        # 의미 없는 값( PASS와 동일 )
        # 원래 EQ_COUNT의 값이었으나 AUTO_INCREMENTS로 데이터베이스 자체에서 대체
        j += 1
    except:
        break
conn.close() 
    
# while True:
#     pass