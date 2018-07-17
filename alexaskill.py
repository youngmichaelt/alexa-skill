from flask_ask import Ask, statement, question, session
from flask import Flask
import json
import requests
import time
import unidecode
from requests import get
import pandas as pd
from bs4 import BeautifulSoup
from random import randint, randrange


app = Flask(__name__)
ask = Ask(app, "/KnowMore")


def get_article():
    #download article
    
    url = 'http://www.todayifoundout.com/index.php/2009/12/click-to-go-to-a-random-interesting-fact-article/'

    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    title = html_soup.find('h2', class_='post-title').text
    
    text = html_soup.find('div', class_='pf-content')

    text = text.find_all('p', recursive=False)

    paragraphs = []
    
    i = 0
    number = len(text)-1
    while i < number:
      
        paragraph = text[i].text
        paragraphs.append(paragraph)
        i+=1

    #preprocess text
    paragraphs = ''.join(paragraphs)
    
    
    paragraphs = paragraphs.replace(u'\xa0', u' ')
    paragraphs = paragraphs.replace('If you liked this article, you might also enjoy our new popular podcast, The BrainFood Show (iTunes, Spotify, Google Play Music, Feed), as well as:', ' ')
    paragraphs = paragraphs.replace('Bonus Facts:', ' ')
    paragraphs = paragraphs.replace('.', '. ')
    paragraphs = paragraphs.replace(',', ', ')
    paragraphs = paragraphs.replace('?', '? ')
    space = '.....'
    space2 = '....'
    paragraphs = ''.join((title, space, space2 , paragraphs))
    
    return paragraphs

get_article()  
p = get_article()


    
    
    

@app.route('/')
def homepage():
    return 'KnowMore'

@ask.launch
def start_skill():
    welcome_message = 'Welcome! Would you like to listen to an article?'
##    article = get_article()
    article_msg = p
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
##    article = get_article()
    message = 'This article is called...'
    article_msg = p
    time.sleep(5)
    return statement(message, p)

@ask.intent('NoIntent')
def no_intent():
    bye_text = 'Okay, have a great day!'
    return statement(bye_text)

    

if __name__ == '__main__':
    app.run()
