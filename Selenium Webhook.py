from selenium import webdriver
import time
from datetime import date
import requests


proxyDict = {  # Proxy for requests (Does not work on corporate network so using proxy)
              'http': 'ENTER PROXY',
              'https': 'ENTER PROXY'
            }

def get_score(endpoint):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    s = webdriver.Chrome(executable_path="chromedriver.exe", options=options)  # Set up Selenium session

    s.get(endpoint)  # Get page
    s.find_element_by_id('Email').send_keys('ENTER EMAIL')  # Type in email
    s.find_element_by_class_name('btn-primary').click()  # Click submit
    s.find_element_by_id('Password').send_keys('ENTER PASSWORD')  # Type in password
    s.find_element_by_class_name('btn-primary').click()  # Click submit

    time.sleep(2)  # Sleep to load in score
    TotScore = s.find_element_by_xpath(
        '//*[@id="dynamic-dashboard"]/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/span[1]').text  # Get Score

    s.get('https://my2.siteimprove.com/Accessibility/624660/15588880510/Overview/Index')
    time.sleep(2)  # Sleep to load in score
    BellEN = s.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[1]').text  # Get Score

    s.get('https://my2.siteimprove.com/Accessibility/624660/14635299164/Overview/Index')
    time.sleep(2)  # Sleep to load in score
    BellFR = s.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[1]').text  # Get Score

    s.get('https://my2.siteimprove.com/Accessibility/812665/Overview/Index')
    time.sleep(2)  # Sleep to load in score
    SupEN = s.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[1]').text  # Get Score

    s.get('https://my2.siteimprove.com/Accessibility/818455/Overview/Index')
    time.sleep(2)  # Sleep to load in score
    SupFR = s.find_element_by_xpath(
        '//*[@id="content"]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[1]').text  # Get Score

    s.close()
    return TotScore, BellEN, BellFR, SupEN, SupFR

def webhook(TotScore, BellEN, BellFR, SupEN, SupFR, CurDate):
    webhook_url = 'ENTER WEBHOOK URL'  # change URL for your webhook

    payload = {
        'title': 'score',
        'text': ("The accessibility scores for " + CurDate + " are: "
                "\n\nTotal Score:" + TotScore +
                "\nShop EN:" + BellEN +
                "\nShop FR:" + BellFR +
                "\nSupport EN:" + SupEN +
                "\nSupport FR:" + SupFR),

        'username': 'Accessibility Bot',
        'icon_emoji': ':accessibility:'}  # custom emoji


    response = requests.post(webhook_url, json=payload, headers={'Content-Type': 'application/json'}, proxies=proxyDict)

    if response.status_code != 200:  # Check for errors, HTTP status 200 means OK
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )


def get_date():
    today = date.today()
    date2 = today.strftime("%B %d, %Y")

    return date2


if __name__ == "__main__":
    start = time.time()  # Calculate total execution time

    link = "https://my2.siteimprove.com/Dashboard/5765905975/5748934667/Dashboard/Index"

    TotScore, BellEN, BellFR, SupEN, SupFR = get_score(link)
    CurDate = get_date()
    webhook(TotScore, BellEN, BellFR, SupEN, SupFR, CurDate)

    end = time.time()
    print(end - start)
