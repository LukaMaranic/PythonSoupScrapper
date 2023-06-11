import sys
import re
from bs4 import BeautifulSoup
import pdb


class QuoteScraper:

    def __init__(self):
        self.results = []

    def parse(self, soup):
        quote_divs = soup.find_all('div', class_='quote')

        for quote_div in quote_divs:
            url = [a['href'] for a in quote_div.find_all('a', href=True)][0]
            author = quote_div.find('small', class_='author').text.strip()
            quote = quote_div.find('span', class_='text').text.strip()
            tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]

            row = {
                'url': url,
                'author': author,
                'quote_text': quote,
                'tags': tags
            }

            self.results.append(row)

        return self.results


class BookScraper:

    def __init__(self):
        self.results = []

    def parse(self, soup):
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

        for book in books:
            url = book.find('a')['href']
            title = book.find('h3').text
            price = float(book.find('p', class_='price_color').text.strip('£'))
            rating = len(book.find('p', class_='star-rating')['class']) - 1
            stock = 1 if book.find('p', class_='instock availability').text.strip() == 'In stock' else 0

            row = {
                'url': url,
                'title': title,
                'price': price,
                'rating': rating,
                'stock': stock
            }

            self.results.append(row)

        return self.results


class DepositoryScraper():
    def __init__(self):
        self.results = []

    def parse(self, soup):
        depository_div = soup.find('div', class_='page-slide')

        url_element = depository_div.find('a', class_='book-url')
        url = url_element['href'] if url_element else None

        title_element = depository_div.find('h2', class_='book-title')
        title = title_element.text.strip() if title_element else None

        stock_element = depository_div.find('span', class_='availability-message')
        stock = 1 if stock_element and stock_element.get_text(strip=True) == 'In stock' else 0

        price_element = depository_div.find('span', class_='sale-price')
        price = float(
            price_element.text.strip().replace('$', '').replace('€', '').replace(',', '.')) if price_element else None

        low_price_element = depository_div.find('span', class_='rrp')
        low_price = float(low_price_element.text.strip().replace('$', '').replace('€', '').replace(',',
                                                                                                   '.')) if low_price_element else price

        rating_element = depository_div.find('span', class_='rating')
        rating = float(rating_element['data-average-rating']) if rating_element else None

        category_element = soup.find('h1', class_='breadcrumb-item active')
        category = category_element.text.strip() if category_element else None

        row = {
            'url': url,
            'title': title,
            'price': price,
            'rating': rating,
            'low_price': low_price,
            'category': category,
            'stock': stock
        }

        self.results.append(row)

        return self.results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Invalid number of arguments.")
    else:
        if sys.argv[1] == "quotes_to_scrape_test.html":
            quotesToScrape = QuoteScraper()
            file_name = sys.argv[1]
            with open(file_name, encoding="utf8") as fp:

                soup = BeautifulSoup(fp, "lxml")
                results = quotesToScrape.parse(soup)

                for result in results:
                    print('Url:', result['url'])
                    print('Quote:', result['quote_text'])
                    print('Author:', result['author'])
                    print('Tags:', ', '.join(result['tags']))
                    print()

        if sys.argv[1] == "books_to_scrape_test.html":
            booksToScrape = BookScraper()
            file_name = sys.argv[1]

            with open(file_name, encoding="utf8") as fp:
                soup = BeautifulSoup(fp, "lxml")
                results = booksToScrape.parse(soup)

                for result in results:
                    print('Url:', result['url'])
                    print('Title:', result['title'])
                    print('Price:', result['price'])
                    print('Rating:', result['rating'])
                    print('Stock:', result['stock'])
                    print()

        if sys.argv[1] == "book_depository_test.html":

            depositoryScraper = DepositoryScraper()
            file_name = sys.argv[1]

            with open(file_name, encoding="utf8") as fp:
                soup = BeautifulSoup(fp, "lxml")
                results = depositoryScraper.parse(soup)

                for result in results:
                    print('Url:', result['url'])
                    print('Title:', result['title'])
                    print('Price:', result['price'])
                    print('Rating:', result['rating'])
                    print('Lowest Price:', result['low_price'])
                    print('Category:', result['category'])
                    print('Stock:', result['stock'])
                    print()
        else:
            print("File not found.")
