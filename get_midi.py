import re
import requests
import sys
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
DOMAIN = "https://bitmidi.com"
search_string = '+'.join(sys.argv[1:])

# Must entered interpret + song name
if search_string:
    print(">>>", search_string)
else:
    exit("You must enter INTERPRET - SONG NAME")

def download_file(link, filename):
    # Get download page
    mid_page = requests.get(DOMAIN + link, headers=headers)
    print(DOMAIN + link)
    parsed_page = BeautifulSoup(mid_page.content, 'html.parser')
    # Get link for download
    links = parsed_page.find_all('a', href=re.compile('uploads'))
    midi_link = links[0]['href']    
    mid_file = requests.get(DOMAIN + midi_link, headers=headers, stream=True)
    # Save midi
    with open(filename, 'wb') as save_midi:
        save_midi.write(mid_file.content)
        print('Downloaded {} successfully.'.format(filename))

url = DOMAIN + '/search?q=' + search_string
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
main_page = requests.get(url, headers=headers)
parsed_page = BeautifulSoup(main_page.content, 'html.parser')

links = parsed_page.find_all('a', href=re.compile('mid'))
link = links[0]['href']
file_name = links[0]['title']

print("DOMAIN NAME", DOMAIN + link)
print("FILE NAME", file_name)
download_file(link, file_name)