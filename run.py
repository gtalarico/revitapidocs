import os

from app import app

files = []
for filename in os.listdir('app/templates'):
    files.append('app/templates/' + filename)

app.run(extra_files=files)
