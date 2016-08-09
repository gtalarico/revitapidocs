from app import app

import os
files=[]
for filename in os.listdir('app/templates'):
    files.append('app/templates/' + filename)
for filename in os.listdir('app/templates/treeview'):
    files.append('app/templates/treeview/' + filename)
# print(files)
app.run(extra_files=files)
