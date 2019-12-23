from splinter import Browser
from bs4 import BeautifulSoup 
import pandas as pd
import time

def scrape_info():
    browser= Browser("chrome")
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    soup = BeautifulSoup(browser.html,"html.parser")

    result=soup.find('div',class_="content_title")
    title=result.a.text
    title

    results = soup.find('div',class_="article_teaser_body")
    body=results.text
    body

    mars={}
    mars["news_title"]=title
    mars["news_paragraph"]=body

    browser= Browser("chrome")
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    click_image=browser.find_by_id("full_image")
    click_image.click()
    time.sleep(2)
    links_found1 = browser.find_link_by_partial_text('more info')
    links_found1.click()
    time.sleep(2)
    soup = BeautifulSoup(browser.html,"html.parser")
    result=soup.find('figure',class_="lede")
    featured_image_url="https://www.jpl.nasa.gov"+result.a.img["src"]
    featured_image_url

    mars['featured_image_url']=featured_image_url

    browser= Browser("chrome")
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    soup = BeautifulSoup(browser.html,"html.parser")

    results = soup.find('div',class_="js-tweet-text-container")
    tweet=results.p.text
    tweet

    mars['weather']=tweet

    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    mars['facts']=df.to_html()

    browser= Browser("chrome")
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    soup = BeautifulSoup(browser.html,"html.parser")
    hemisphere_image_urls=[]
    hemisphere = {}
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        hemisphere = {}
        # We have to find the elements
        browser.find_by_css("a.product-item h3")[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get Hem title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hem object to list
        hemisphere_image_urls.append(hemisphere)
        # backwards
        browser.back()

    mars['hemisphere']=hemisphere_image_urls
    hemisphere_image_urls
        
    return mars
if __name__ == "__main__":
    print(scrape_info())