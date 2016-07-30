from bs4 import BeautifulSoup
import re
# FILE = 'RevitAPI.hhc'
FILE = 'RevitAPI.hhk'
OUTFILE = 'OUT-' + FILE
with open(FILE, 'r') as fp:
    content = fp.read()

soup = BeautifulSoup(content, 'html5lib')
# soup = BeautifulSoup(content, 'html.parser')

ul_tags = soup.find_all('ul')
for ul in ul_tags:
    li = ul.find('li')
    li.object.unwrap()
    if not li.contents:  # REMOVE EMPTY LI
        li.extract()     # REMOVE EMPTY LI
    import pdb; pdb.set_trace()
    param_tags = li.find_all('param')
    for param in param_tags:
        if param['name'] == 'Name':
            name = param['value']
        if param['name'] == 'Local':
            url = param['value']
    new_tag = soup.new_tag('a', href=url, **{'class':'api-link'})
    new_tag.string = name
    li.param.extract()
    li.param.extract()
    li.insert(0, new_tag)
    # print(new_tag)
print('Finished.')
#
with open(OUTFILE, 'w') as fp:
    fp.write(soup.prettify())

# print(soup.contents)

# START

# <UL>
#   <LI><OBJECT type="text/sitemap">
#     <param name="Name" value="BrowserOrganizationType Enumeration">
#     <param name="Local" value="html/87243309-4a1a-f50a-c787-a2fdbfa76785.htm">
#   </OBJECT></LI>
# </UL>

# NEW
# <li>
#  <a class="api-link" href="html/91957e18-2935-006c-83ab-3b5b9dbb5928.htm">
#   Autodesk.Revit.ApplicationServices Namespace
#  </a>
# </li>
