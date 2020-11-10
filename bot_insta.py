# coding: utf-8
import os, json
import argparse
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def loadjsoncookie(jsoncookie, browser):
    with open(jsoncookie, 'r') as bloc:
        distros_dict = json.load(bloc)
    for i in range(0, len(distros_dict)):
        # print(distros_dict[i])
        browser.add_cookie(distros_dict[i])


def exportjsoncookie(filejson, browser):
    # print(browser.get_cookies())
    my_details = browser.get_cookies()
    with open(filejson, 'w') as json_file:
        json.dump(my_details, json_file, sort_keys=True, indent=4)


def click_element(valide):
    for v in valide:
        v.click()


def write_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_json(jsonload):
    with open(jsonload, 'r') as f:
        data = json.load(f)
        return data


def scrollPage(className):
    # Scroll page abonnée
    old_position = 0
    new_position = None
    while new_position != old_position:
        old_position = new_position
        sleep(1)
        # scroll
        browser.execute_script(
            "document.getElementsByClassName('" + className + "')[0].scrollTo(0, document.getElementsByClassName('" + className + "')[0].scrollHeight);")
        # new position
        new_position = browser.execute_script(
            "var lenOfPage=document.getElementsByClassName('" + className + "')[0].scrollHeight;return lenOfPage;")


def getNameFollow(mydivs):
    nb_follower = 0
    listAbonnee = []
    for link in mydivs:
        a = link.find_all('a')
        for name in a:
            title = name.get('title')
            if title != None:
                nb_follower += 1
                href = name.get('href')
                listAbonnee.append(href.replace('/', ''))
                print(href, title, nb_follower)
    return listAbonnee


if __name__ == "__main__":
    opts = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    opts.add_argument("user-agent=" + user_agent)

    # opts.add_argument('headless')
    browser = webdriver.Chrome(options=opts, executable_path='C:/chromedriver/chromedriver.exe')
    browser.get("http://www.example.com")

    # load the old cookie
    cookies = "coockies.json"
    #cookiesperso = "coockies.json"
    link = "https://www.instagram.com/?hl=fr"
    loadjsoncookie(cookies, browser)
    browser.get(link)
    sleep(2)  # time for charge the page

    # button activate notif
    btn_notif = browser.find_elements_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    click_element(btn_notif)  # click on the add element +
    sleep(2)

    # profile
    btn_profil = browser.find_elements_by_xpath('/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[1]/a')
    click_element(btn_profil)
    sleep(3)

    # abonnée
    btn_abonnee = browser.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
    click_element(btn_abonnee)
    sleep(2)

    # Scroll page abonnée
    scrollPage('isgrP')
    # get page Html after load
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    mydivs = soup.findAll("div", {"class": "PZuss"})

    listAbonnee = getNameFollow(mydivs)
    # click out de abonnement
    actions = ActionChains(browser)
    actions.move_by_offset(100, 100).click().perform()

    # Abonnement
    btn_abonnement = browser.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
    click_element(btn_abonnement)
    sleep(2)

    # Scroll page abonnée
    scrollPage('isgrP')
    # get page Html after load
    soup2 = BeautifulSoup(browser.page_source, 'html.parser')
    mydivs2 = soup2.findAll("div", {"class": "PZuss"})

    listAbonnement = getNameFollow(mydivs2)
    # click out de abonnement
    actions = ActionChains(browser)
    actions.move_by_offset(100, 100).click().perform()

    # get all not follower :
    not_follower = list(set(listAbonnement) - set(listAbonnee))
    write_json(not_follower, 'notfollower.json')
    sleep(60)  # time for charge the page
    # get new Cookies
    exportjsoncookie(cookies, browser)
    browser.quit()
