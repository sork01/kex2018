import re
import requests
import urllib.request
import html

acronym = ''
lookup = 'kuk'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
get = requests.get('https://www.acronymfinder.com/' + str(lookup) + '.html', headers=headers , timeout=0.75)
html.unescape(get)
response = re.findall(r'goog_search\(\'([^\']+)', get.content.decode('utf-8'))
for i in range(3):
    acronym += response[i].replace('+', ' ')
    acronym += '\n'
print(acronym)
