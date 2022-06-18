#lesson 10.3.3
# Import Splinter, BeautifulSoup, and Pandas
from tkinter import font
from matplotlib import font_manager
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


#10.5.3 add a function to intialize the browser

def scrape_all():
    #initiate headlessdriver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    #we initiall set headless to false so we can test now set to true bc not testing
    browser = Browser('chrome', **executable_path, headless = True)

    #set variables
    news_title, news_paragraph = mars_news(browser)

    data ={
        'news_title' : news_title,
        'news_paragraph' : news_paragraph,
        'featured_image': featured_image(browser),
        'mars_hemisphere': mars_hemi(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }
        
    #quit the browser-- important step because if not it will keep listening for instructions
    browser.quit() 
    return data 


#10.5.2 adding a mars news scrape function
def mars_news(browser):
    #visit the mars nasa news site
    url = 'http://redplanetscience.com/'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    #convert the browser html to a soup object and then quit
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try and except
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #use the parent element to find the first 'a' tag and save it as news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to find text
          #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
       return None, None

    return news_title, news_p


# # 10.3.4 scrape the image
# ###  Featured images

#update featured image with a function

def featured_image(browser):
    #visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)  

    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #find the relative image url
         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    #use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

#add a mars facts function

def mars_facts():
#add try and except for error handling
    try:
        #use the read_html to scrape into df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    
    #assign columns and set index 
    #assign columns and set index
    
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True) 
  

    #convert dataframe into html format, add bootstrap
    return df.to_html()

#create variable for hemisphere urls outside of the function so it can be 
#used in scrape all


def mars_hemi(browser):
    hemi_image_urls =[]
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    #optional delay for browser
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    mars_hemi_site = browser.find_by_css('a.product-item img')
# 3. Write code to retrieve the image urls and titles for each hemisphere.

    for click in range(len(mars_hemi_site)):
        try: 
            hemi = {}
            #find each hemi link
            browser.find_by_css('a.product-item img')[click].click()
            #get the image 
            hemi['img_url'] = browser.find_by_text("Sample")['href']  
            #get the title
            hemi['title'] = browser.find_by_css('h2.title').text  
            ## append to list
            hemi_image_urls.append(hemi)
            #go back to site
            browser.back()
        except AttributeError:
            return None, None 
    return hemi_image_urls



if __name__== "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())



