import requests
import re
from uselessItems import useless_items
from bs4 import BeautifulSoup as soup
import json
import time

from items import search_urls
import variables

current_session = requests.Session()
session_cookies = None


def create_new_session():
    global current_session, session_cookies
    current_session.close()
    current_session = requests.Session()
    print(f'\tCreated new session.')

    current_session.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        # 'authority': 'www.roguefitness.com',
        # ':authority:': 'www.roguefitness.com',
    })

    current_session.get('https://www.roguefitness.com/')

    print(f'\t{len(current_session.cookies)} Cookie(s): {current_session.cookies}')

    # # Run Chrome selenium in headless mode
    # options = Options()
    # options.headless = True
    # driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    # driver.delete_all_cookies()
    # driver.get('https://www.roguefitness.com/')
    # print(f'\tCreated new session.')
    # cfduid_cookie = driver.get_cookie('__cfduid')
    # cfruid_cookie = driver.get_cookie('__cfruid')
    # session_cookies = [cfduid_cookie, cfruid_cookie]
    # print(f'\t{len(session_cookies)} Cookie(s): {session_cookies}')
    # driver.close()
    #
    # current_session.close()
    # current_session = requests.Session()
    #
    # current_session.headers.update({
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    #     # 'authority': 'www.roguefitness.com',
    #     # ':authority:': 'www.roguefitness.com',
    # })
    #
    # for cookie in session_cookies:
    #     try:
    #         expiry = cookie['expiry']
    #     except KeyError:
    #         expiry = None
    #     current_session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'],
    #                                 secure=cookie['secure'], expires=expiry)
    # print(f'\t{len(current_session.cookies)} Cookie(s): {current_session.cookies}')


def get_data_from_url(item_name):
    global current_session, session_cookies
    item_type = search_urls[item_name]['type']
    full_item_name = search_urls[item_name]['product_name']
    item_link = search_urls[item_name]['link']
    item_category = search_urls[item_name]['category']
    page_items = []

    response = current_session.get(item_link)
    redirect_count = len(response.history)

    page_soup = soup(response.text, 'html.parser')

    if page_soup.find(id='cfRayId') is not None:
        print(f'\tFound Captcha')
        print(f'\tRequest: {current_session.headers}')
        print(f'\tResponse: {response.headers}')
        print(f'\tCookies: {current_session.cookies}')
        time.sleep(5)

    if variables.debug_mode:
        print(page_soup)
        time.sleep(5)

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
