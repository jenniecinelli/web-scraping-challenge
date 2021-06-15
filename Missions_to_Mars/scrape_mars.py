from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
	
	executable_path = {'executable_path': ChromeDriverManager().install()}
	return Browser("chrome", **executable_path, headless=False)
	
mars_data = {}

def scrape_info():

    browser = init_browser()

    time.sleep(1)

    url_news='https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html = browser.html
    soup = bs(html, "html.parser")
    

# Mars News
    titles = []
    paragraphs = []
    links = []

    results = soup.find_all('div', class_='slide')
    for result in results:
      titles.append(result.find('div', class_="content_title").text)
      paragraphs.append(result.find('div', class_='rollover_description_inner').text)
      links.append("https://mars.nasa.gov" + result.a['href'])

    mars_data['news_title'] = titles[0]
    mars_data['news_paragraph'] = paragraphs[0]
    mars_data['news_url'] = links[0]
    

# # Space Image
    url_image = 'https://spaceimages-mars.com/'
    browser.visit(url_image)
    image_html = browser.html
    image_soup = bs(image_html, "html.parser")

    results = image_soup.find_all(class_="floating_text_area") 

    for result in results:  
        try:
            featured = result.a['href']
            featured_image_url = "https://spaceimages-mars.com/" + featured
        
        except AttributeError as e:
            print(e)

    mars_data['featured_image'] = featured_image_url

# Facts
    url_facts = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_facts)
    df = tables[0]

    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    mars_data['facts'] = html_table

# Hemispheres
    url_hem = 'https://marshemispheres.com/'
    browser.visit(url_hem)

    hemisphere_image_urls = []
    browser.click_link_by_partial_text('Cerberus')
    html = browser.html
    soup = bs(html, 'html.parser')

    cerberus_title = soup.find('h2', class_="title").text
    cerberus_img_url = soup.find(class_="downloads").a['href']

    dict_1 = {"title":cerberus_title, "img_url": 'https://marshemispheres.com/' + cerberus_img_url}
    hemisphere_image_urls.append(dict_1)

    browser.back()

    browser.click_link_by_partial_text('Schiaparelli')

    html = browser.html
    soup = bs(html, 'html.parser')

    schiaparelli_title = soup.find('h2', class_="title").text
    schiaparelli_img_url = soup.find(class_="downloads").a['href']

    dict_2 = {"title":schiaparelli_title, "img_url": 'https://marshemispheres.com/' +  schiaparelli_img_url}
    hemisphere_image_urls.append(dict_2)

    browser.back()

    browser.click_link_by_partial_text('Syrtis Major')

    html = browser.html
    soup = bs(html, 'html.parser')

    syrtis_major_title = soup.find('h2', class_="title").text
    syrtis_major_img_url = soup.find(class_="downloads").a['href']

    dict_3 = {"title":syrtis_major_title, "img_url": 'https://marshemispheres.com/' +  syrtis_major_img_url}
    hemisphere_image_urls.append(dict_3)

    browser.back()
    browser.click_link_by_partial_text('Valles Marineris')

    html = browser.html
    soup = bs(html, 'html.parser')

    valles_marineris_title = soup.find('h2', class_="title").text
    valles_marineris_img_url = soup.find(class_="downloads").a['href']

    dict_4 = {"title":valles_marineris_title, "img_url": 'https://marshemispheres.com/' +  valles_marineris_img_url}
    hemisphere_image_urls.append(dict_4)

    mars_data['hemisphere_data'] = hemisphere_image_urls

    browser.quit()

    return mars_data