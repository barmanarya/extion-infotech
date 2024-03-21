from flask import Flask, redirect, request
import sqlite3
import string
import random

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('urls.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY, long_url TEXT, short_code TEXT)''')
conn.commit()

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('long_url')
    if not long_url:
        return {'error': 'Missing long_url'}, 400

    # Check if the URL already exists in the database
    c.execute("SELECT short_code FROM urls WHERE long_url=?", (long_url,))
    existing_short_code = c.fetchone()
    if existing_short_code:
        return {'short_url': f'http://yourdomain.com/{existing_short_code[0]}'}

    # Generate a new short code
    short_code = generate_short_code()

    # Insert the new URL into the database
    c.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
    conn.commit()

    return {'short_url': f'http://yourdomain.com/{short_code}'}

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    # Retrieve the long URL associated with the short code
    c.execute("SELECT long_url FROM urls WHERE short_code=?", (short_code,))
    long_url = c.fetchone()
    if long_url:
        return redirect(long_url[0])
    else:
        return {'error': 'Short URL not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)
