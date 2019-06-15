import os
from flask import Flask, render_template, request, current_app
from flask_pager import Pager
import requests
import json
import sqlite3

my_url = "https://jobs.github.com/positions.json?description=python&full_time=true&location=sf"
content = requests.session()

text = json.loads(content.get(my_url).content)

some_data = []
some_data1 = []
some_data2 = []
for title in text:
    some_data.append(title['company_url'])
    some_data1.append(title['company'])
    some_data2.append(title['title'])

#print(some_data,some_data1,some_data2)

conn = sqlite3.connect('info.db')
c = conn.cursor()
c.execute("""CREATE TABLE oktable (first text, last text, post text)""")
params = (str(some_data), str(some_data1), str(some_data2))
c.execute(f"INSERT INTO oktable VALUES (?, ?, ?)", params)
conn.commit()
conn.close()


app = Flask(__name__)
app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 20
app.config['VISIBLE_PAGE_COUNT'] = 10


@app.route("/")
def index():
    page = int(request.args.get('page', 1))
    count = 40
    data = range(count)
    pager = Pager(page, count)
    pages = pager.get_pages()
    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = (data[skip: skip + limit], str(some_data1), str(some_data), str(some_data2))
    return render_template('index.html', pages=pages, data_to_show=data_to_show)

if __name__ == '__main__':

    app.run(debug=True)
