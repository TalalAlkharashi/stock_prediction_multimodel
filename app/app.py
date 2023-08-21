from flask import Flask, render_template, flash, redirect, url_for
from news_scraper import NewsScraper  # Import your NewsScraper class
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secret key

db_url = "sqlite:///news_database.db"
scraper = NewsScraper(base_url="https://www.mubasher.info/markets/TDWL/stocks/4190/news", total_pages=10, db_url=db_url)
scraper.initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape_data():
    try:
        scraper.scrape_data()
        flash("Data scraping and storage successful!", 'success')
    except Exception as e:
        flash("An error occurred during scraping: " + str(e), 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
