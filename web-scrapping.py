from bs4 import BeautifulSoup
import requests
import smtplib
import time
import yaml

credentials = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)

url = credentials['url']

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }


def check_price():
    pages = requests.get(url, headers=headers)
    soup = BeautifulSoup(pages.content, 'html.parser')
    # soup1 = BeautifulSoup(soup.prettify(), "html.parser")
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = price[2:len(price)]
    converted_price1 = converted_price.split(',')
    new_converted_price = ''
    for i in range(len(converted_price1)):
        new_converted_price += converted_price1[i]
    new_converted_price = float(new_converted_price)
    if new_converted_price < 100000:
        send_mail()
        print("Email has been sent")
    print(converted_price)


def send_mail():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(credentials['sender_email'], credentials['sender_email_password'])
        subject = 'Price Fell Down'
        body = 'Please visit the webiste '+url

        msg = "Subject:{}\n\n{}".format(subject, body)

        server.sendmail(credentials['sender_email'],
                        credentials['reciever_email'], msg)
        print('Email has been sent')
        server.quit()
    except Exception as e:
        print(e)


try:
    while True:
        check_price()
        time.sleep(60)
except KeyboardInterrupt:
    print('stopping')
