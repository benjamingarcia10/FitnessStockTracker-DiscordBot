import requests
import re
from uselessItems import useless_items
from bs4 import BeautifulSoup as soup
import json

from items import search_urls
import variables


def get_data_from_url(item_name):
    item_type = search_urls[item_name]['type']
    full_item_name = search_urls[item_name]['product_name']
    item_link = search_urls[item_name]['link']
    item_category = search_urls[item_name]['category']
    page_items = []

    response = requests.get(item_link)
    redirect_count = len(response.history)

    page_soup = soup(response.text, 'html.parser')

    if item_type == 'multi':
        grouped_items = page_soup.find_all(class_='grouped-item')
        for single_item in grouped_items:
            if full_item_name in useless_items:
                return
            new_item = {
                'name': try_except(lambda: single_item.find(class_='item-name').text.strip(), lambda: 'NOT FOUND'),
                'price': try_except(lambda: single_item.find(class_='price').text.strip(), lambda: 'NOT FOUND'),
                'in_stock': try_except(lambda: single_item.find(class_='bin-stock-availability').text.strip(),
                                       lambda: 'NOT FOUND')
            }
            page_items.append(new_item)
    elif item_type == 'bone':
        if redirect_count == 0:
            grouped_items = page_soup.find_all(class_='grouped-item')
            for single_item in grouped_items:
                if full_item_name in useless_items:
                    return
                new_item = {
                    'name': try_except(lambda: single_item.find(class_='item-name').text.strip(), lambda: 'NOT FOUND'),
                    'price': try_except(lambda: single_item.find(class_='price').text.strip(), lambda: 'NOT FOUND'),
                    'in_stock': try_except(lambda: single_item.find(class_='bin-stock-availability').text.strip(),
                                           lambda: 'NOT FOUND')
                }
                page_items.append(new_item)
        else:
            new_item = {
                'in_stock': 'Notify Me'
            }
            page_items.append(new_item)
    elif item_type == 'grab bag':
        if redirect_count == 0:
            page_items = get_data_from_js(page_soup, 'RogueColorSwatches')
        else:
            new_item = {
                'in_stock': 'Notify Me'
            }
            page_items.append(new_item)
    elif item_type == 'cerakote':
        page_items = get_data_from_js(page_soup, 'relatedColorSwatches')
    elif item_type == 'monster bench':
        page_items = get_data_from_js(page_soup, 'RogueColorSwatches', 5)
    elif item_type == 'rmlc':
        page_items = get_data_from_js(page_soup, 'RogueColorSwatches', 11)
    elif item_type == 'trolley':
        page_items = get_data_from_js(page_soup, 'RogueColorSwatches', 4)
    elif item_type == 'db15':
        page_items = get_data_from_js(page_soup, 'RogueColorSwatches', 2)
    elif item_type == 'custom2':
        page_items = get_data_from_js(page_soup, 'RogueColorSwatches')
    elif item_type == 'custom':
        page_items = get_data_from_js(page_soup, 'ColorSwatches')
    elif item_type == 'ironmaster':
        new_item = {
            'name': try_except(lambda: page_soup.find(class_='product_title').text.strip(), lambda: 'NOT FOUND'),
            'price': 'N/A',
            'in_stock': try_except(lambda: page_soup.find(class_='stock').text.strip(), lambda: 'NOT FOUND')
        }
        page_items.append(new_item)
    else:
        new_item = {
            'name': try_except(lambda: page_soup.find(class_='product-title').text.strip(), lambda: 'NOT FOUND'),
            'price': try_except(lambda: page_soup.find(class_='price').text.strip(), lambda: 'NOT FOUND'),
            'in_stock': try_except(lambda: page_soup.select('.product-options-bottom button')[0].text.strip(),
                                   lambda: 'NOT FOUND')
        }
        page_items.append(new_item)
    image_url = try_except(lambda: page_soup.find('div', class_='prod-header-img').find('img')['src'],
                           lambda: 'NOT FOUND'),
    # return page_items, image_url
    variables.checked_items[item_name] = page_items
    variables.items_to_check[item_name]['image_url'] = image_url


# Function to extract data from JavaScript script
def get_data_from_js(page_soup, script_name, slice_amount=0):
    info = []
    page_items = []

    scripts = page_soup.find_all(string=re.compile(script_name))
    for script in scripts:
        split_data = re.compile('[\[\]]{1,2}').split(script.strip())
        for split in split_data:
            if 'additional_options' in split:
                stripped_str = split[split.index('{'): split.index('stockTitle') - 2]
                info.append(json.loads(stripped_str + '}}'))

    if slice_amount != 0:
        info = info[0:slice_amount]

    for item in info:
        try:
            if item.get(list(item)[0])['isInStock']:
                stock_text = 'Add to Cart'
            else:
                stock_text = 'Notify Me'
        except:
            stock_text = 'NOT FOUND'

        new_item = {
            'name': try_except(lambda: item.get(list(item)[0])['label'], lambda: 'NOT FOUND'),
            'price': try_except(lambda: page_soup.find(class_='price').text.strip(), lambda: 'NOT FOUND'),
            'in_stock': stock_text
        }
        page_items.append(new_item)
    return page_items


# Try except function to simplify variable assignment
def try_except(success, failure, *exceptions):
    try:
        return success()
    except exceptions or Exception:
        return failure() if callable(failure) else failure
