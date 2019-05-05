# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:10:56 2019

@author: xiang
"""
    # Visit visitcostarica.herokuapp.com
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
import shutil


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":r"C:\Users\xiang\Desktop\webscraping_hw\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars = {}
def scrape():
    browser = init_browser()
    

    # Visit nasa.com
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)

    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #scraping title
    news_title = soup.find('div', class_='content_title').get_text()
    #print(news_title)

    #scraping paragraph
    news_paragraph = soup.find('div', class_="article_teaser_body").get_text()
    
    #add title and paragraph to the dictionary
    mars['news_title']= news_title
    mars['news_paragraph'] = news_paragraph 
    
    #Mars featured image url using bp
    #https://stackoverflow.com/questions/26895371/nameerror-name-requests-is-not-defined
    #url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url1=os.path.dirname('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    base_url = os.path.dirname(base_url1)
    base_url
    image_url='https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA19113'
    browser.visit(image_url)
    image_html = browser.html
    soup = bs(image_html, 'html.parser')
    time.sleep(2)
    featured_image_url=soup.find("img", class_="main_image")["src"]
    featured_image_url
    full_image_url = base_url+featured_image_url
    #add image url to the mars_data
    mars["featured_image_url"] = full_image_url
    
    #featured image
    response = requests.get(full_image_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    
    # Display the image with IPython.display
    from IPython.display import Image
    featured_image = Image(url='img.jpg')
    mars["featured_image"]=featured_image
    
    
    #Mars weather
    #weather'latest tweet 
    weather_url= "https://twitter.com/MarsWxReport/status/1124431254630404097"
    browser.visit(weather_url)
    weather_html = browser.html
    soup = bs(weather_html, 'html.parser')
    time.sleep(5)
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text").get_text()
    mars["mars_weather"] = mars_weather

    # Mars facts
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    featured_image_url= soup.find('img',class_= "carousel_item")
    #print(featured_image_url)
    
    # fact url
    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url)
    df= table[0]
    df.columns = ['Parameter', 'Value']
    df.set_index('Parameter', inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n','')
    mars["mars_table"] = html_table
    
    #Mars Hemisperes
    hemispheres_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(5)
    hemi_html=browser.html
    soup = bs(hemi_html, 'html.parser')
    time.sleep(5)
    hemi_base_url1=os.path.dirname('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    hemi_base_url = os.path.dirname(hemi_base_url1)
    hemi_base_url
        # scraping cerberus_img_rul
    img_urls=[]
    cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(cerberus_url)
    cerberus_image = browser.html
    soup = bs(cerberus_image, "html.parser")
    cerberus_img_url =soup.find("img", class_="wide-image")["src"]
    
    Cerberus = {"image_title": "Cerberus", "image_url": cerberus_img_url}
    img_urls.append(Cerberus)
    
    # scraping schiaparelli_img_rul
    schi_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(schi_url)
    schiaparelli_image = browser.html
    soup = bs(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    schiaparelli_img_url = hemi_base_url + schiaparelli_url
    
    Schiaparelli = {"image_title": "Schiaparelli", "image_url": schiaparelli_img_url}
    img_urls.append(Schiaparelli)
    
    # scraping syrtis_img_rul
    syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis_url)
    syrtis_image = browser.html
    soup = bs(syrtis_image, "html.parser")
    syrtis_url = soup.find("img", class_="wide-image")["src"]
    syrtis_img_url = hemi_base_url + syrtis_url
    
    Syrtis = {"image_title": "Syrtis", "image_url": syrtis_img_url}
    img_urls.append(Syrtis)
    
    # scraping valles_img_rul
    valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles_url)
    valles_image = browser.html
    soup = bs(valles_image, "html.parser")
    valles_url = soup.find("img", class_="wide-image")["src"]
    valles_img_url = hemi_base_url + valles_url
    
    Valles = {"image_title": "Valles", "image_url": valles_img_url}
    img_urls.append(Valles)
    
    mars["img_url"] = img_urls
    # Close the browser after scraping
    browser.quit()

    # Return the dictionary
    return mars


