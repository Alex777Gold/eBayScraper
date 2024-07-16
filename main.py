import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json


class eBayScraper:
    def __init__(self, url):
        self.url = url

    async def fetch_html(self):
        # Asynchronously fetch HTML content from the specified URL
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.text()

    async def extract_data(self):
        html = await self.fetch_html()
        soup = BeautifulSoup(html, 'html.parser')

        # Finding title
        h1_element = soup.find('h1', class_='x-item-title__mainTitle')
        title = h1_element.find(
            'span', class_='ux-textspans ux-textspans--BOLD').get_text(strip=True) if h1_element else None

        # Finding image
        div_element = soup.find('div', class_='ux-image-carousel-item')
        image_url = div_element.find('img').get(
            'data-zoom-src') if div_element else None

        # Finding price
        div_element = soup.find('div', class_='x-price-primary')
        price = div_element.find(
            'span', class_='ux-textspans').get_text(strip=True) if div_element else None

        # Finding seller info
        div_element = soup.find(
            'div', class_='x-sellercard-atf__info__about-seller')
        seller = div_element.find(
            'span', class_='ux-textspans ux-textspans--BOLD').get_text(strip=True) if div_element else None

        # Finding shipping cost
        div_element = soup.find(
            'div', class_='ux-labels-values__values-content')
        shipping_cost = div_element.find(
            'span', class_='ux-textspans').get_text(strip=True) if div_element else None

        # Construct JSON object
        data = {
            'title': title,
            'image_url': image_url,
            'product_url': self.url,
            'price': price,
            'seller': seller,
            'shipping_price': shipping_cost
        }

        return data

    async def main(self):
        data = await self.extract_data()
        print(json.dumps(data, indent=2))


if __name__ == '__main__':
    # URL of the eBay product page to scrape
    url = 'https://www.ebay.com/itm/125780394294'
    # Create an instance of eBayScraper with the URL
    scraper = eBayScraper(url)
    # Run the main coroutine asynchronously using asyncio
    asyncio.run(scraper.main())
