import os

from app import app

files = []
for filename in os.listdir('app/templates'):
    files.append('app/templates/' + filename)

for filename in os.listdir('app/static/css'):
    files.append('app/static/css/' + filename)

app.run(extra_files=files)
