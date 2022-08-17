from bs4 import BeautifulSoup
from selenium import webdriver 
from chromedriver_py import binary_path
import requests
import pandas as pd

english = []
japanese =[]
episodes = []
page_link=[]
score = []
ranks = []
popularity = []
release = []
genres = []

def get_genres(new_url_soup):
    temp_list = []
    for container in new_url_soup.find_all("span",itemprop = "genre"):
        temp_list.append(container.text)
    genres.append(temp_list)
        
def get_season(new_url_soup):
    container = new_url_soup.find("span",class_="information season") if new_url_soup.find("span",class_="information season") else '-'
    if container == "-":
        release.append(container)
    else:
        release.append(container.a.text)
        
def get_popularity(new_url_soup):
    container = new_url_soup.find("span", class_="numbers popularity") if new_url_soup.find("span", class_="numbers popularity") else '-'
    if container == "-":
        popularity.append(container)
    else:
        popularity.append(container.strong.text[1:])

def get_rank(new_url_soup):
    container = new_url_soup.find("div", class_="spaceit_pad po-r js-statistics-info di-ib", attrs = {'data-id': 'info2'}) if new_url_soup.find("div", class_="spaceit_pad po-r js-statistics-info di-ib", attrs = {'data-id': 'info2'}) else '-'
    if container == "-":
        ranks.append(container)
    else:
        ranks.append(container.text[12:-109])
        
def get_score(new_url_soup):
    container = new_url_soup.find("span", itemprop="ratingValue") if new_url_soup.find("span", itemprop="ratingValue") else '-'
    if container == "-":
        score.append(container)
    else:
        score.append(container.text)
        
def get_japanese_name(new_url_soup):
    container = new_url_soup.find("h1", class_="title-name h1_bold_none") if new_url_soup.find("h1", class_="title-name h1_bold_none") else '-'
    if container == "-":
        japanese.append(container)
    else:
        japanese.append(container.strong.text)

def get_episodes_count(soup):
    for container in soup.find_all("td", class_="data progress"):
        episodes.append(container.span.text)
    
def get_english_name(soup):
    for container in soup.find_all("td", class_="data title clearfix"):
        english.append(container.a.text)
    
def full_scraper(my_url):
    browser = webdriver.Chrome(executable_path=binary_path)   
    browser.get(my_url)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);") 
    html_source = browser.page_source 
    browser.close() 
    soup = BeautifulSoup(html_source, "html.parser")
    
    get_english_name(soup)
    
    get_episodes_count(soup)
    
    for new_url in soup.find_all("td", class_="data title clearfix"):
        hyperlink_url = "https://myanimelist.net" + new_url.a['href']
        page_link.append(hyperlink_url)
        second_html_source = requests.get(hyperlink_url)
        new_url_soup = BeautifulSoup(second_html_source.text, "html.parser")
        
        get_japanese_name(new_url_soup)
        
        get_score(new_url_soup)

        get_rank(new_url_soup)
        
        get_popularity(new_url_soup)
        
        get_genres(new_url_soup)
        
        get_season(new_url_soup)

    data = pd.DataFrame({
    'English Name': english,
    'Japanese Name': japanese,
    'Episode Count': episodes,
    'Score' : score,
    'Rank' :ranks,
    'Popularity': popularity,
    'Release Period': release,
    'Genres' : genres,
    'Anime link' : page_link,
    })
    data.index = data.index + 1
    
    data.to_csv('AnimeList.csv',encoding='utf-8') 

    print(data)

    
def main():
    username = input("Enter username\n")
    category = input("Enter \"All Anime\", \"Currently Watching\", \"Completed\", \"On Hold\", \"Dropped\", or \"Plan to Watch\"\n")
    if category.lower() == "all anime":
        status = "7"
    elif category.lower() == "currently watching":
        status = "1"
    elif category.lower() == "completed":
        status = "2"
    elif category.lower() == "on hold":
        status = "3"
    elif category.lower() == "dropped":
        status = "4"
    elif category.lower() == "plan to watch":
        status = "6"
    else:
        print("Error, exiting")
        exit()
        
    url = "https://myanimelist.net/animelist/" + username + "?status=" + status
    full_scraper(url)
    
if __name__ == "__main__":
    main()