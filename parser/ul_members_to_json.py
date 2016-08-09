from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json

FILE = 'app/templates/json/html/members_2017.html'
OUTFILE = 'app/templates/json/members_2017.json'
with open(FILE, 'r') as fp:
    content = fp.read()


soup = BeautifulSoup(content, 'html.parser')
ul = soup.ul
lis = OrderedDict()
for li in ul.find_all('li', recursive=False):
    result = OrderedDict()
    a = li.find('a')
    try:
        lis[a.text.strip()] = a['href']
        # result['name'] = a.text.strip()
    except:
        import pdb; pdb.set_trace()
    # result['href'] = a['href']
    # lis.append(result)

    # return result


# soup = BeautifulSoup(content, 'html5lib')
with open(OUTFILE, 'w') as fp:
    json.dump(lis, fp, indent=0)
# pprint(ul)
