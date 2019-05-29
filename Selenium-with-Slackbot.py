from requestium import Session
import time
from datetime import date
import requests

def get_score(endpoint):
    s = Session(webdriver_path="chromedriver.exe", browser="chrome")  # Set up Selenium session
    s.driver.get(endpoint)  # Get page
    s.driver.find_element_by_id('Email').send_keys('wrichiek.kar@bell.ca')  # Type in email
    s.driver.find_element_by_xpath('//*[@id="main-wrap"]/div[1]/div/div/div[2]/form/div[2]/button').click()  # Click submit (Change xpath for diff page)
    s.driver.find_element_by_id('Password').send_keys('bell1234')  # Type in password
    s.driver.find_element_by_xpath('//*[@id="main-wrap"]/div[1]/div/div/div[2]/form/div[3]/button').click()  # Click submit (Change xpath for diff page)
    time.sleep(1)  # Sleep to load in score
    score = s.driver.find_element_by_xpath('//*[@id="dynamic-dashboard"]/div[3]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/span[1]').text  # Get Score

    return score

def webhook(score):
    webhook_url = 'https://hooks.slack.com/services/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'  # change URL for your webhook
    now = get_date()
    payload = {'text': "The accessibility score for " + now + " is: " + score}

    response = requests.post(webhook_url, json=payload, headers={'Content-Type': 'application/json'})

    if response.status_code != 200:  # Check for errors, HTTP status 200 means OK
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def get_date():
    today = date.today()
    date2 = today.strftime("%B %d, %Y")

    return date2

if(__name__ == "__main__"):
    start = time.time()  # Calculate total execution time
    link = "https://my2.siteimprove.com/Dashboard/5765905975/5748934667/Dashboard/Index"
    score = get_score(link)
    webhook(score)
    end = time.time()
    print(end - start)
