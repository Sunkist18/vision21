import os
import time

import qrcode
from selenium import webdriver
from selenium.common import exceptions
from pprint import pprint

total0 = 0
total = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe', options=chrome_options)


def scrape(url):
    driver.get(url)
    time.sleep(2.5)

    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    try:
        # Extract the elements storing the usernames and comments.
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    # print("> VIDEO TITLE: " + title + "\n")
    # print("> USERNAMES & COMMENTS:")

    return_comment = ''

    for username, comment in zip(username_elems, comment_elems):
        # print(username.text + ":")
        # print(comment.text + "\n")
        return_comment = comment.text
        break

    return title, return_comment


def isSkipValied(string):
    if len(string):
        if string[-1] == '/':
            string = string[:-1]
    return_value = []
    k = 'NULL'
    try:
        for part in string.split('/'):
            k = part
            time, num = part.split()[0], ' '.join(part.split()[1:])
            time = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
            return_value.append([num, str(time)])
    except Exception as e:
        print('인식할 수 없는 스킵 문자열이 있습니다')
        error_links.append(youtube_link)
        print(e)
        print(k)
    return return_value

error_links = []

if __name__ == '__main__':
    while True:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=0,
        )
        # print()
        youtube_link = input()

        if youtube_link == "total":
            print(total, 'QR Code from', total0, 'videos')
            pprint(error_links)
            continue
        
        if '&' in youtube_link:
            youtube_link = youtube_link[:youtube_link.index('&')]

        total0 += 1

        path, skip_str = scrape(youtube_link)
        skip_str = isSkipValied(skip_str)
        # path = ' '.join(path.split()[:-2])

        if not skip_str:
            print('NULL STRING')
            continue
        try:
            os.mkdir(path)
        except:
            pass
        count = 0
        for title, t in skip_str:
            count += 1
            qr.clear()
            qr.add_data(youtube_link + '&t=' + t)
            qr.make_image().save(path + '/' + '%03d' % count + '_' + title + '.png')
        # print('[QRCODE] Work complete with', len(skip_str), 'files.')
        total += len(skip_str)
