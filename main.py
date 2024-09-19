import sys
from bs4 import BeautifulSoup


class BookDepositoryTest:

    def __init__(self, name="BookDepositoryTest"):
        self.results = []

    def parse(self, soup):

        book_items = soup.find_all("div", class_="book-item")

        for book_item in book_items:

            url = book_item.find("div", class_="item-info").find("a")["href"]
            title = book_item.find("h3", class_="title").find("a").text.strip()

            price_tag = book_item.find("p", class_="price")
            if price_tag:
                spans = price_tag.findAll("span")

                if len(spans) > 2:
                    price = float(spans[2].text.strip("€").strip(" ").replace(",", "."))
            else:
                price = "No price present"

            low_price = float(
                book_item.find("div", class_="price-wrap omnibus")
                .find("span")
                .text.strip()
                .strip("€")
                .strip(" ")
                .replace(",", ".")
            )

            rating = book_item.find("div", class_="stars")

            if rating:
                full_stars = rating.findAll("span", class_="star full-star")
                full_star_count = len(full_stars)
            else:
                full_star_count = 0

            category = book_item.parent.parent.parent.parent.parent.find(
                "div", class_="block-header"
            ).h2.text.strip()

            row = {
                "url": url,
                "title": title,
                "price": price,
                "low_price": low_price,
                "rating": full_star_count,
                "category": category,
            }

            self.results.append(row)

        return self.results


class BooksToScrapeTest:

    def __init__(self, name="BooksToScrapeTest"):
        self.results = []

    def parse(self, soup):

        books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in books:

            url = book.find("a")["href"]
            title = book.find("h3").text.strip()
            price = float(book.find("p", class_="price_color").text.strip("£"))
            rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}[
                book.find("p", class_="star-rating")["class"][1]
            ]

            stock = (
                1
                if "In stock"
                in book.find("p", class_="instock availability").text.strip()
                else 0
            )

            row = {
                "url": url,
                "title": title,
                "price": price,
                "rating": rating,
                "stock": stock,
            }

            self.results.append(row)

        return self.results


class QuotesToScrapeTest:

    def __init__(self, name="QuotesToScrapeTest"):
        self.results = []

    def parse(self, soup):

        quote_divs = soup.find_all("div", class_="quote")

        for quote_div in quote_divs:
            url = [a["href"] for a in quote_div.find_all("a", href=True)][0]
            author = quote_div.find("small", class_="author").text.strip()
            quote = quote_div.find("span", class_="text").text.strip()
            tags = [tag.text for tag in quote_div.find_all("a", class_="tag")]

            row = {"url": url, "author": author, "quote_text": quote, "tags": tags}

            self.results.append(row)

        return self.results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid number of arguments.")
    if (
        sys.argv[1] != "book_depository_test.html"
        and sys.argv[1] != "books_to_scrape_test.html"
        and sys.argv[1] != "quotes_to_scrape_test.html"
    ):
        print("Unknown file.")

    else:
        file_name = sys.argv[1]
        with open(file_name, encoding="utf8") as fp:
            soup = BeautifulSoup(fp, "lxml")

            if file_name == "quotes_to_scrape_test.html":

                quotesToScrape = QuotesToScrapeTest()
                file_name = sys.argv[1]

                with open(file_name, encoding="utf8") as fp:
                    results = quotesToScrape.parse(soup)

                    for result in results:
                        print("Url:", result["url"])
                        print("Author:", result["author"])
                        print("Text:", result["quote_text"])
                        print("Tags:", ", ".join(result["tags"]))
                        print()

            if file_name == "books_to_scrape_test.html":

                booksToScrape = BooksToScrapeTest()
                file_name = sys.argv[1]

                with open(file_name, encoding="utf8") as fp:

                    results = booksToScrape.parse(soup)

                    for result in results:
                        print("Url:", result["url"])
                        print("Title:", result["title"])
                        print("Stock:", result["stock"])
                        print("Price:", result["price"])
                        print("Rating:", result["rating"])
                        print()

            if file_name == "book_depository_test.html":

                bookDepositoryTest = BookDepositoryTest()
                file_name = sys.argv[1]

                with open(file_name, encoding="utf8") as fp:

                    results = bookDepositoryTest.parse(soup)

                for result in results:

                    print("Url:", result["url"])
                    print("Title:", result["title"])
                    print("Price:", result["price"])
                    print("Low price:", result["low_price"])
                    print("Rating:", result["rating"])
                    print("Category:", result["category"])
                    print()
