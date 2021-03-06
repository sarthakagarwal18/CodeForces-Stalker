from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import time
import sys
import webbrowser


def tabulate_results(user_handle, user_title, user_rating, max_rating):

    table = []

    for i in range(len(user_handle)):

        entry = []
        entry.append(i+1)
        entry.append(user_handle[i])
        entry.append(user_title[i])
        entry.append(user_rating[i])
        entry.append(max_rating[i])
        table.append(entry)

    print(tabulate(table, headers=["Index", "Handle", "Title", "Rating", "Max Rating"]))


def get_response(url):
    try:
        source_code = requests.get(url, verify=False, timeout=240)
    except:
        time.sleep(5)
        source_code = requests.get(url, verify=False, timeout=240)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def read_file():
    fr = open('Friends.txt', 'r')
    text = fr.readlines()
    fr.close()
    return text


def populate():

    handles = read_file()

    user_handle = []
    user_title = []
    user_rating = []
    max_rating = []

    i = 0

    while i < len(handles):

        url = "http://codeforces.com/profile/" + handles[i]
        soup = get_response(url)

        link = soup.findAll('div', {'class': 'info'})
        for div in link:
            span = div.find_all('span')

        user_handle.append(handles[i])
        user_title.append(span[0].string)
        user_rating.append(span[1].string)
        max_rating.append(span[4].string)

        i += 1

    return user_handle, user_title, user_rating, max_rating


def main():

    user_handle, user_title, user_rating, max_rating = populate()

    tabulate_results(user_handle, user_title, user_rating, max_rating)

    index = int(input("Choose option: 1-"+str(len(user_handle)) + " to view profile OR press "+str(len(user_handle)+1)+" to exit : "))

    if index >= 1 and index <= len(user_handle):
        webbrowser.open("http://codeforces.com/profile/" + user_handle[index-1])
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
