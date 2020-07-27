# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time



# Establish path
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():

    # Create dictionary for scraped data
    mars_data = {}

    # Define URL
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(5)
    html = browser.html

    # Extract html from URL
    soup = BeautifulSoup(html, 'html.parser')

    # Parse through html to return paragraph and title
    news_p = soup.find('ul', class_='item_list').\
    find('div', class_='article_teaser_body').text

    news_title = soup.find('ul', class_='item_list').\
    find('div', class_='content_title').text

    # Add info to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    # Define URL
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    time.sleep(5)
    html2 = browser.html

    # Extract html from URL
    soup2 = BeautifulSoup(html2, 'html.parser')

    # Parse through html to return image source
    link = soup2.find('div', class_='carousel_container').\
    find('div', class_='carousel_items').\
    find('article').get('style')

    link_update = link.split('(')
    link_new = link_update[1].split(')')
    link_transformed = link_new[0]

    link_transformed = link_transformed.replace('wallpaper', 'largesize')
    link_transformed = link_transformed.replace('-1920x1200', '_hires')
    link_transformed = link_transformed.replace("'", "")

    # Combine URL
    featured_image_url = 'https://www.jpl.nasa.gov' + link_transformed

    # Add info to dictionary
    mars_data['featured_image_url'] = featured_image_url

    # Define URL
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    time.sleep(5)
    html3 = browser.html

    # Extract html from URL
    soup3 = BeautifulSoup(html3, 'html.parser')

    # Parse through html to find first tweet
    mars_weather = soup3.find('div', lang='en').text

    # Add info to dictionary
    mars_data['mars_weather'] = mars_weather

    # Define URL
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)

    time.sleep(5)
    html4 = browser.html

    # Extract html from URL
    soup4 = BeautifulSoup(html4, 'html.parser')

    # Import pandas and structure table
    import pandas as pd

    tables = pd.read_html(url4)

    tables_df = pd.DataFrame(tables[0])

    # Structure Table
    tables_new_df = tables_df.rename(columns={0: "Description", 1: "Value"})

    # Structure Table
    transformed_df = tables_new_df.set_index("Description")
    mars_table = transformed_df.to_html(classes='marstable')
    mars_table = mars_table.replace('\n', ' ')

    # Add info to dictionary
    mars_data['mars_table'] = mars_table

    # Define URL
    pic1_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(pic1_url)

    # For loop
    mars_pics = []

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup_pic = BeautifulSoup(html, 'html.parser')
        partial = soup_pic.find("img", class_="wide-image").get('src')
        img_title = soup_pic.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        diction={"title":img_title,"img_url":img_url}
        mars_pics.append(diction)
        browser.back()
    

    mars_data['mars_pics'] = mars_pics

    return mars_data
    # print(mars_data)