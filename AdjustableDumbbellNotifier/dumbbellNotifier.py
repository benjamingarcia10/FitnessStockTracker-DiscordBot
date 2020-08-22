import requests
from bs4 import BeautifulSoup as soup

BOWFLEX_DUMBBELL_LINK = 'https://www.bowflex.com/selecttech/552/100131.html'
CHF_DUMBBELL_LINK = 'https://www.corehomefitness.com/products/chf-db1'


def check_bowflex_stock():
    print('Checking Bowflex SelectTech 552 Dumbbells Stock')
    response = requests.get(BOWFLEX_DUMBBELL_LINK)
    page_soup = soup(response.text, 'html.parser')
    add_to_cart_class_attributes = page_soup.find(id='add-to-cart').attrs['class']

    if 'add-to-cart-disabled' in add_to_cart_class_attributes:
        bowflex_available = False
        product_url = f'https://www.bowflex.com{page_soup.find(id="product-content").find("img")["src"]}'
        print(product_url)
        print('Bowflex SelectTech 552 Dumbbells Currently Unavailable.')
    else:
        bowflex_available = True
        print('Bowflex SelectTech 552 Dumbbells Currently Available.')


def check_chf_stock():
    pass


if __name__ == '__main__':
    check_bowflex_stock()
