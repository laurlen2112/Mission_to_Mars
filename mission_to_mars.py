#!/usr/bin/env python
# coding: utf-8

# In[25]:


#lesson 10.3.3
#import splinter and BS
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#import pandas
import pandas as pd

#set executeable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)


#visit mars nasa site
url = 'https://redplanetscience.com'
browser.visit(url)

#optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time = 1)


#set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


#begin scraping
slide_elem.find('div', class_='content_title')


#use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


#use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # 10.3.4 scrape the image
# ###  Featured images

#visit url
url = 'https://spaceimages-mars.com'
browser.visit(url)

#find and click the full image button
full_image_elem =browser.find_by_tag('button')[1]
full_image_elem.click()


#parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

#find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


#use the base url to create an absolute url
img_url = f'http://spaceimages-mars/{img_url_rel}'
img_url


#10.3.5 scrape mars facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace = True)
df


df.to_html()

#quit the browser-- important step because if not it will keep listening for instructions
browser.quit()





