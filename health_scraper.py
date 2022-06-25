from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# token: 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
url = "https://www.health.kr/researchInfo/herbalMedicine2.asp"
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
driver.implicitly_wait(3)
line_xpath = '/html/body/section/section/section/article[2]/div[1]/a' # 줄 선택
line100_xpath = '/html/body/section/section/section/article[2]/div[1]/ul/li[6]/a' # 100줄 보기
detail_xpath = '/html/body/section/section/section/article[2]/table/tbody/tr[{0}]/td[1]/a' # 2 to 101

def scrape_name():
    find_all = soup.find_all('td')
    name = find_all[0].string.split()
    dictionary = {'국명':name[0], '한자명':name[1]}
    
    return dictionary

def scrape_content():
    tds = soup.find_all('td')
    contents = [t.text for t in tds]
    contents = contents[1:]
    
    ths = soup.find_all('th')
    index = [t.string.split() for t in ths]
    index = [''.join(t) for t in index if ''.join(t) != '處方名']
    
    dictionary = dict()
    for s in range(len(index)):
        dictionary[index[s]] = contents[s]
    
    return dictionary

def click_line100():
    driver.find_element("xpath", line_xpath).click()
    driver.implicitly_wait(2)
    driver.find_element("xpath", line100_xpath).click()
    driver.implicitly_wait(2)



try: 
    click_line100()

    df = pd.DataFrame()
    for i in range(2, 102):

        driver.find_element("xpath", detail_xpath.format(i)).click()
        driver.implicitly_wait(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        dictionary = scrape_name()
        content_dict = scrape_content()
        dictionary.update(content_dict)

        page_df = pd.DataFrame(dictionary, index=[0])
        df = df.append(page_df, ignore_index=True)

        driver.back()
        driver.implicitly_wait(2)
finally:
    driver.close()

df.to_csv('health_scraped.csv', encoding='utf-8-sig')

# version
# after 4.3.0
# find_element_by_xpath >> not working
# changed: find_element("xpath", 'path')