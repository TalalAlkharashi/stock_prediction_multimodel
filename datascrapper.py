from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class NewsArticle(Base):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    tag = Column(String, nullable=False)

class NewsScraper:
    def __init__(self, base_url, total_pages, driver_path='chromedriver.exe', db_url='sqlite:///news_database.db'):
        self.base_url = base_url
        self.total_pages = total_pages
        self.driver_path = driver_path
        self.db_url = db_url
        self.driver = None
        self.engine = None
        self.Session = None

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Set headless mode
        self.driver = webdriver.Chrome(self.driver_path, options=chrome_options)

    def initialize_db(self):
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def close_resources(self):
        if self.driver:
            self.driver.quit()

    def scrape_data(self):
        self.initialize_driver()
        self.initialize_db()

        for page_num in range(1, self.total_pages + 1):
            page_url = f"{self.base_url}{page_num}"
            self.retry_load_page(page_url)

            self.driver.implicitly_wait(10)

            articles = self.driver.find_elements(By.CLASS_NAME, "mi-article-media-block__content")
            for article in articles:
                title_element = article.find_element(By.CLASS_NAME, "mi-article-media-block__title")
                title = title_element.text.strip()

                date_element = article.find_element(By.CLASS_NAME, "mi-article-media-block__date")
                date = date_element.text.strip()

                tag_elements = article.find_elements(By.CLASS_NAME, "label")
                tag = tag_elements[0].text.strip() if tag_elements else "N/A"

                self.save_to_db(title, date, tag)

            print(f"Page {page_num}/{self.total_pages} done")

        self.close_resources()

    def retry_load_page(self, page_url, max_retries=3):
        for retry in range(max_retries):
            try:
                self.driver.get(page_url)
                break
            except WebDriverException as e:
                if retry == max_retries - 1:
                    raise e
                print(f"Retry {retry + 1}/{max_retries} due to: {e}")
            time.sleep(3)

    def save_to_db(self, title, date, tag):
        session = self.Session()
        news_article = NewsArticle(title=title, date=datetime.strptime(date, '%d/%m/%Y %I:%M %p'), tag=tag)
        session.add(news_article)
        session.commit()
        session.close()

# Instantiate the class and use it
base_url = "https://www.mubasher.info/news/sa/pulse/stocks/"
total_pages = 219
db_url = "sqlite:///news_database.db"
scraper = NewsScraper(base_url, total_pages, db_url=db_url)
scraper.scrape_data()
