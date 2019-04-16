from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    #set url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find headline and teaser text
    headline = soup.find("div", class_="content_title").text
    teaser = soup.find("div", class_="article_teaser_body").text
    
    ########
    #set url
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find full-sized featured image
    featured_img = soup.find("footer")
    featured_img = featured_img.find("a")["data-fancybox-href"]
    featured_img = "https://www.jpl.nasa.gov" + featured_img
    
    ########
    #set url
    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find weather data
    weather = soup.find("p", class_="tweet-text").text

    ########
    #set url
    url="https://space-facts.com/mars/"

    #scrape table with pandas
    tables = pd.read_html(url)
    mars_df = tables[0]
    #set index
    mars_df = mars_df.set_index(0)

    #convert to html
    mars_table = mars_df.to_html(header=False)
    mars_table = mars_table.replace('\n', '')

    ########
    #set url
    url="http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find hemisphere titles 
    h3s = soup.find_all("h3")
    hemispheres = [result.text[:-9] for result in h3s]

    #set empty list for hemisphere imgs
    hemisphere_imgs = []

    for hemisphere in hemispheres:
        #click hemisphere link
        browser.click_link_by_partial_text(hemisphere)

        time.sleep(1)

        #scrape page into soup 
        html = browser.html
        soup = bs(html, 'html.parser')

        #find hemisphere image
        hemisphere_img = soup.find("div", class_="downloads")
        hemisphere_img = hemisphere_img.find("a")["href"]
        #append img to list
        hemipshere_imgs = hemisphere_imgs.append(hemisphere_img)

        #rest url
        url="http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)

    #create dict of hemisphere info
    hemisphere_df = pd.DataFrame({"img_url": hemisphere_imgs, "title": hemispheres})
    hemisphere_dict = hemisphere_df.to_dict("records")

    ########
    #set url
    url = "https://www.google.com/search?q=mars"
    browser.visit(url)

    time.sleep(1)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find summary
    summary = soup.find("div", class_ = "SALvLe farUxc mJ2Mod")
    summary = summary.find("span").text
    summary

    #create dict of all mars info
    mars_data = {
        "headline": headline, 
        "teaser": teaser,
        "feat_img": featured_img, 
        "weather": weather, 
        "facts": mars_table, 
        "hemispheres": hemisphere_dict,
        "summary": summary
    }

    #close the browser after scraping
    browser.quit()

    #return results
    return mars_data