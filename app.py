from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('url_shortener.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT NOT NULL, short_url TEXT NOT NULL)''')
conn.commit()
conn.close()

# generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

# insert a new URL into the database
def insert_url(long_url, short_url):
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_url))
    conn.commit()
    conn.close()

# Function to get the long URL from the short URL
def get_long_url(short_url):
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_url=?", (short_url,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_url = generate_short_url()
    insert_url(long_url, short_url)
    return render_template('shortened.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
