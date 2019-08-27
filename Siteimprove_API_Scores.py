from datetime import date
import requests


proxyDict = {  # Proxy for requests (Does not work on corporate network so using proxy)
              'http': 'ENTER PROXY',
              'https': 'ENTER PROXY'
            }

user= 'ENTER EMAIL' #  email
api_key= 'ENTER API KEY'  # api key for password
webhook_url = 'ENTER WEBHOOK URL'  # Webhook URL

def get_score():
    #data = requests.get('https://api.siteimprove.com/v2/sites/5748934667/dci/overview', verify=False, auth=(user, api_key), proxies=proxyDict).json()
    #TotScore = data.get("accessibility").get("total")

    data = requests.get('https://api.siteimprove.com/v2/sites/5748934667/dci/overview?group_id=15588880510', verify=False, auth=(user, api_key), proxies=proxyDict).json()
    BellEN = data.get("accessibility").get("total")

    data = requests.get('https://api.siteimprove.com/v2/sites/5748934667/dci/overview?group_id=14635299164', verify=False, auth=(user, api_key), proxies=proxyDict).json()
    BellFR = data.get("accessibility").get("total")

    data = requests.get('https://api.siteimprove.com/v2/sites/8070332119/dci/overview', verify=False, auth=(user, api_key), proxies=proxyDict).json()
    SupEN = data.get("accessibility").get("total")

    data = requests.get('https://api.siteimprove.com/v2/sites/8072738471/dci/overview', verify=False, auth=(user, api_key), proxies=proxyDict).json()
    SupFR = data.get("accessibility").get("total")

    AvgScore = round (((BellEN + BellFR + SupEN + SupFR)/4),2)
    return AvgScore, BellEN, BellFR, SupEN, SupFR

def webhook(AvgScore, BellEN, BellFR, SupEN, SupFR, CurDate):

    payload = {
        'title': 'score',
        'text': ("The accessibility scores for " + CurDate + " are: "
                "\n\nAverage Score: " + str(AvgScore) +
                "\nShop EN: " + str(BellEN) +
                "\nShop FR: " + str(BellFR) +
                "\nSupport EN: " + str(SupEN) +
                "\nSupport FR: " + str(SupFR)),

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

    requests.packages.urllib3.disable_warnings()
    
    AvgScore, BellEN, BellFR, SupEN, SupFR = get_score()
    CurDate = get_date()
    webhook(AvgScore, BellEN, BellFR, SupEN, SupFR, CurDate)
