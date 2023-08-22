from flask import Flask, render_template, flash, redirect, url_for
from datascrapper import NewsScraper  # Import your NewsScraper class

app = Flask(__name__)

db_url = "sqlite:///news_database.db"
scraper = NewsScraper(base_url="https://www.mubasher.info/markets/TDWL/stocks/4190/news", total_pages=1, db_url=db_url)
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
