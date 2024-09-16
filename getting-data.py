# %%

import requests
from bs4 import BeautifulSoup
import bs4 as bs
import regex as re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle

# %%

# input the following depending on the forum you want to scrape
url = '' 
forum_name = ''

# %%

options = webdriver.ChromeOptions()
# arguments to use the Chrome webdriver
options.add_argument('--incognito')  # use an incognito browser instance
options.add_argument('--headless')   # operate in headless mode; don't physically open a new window
options.add_argument('--no-sandbox') # very complicated but necessary to make this run; see https://www.google.com/googlebooks/chrome/med_26.html
# executable path points to your downloaded webdriver, mine is at the top level of the directory and called 'chromedriver'
driver = webdriver.Chrome(
    executable_path='./chromedriver', options=options)
driver.get(url)
# driver.get(url) opens the page
# the following two are to see if it works properly:
page = driver.execute_script('return document.body.innerHTML')
soup = bs.BeautifulSoup(''.join(page), 'html.parser')
# join() is a string method in python that joins all elements of an iterable (in this case page) by a separator (in this case a space)

# %%

# function will make your webdriver scroll down the page. takes as arguments your driver name and a legnth of time to wait in between each iteration of scroll.

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    count=0
    while True:

        # telling the driver to scroll to the pixel with zeroeth horizontal (leftmost) position and at the bottom of the current page (scroll height)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        # giving it time to load by waiting for the inputted duration of time
        # if there isn't a timeout, the body height will always be the same as the previous iteration since nothing new loaded
        time.sleep(scroll_pause_time)

        # assigning the new scroll height to new_height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height==new_height: break

        last_height=new_height

        count+=1
        if count==100 : break


# this function gets all the links on a single page source.
def all_links(url):

    # driver.implicitly_wait(30)  means  if the driver takes more than 30 seconds in trying to execute a task, then it stops
    driver.implicitly_wait(30)
    # driver.get(url) opens the page
    driver.get(url)

    # when you input url into driver.get(url), it’s assumed that url is the domain of the URL, therefore some links that are outputted will start with what comes right after the domain since the domain is implied
    # in other words, the domain (the url that you input) might be cut off, therefore resulting in the output of the rest of the URL
    # in this case, https://forum.fractalfuture.net is cut off from the topic links (the ones with /t/) that lead to posts


    # setting scroll_pause_time to 1 second
    scroll(driver,1)


    # driver.page_source are the contents of page driver is currrently on
    soup_a = bs.BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup_a.prettify())


    # Then we close the driver after we capture the page source with variable soup_a
    driver.close()

    # # Empty array to store the links, can you rewrite as a comprehension?
    # links = []
    # # Looping through all the a elements in the page source
    # for link in soup_a.find_all('a'):
    #     # link.get('href') gets the href/url out of the a element
    #     links.append(link.get('href'))

    links=[link.get('href') for link in soup_a.find_all('a')] #==links

    return links


links = all_links(url)
print(links)

# %%

# only topic links
links = [i for i in links if re.search(r'^/t/', str(i))]
print(links)

# %%

# remove slightly different URLs that lead to different places of same post page
links2=[m for m in links if len(re.findall('/', m))==3]
print(len(links2))

# %%

# remove duplicate links
links3=list(set(links2))
print(len(links3))
# By comparing the lengths, it reveals that the only duplicate is the one at the beginning since the total difference is 1

# %%

final_links=links3

# adding url domain to topic links
final_links = [url + i for i in final_links]

# %%

with open('forum_links.data', 'wb') as filehandle:
    pickle.dump(final_links, filehandle)

# %%

with open('forum_links.data', 'rb') as filehandle:
    final_links = pickle.load(filehandle)

# %%

# Format for scraping individual post
# Make sure to substitute URL with actual URL

page = requests.get("URL")

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

soup.find('div', class_='post').get_text()

# %%

page = requests.get("https://forum.fractalfuture.net/")

soup = BeautifulSoup(page.content, 'html.parser')

alist=soup.find_all('a')

# el1=soup.find_all('a')[0]
# print('yes') if str(el1).find("/t/") != -1 else print('no')

tlist=[el for el in alist if str(el).find("/t/") != -1]

# print(tlist)

# the following is specific to Fractal website:
# removing the first four /t/ :
# If you don't want the website's pinned post, then change the range to 5
for i in range(4) :
    tlist.remove(tlist[0])

# print(tlist)


# print(tlist[0].get('href'))
turllist=[tel.get('href') for tel in tlist]

# %%

# This is what is gonna be used generically for discourse sites once you've used the webdriver to retrieve the full list of URLs
# You will input that list to the function textspitlist

def textspit(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    if soup.find('div', class_='post') == None : return('')
    else : return(soup.find('div', class_='post').get_text())



def textspitlist(url_list):
    return([textspit(i) for i in url_list])



final_posts_text = textspitlist(final_links)

# %%

with open(forum_name + '_posts_text.data', 'wb') as filehandle:
    pickle.dump(final_posts_text, filehandle)

# %%

# remove defective links that resulted in [] as the post text

with open('cartalk_posts_text.data', 'rb') as filehandle:
    cartalk_posts_text = pickle.load(filehandle)

print(len(cartalk_posts_text))
cartalk_posts_text_shortened=[i for i in cartalk_posts_text if i!=[]]
print(len(cartalk_posts_text_shortened))

print(cartalk_posts_text_shortened)

with open('cartalk_posts_text_shortened.data', 'wb') as filehandle:
    pickle.dump(cartalk_posts_text_shortened, filehandle)

# %%

with open(forum_name + '_posts_text.data', 'rb') as filehandle:
    forum_text = pickle.load(filehandle)

# %%

with open('cartalk_posts_text.data', 'rb') as filehandle:
    cartalk_posts_text = pickle.load(filehandle)

with open('fractalfuture_posts_text.data', 'rb') as filehandle:
    fractalfuture_posts_text = pickle.load(filehandle)

with open('realtimevfx_posts_text.data', 'rb') as filehandle:
    realtimevfx_posts_text = pickle.load(filehandle)

with open('secops_posts_text.data', 'rb') as filehandle:
    secops_posts_text = pickle.load(filehandle)

with open('swapd_posts_text.data', 'rb') as filehandle:
    swapd_posts_text = pickle.load(filehandle)


all_forums_posts_text = cartalk_posts_text + fractalfuture_posts_text + realtimevfx_posts_text + secops_posts_text + swapd_posts_text


with open('all_forums_posts_text.data', 'wb') as filehandle:
    pickle.dump(all_forums_posts_text, filehandle)
