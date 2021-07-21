from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
 
path=r'C:\Users\t2001\Downloads\chromedriver_win32\chromedriver.exe'
browser=webdriver.Chrome(executable_path=path)

browser.get('https://www.youtube.com/')
time.sleep(15)

channel='Mahathalli'
search=browser.find_element_by_xpath('//*[@id="search"]')
search.click()
search.send_keys(channel)
search.send_keys(Keys.ENTER)

time.sleep(10)

ch=browser.find_element_by_xpath('//*[@id="main-link"]')
url=ch.get_attribute('href')

browser.get(url+'/videos')
time.sleep(10)

while True:
    scroll_height = 1000
    h1 = browser.execute_script("return document.documentElement.scrollHeight")
    browser.execute_script(f"window.scrollTo(0, {h1+scroll_height});")
    time.sleep(3)
    h2 = browser.execute_script("return document.documentElement.scrollHeight")
    if h1 == h2:
        break

pg=browser.page_source
soup=BeautifulSoup(pg,'lxml')
de=soup.findAll('a',{'id':"thumbnail"})

urls=[]

for i in de:
	u=i.get('href')
	try:
		urls.append('https://www.youtube.com'+u) #Since the fetched urls are not complete we need to append -https://www.youtube.com in front to fetch the complete url
	except:
		continue

name=[]
likes=[]
dislikes=[]
views=[]
date=[]

urls=urls[:5]

for i in urls:
	browser.get(i)
	time.sleep(10)
	
	name.append(browser.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text)

	pg=browser.page_source
	soup=BeautifulSoup(pg,'lxml')
	text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
	likes.append(text_yt_formatted_strings[0].attrs.get("aria-label"))
	dislikes.append(text_yt_formatted_strings[1].attrs.get("aria-label"))

	views.append(browser.find_element_by_xpath('//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text)
	date.append(browser.find_element_by_xpath('//*[@id="info-strings"]/yt-formatted-string').text)

data = {'Name of the video': name, 'URL': urls,'Number of likes':likes,'Number of dislikes':dislikes,'Views':views,'Release Date':date}  
df=pd.DataFrame(data)

df.to_csv("YouTube_data.csv")

print("Done !!")
browser.quit()

