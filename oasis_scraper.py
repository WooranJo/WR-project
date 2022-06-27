# OASIS 전통의학 정보포털 약재백과
# https://oasis.kiom.re.kr/oasis/herb/monoSearch.jsp?srch_menu_nix=87Z2RM16

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

url = "https://oasis.kiom.re.kr/oasis/herb/monoSearch.jsp?srch_menu_nix=87Z2RM16"
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)

# 상세보기 xpath
detail_xpath = '/html/body/div/div/section/form/ul[{0}]/li[{1}]/a'
# 약성클릭 xpath
nature_xpath1 = '/html/body/div/div/nav/div/div/div/div[1]/ul/li/ul/li[2]/a'
nature_xpath2 = '/html/body/div/div/nav/div/div/ul/li/ul/li[2]/a'
 

def click_inside(ul, li):
    try: 
        driver.find_element_by_xpath(detail_xpath.format(ul, li)).click() # 상세보기 클릭
        driver.implicitly_wait(2)
        driver.find_element_by_xpath(nature_xpath1).click() # 약성 클릭1
        
    except:
        driver.find_element_by_xpath(nature_xpath2).click() # 약성 클릭2
        

def scrape():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 약초 한글명, 한자명, 학명 긁기
    title = soup.find_all('h2', class_='title')
    name = title[0].string.split(',')
    dictionary = {'국명':name[0], '한자명':name[1], '학명':name[2]}  # dictionary에 저장 (dataframe에 넣기 위해서)
    
    tds = soup.find_all('td') # table에 있는 정보
    texts = [t.text.strip() for t in tds if t.text.strip() and not t.text.strip().isdigit()] # 공백, 숫자로만 이루어진 스트링 빼고 담기
    texts = texts[0:13] # 필요한 정보만 자르기
    
    contents = dict()
    for s in range(len(texts)-1): # {index:content}로 저장
        if s%2==0:
            contents[texts[s]] = texts[s+1]
    contents["인경"] = texts[-1]
    
    dictionary.update(contents) # name, contents dictionary 합치기
    page_df = pd.DataFrame(dictionary, index=[0]) # 한글명, 한자명, 학명, 효능 기타등등 dataframe 넣기!
    return dictionary # 약초 하나에 대한 정보가 담긴 dataframe 반환

def backward(n,sec): # 뒤로가기. n = 뒤로 갈 횟수, sec = 기다릴 시간(단위: 초)
    for i in range(n):
        driver.back()
        driver.implicitly_wait(sec)


df = pd.DataFrame()
try: # table 구조 ==> 4x16
    for i in range(1, 17): 
        for j in range(1, 5):
            click_inside(i, j) # 클릭해서 들어가기
            driver.implicitly_wait(2) # 가취가욥~~!!
            dictionary = scrape() # 데이터 긁어와서 dictionary에 저장
            
            df = df.append(dictionary, ignore_index=True) # 최종 df에 append
            
            backward(2, 2) # 뒤로가기 (첫페이지로 이동)

finally: # 오류나거나 작업 완료시 창 닫고 csv 저장
    driver.close()
    df.to_csv('OASIS_ㄱ.csv', encoding='utf-8-sig') # 한글, 한자 깨짐 없이 저장
# 반드시 오류나 나는 구조.. 마지막 행이 3개로 이루어져서 i=16에 j=4가 없음. 오류 발생 == 작업완료
