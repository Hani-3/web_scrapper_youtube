from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen 
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from flask import Flask
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['POST' , 'GET'])
def youtube():
    try:
        driver = webdriver.Chrome()  # to initialize chrome driver
        d=driver.get("https://www.youtube.com/@PW-Foundation/videos") # geting url 
        youtubePage = driver.page_source  # get website page
        youtube_html = bs(youtubePage, "html.parser") # beautify text using BeautifulSoup library
        video_details = youtube_html.find_all('div', {'class': "style-scope ytd-rich-grid-media"}) # find class from inspect of website
        video_details = youtube_html.select(".style-scope ytd-rich-grid-media")
        reviews = []
        with open('data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write the header row
            writer.writerow(["Video_URL", "Thumbnail", "Title", "Views", "Posting_Time"])
            for i in range(5): # Loop for first five video
                video = video_details[i]
                try:
                    video_class=video.select('a')
                    for j in video_class: # loop to get url link from 'a class'
                        video_url = j.get('href') # get herf link feom 'a' class
                except:
                    logging.info("video_url")
                    
                try:
                    full_video_url = "https://www.youtube.com" + video_url
                    geturl = requests.get(full_video_url)
                    video_html = bs(geturl.text, 'html.parser')
                    data=video_html.find('meta', property='og:image')['content']
                except:
                    logging.info("data")
                    
                try:
                    title_class=video.select('a')
                    for j in title_class: # loop to get url link from 'a class'
                        title = j.get('title') # get herf link feom 'a' class
                except:
                    logging.info("title")
                    
                try:
                    views = video.find_all("span","inline-metadata-item style-scope ytd-video-meta-block")
                    views = views[0].getText()
                except:
                    logging.info("views")
                    
                try: 
                    posting_time = video.find_all("span","inline-metadata-item style-scope ytd-video-meta-block")
                    posting_time = posting_time[1].getText()
                except:
                    logging.info("posting_time")

                my_dict = {"full_video_url": full_video_url, "data": data, "title": title, "views": views, "posting_time": posting_time}

                # Append the details to the list
                reviews.append(my_dict)

             # Write the details to the CSV file
            writer.writerows(reviews)
    
    except Exception as e:
            logging.info(e)
            return 'something is wrong'

    return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])

if __name__=="__main__":
    app.run()