import requests
import re
from data.uselessItems import useless_items
from bs4 import BeautifulSoup as soup
import json
import traceback

from data.items import search_urls
import variables

from helpers.notifications import send_rogue_error_webhook

current_session = requests.Session()
item_retry_data = {}
original_session_retries = 0
max_session_retries = 10


# Create new session with cookies from www.roguefitness.com
def create_new_session(url, item_name=None):
    global current_session, item_retry_data, original_session_retries, max_session_retries
    if item_name is None:
        try:
            try:
                current_session.close()
            except:
                traceback.print_exc()
            current_session = requests.Session()

            if variables.rogue_debug_mode:
                print(f'\tCreated new session.')

            current_session.headers.update({
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                # 'authority': 'www.roguefitness.com',
            })

            current_session.get(url)

            if variables.rogue_debug_mode:
                print(f'\t{len(current_session.cookies)} Cookie(s): {current_session.cookies}')
            original_session_retries = 0
        except Exception as e:
            original_session_retries += 1
            if original_session_retries > max_session_retries:
                send_rogue_error_webhook(f'{type(e)} - {e} Could not create new session. Cloud Server connection '
                                         f'error. Bot managers or server admins please restart Rogue tracking '
                                         f'({variables.command_prefix}rogue).')
                return
            else:
                create_new_session(url)
    else:
        try:
            try:
                item_retry_data[item_name]['current_session'].close()
            except KeyError as e:
                item_retry_data[item_name] = {
                    'retry_count': 0,
                    'current_session': None
                }
            except:
                traceback.print_exc()

            new_session = requests.Session()

            if variables.rogue_debug_mode:
                print(f'\tCreated new session for item: {item_name}.')

            new_session.headers.update({
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                # 'authority': 'www.roguefitness.com',
            })

            new_session.get(url)

            if variables.rogue_debug_mode:
                print(f'\tITEM SESSION ({item_name}) - {len(new_session.cookies)} Cookie(s): {new_session.cookies}')

            item_retry_data[item_name] = {
                'retry_count': 0,
                'current_session': new_session
            }
            return new_session
        except Exception as e:
            if item_name in item_retry_data:
                item_retry_data[item_name]['retry_count'] += 1
            else:
                item_retry_data[item_name] = {
                    'retry_count': 1,
                    'current_session': None
                }
            if item_retry_data[item_name]['retry_count'] > max_session_retries:
                send_rogue_error_webhook(
                    f'{type(e)} - {e} Could not create new session for {item_name} after '
                    f'{item_retry_data[item_name]["retry_count"]} retries. Cloud Server connection error. '
                    f'Bot managers or server admins please restart Rogue tracking ({variables.command_prefix}rogue).')
                return None
            else:
                return create_new_session(url, item_name)


# Extract data from item based on item_name and item type
def get_data_from_item(item_name):
    if variables.rogue_debug_mode:
        print(f'\tChecking {item_name}')

    global current_session
    item_type = search_urls[item_name]['type']
    full_item_name = search_urls[item_name]['product_name']
    item_link = search_urls[item_name]['link']
    item_category = search_urls[item_name]['category']
    page_items = []

    # If connection error, stop tracking and send error notification
    try:
        response = current_session.get(item_link)
        redirect_count = len(response.history)
        page_soup = soup(response.text, 'html.parser')
    except Exception as e:
        try:
            item_session = create_new_session('https://www.roguefitness.com/', item_name)
            response = item_session.get(item_link)
            redirect_count = len(response.history)
            page_soup = soup(response.text, 'html.parser')
        except:
            traceback.print_exc()
            send_rogue_error_webhook(f'{type(e)} - {e} Could not connect to page when tracking {item_name}. Cloud '
                                     f'Server connection error. Bot managers or server admins please restart Rogue '
                                     f'tracking ({variables.command_prefix}rogue).')
            return

    # Stop tracking and send error notification if captcha is found
    if page_soup.find(id='cfRayId') is not None:
        if item_type == 'bone' or item_type == 'grab bag':
            pass
        else:
            try:
                item_session = create_new_session('https://www.roguefitness.com/', item_name)
                response = item_session.get(item_link)
                redirect_count = len(response.history)
                page_soup = soup(response.text, 'html.parser')

                if page_soup.find(id='cfRayId') is not None:
                    print(f'\tFound Captcha When Checking {item_name}')
                    print(f'\tLink: {item_link}')
                    print(f'\tRequest: {item_session.headers}')
                    print(f'\tResponse: {response.headers}')
                    print(f'\tCookies: {item_session.cookies}')
                    # print(page_soup)
                    send_rogue_error_webhook(f'CAPTCHA FOUND on {item_name} - Stopping tracking')
            except Exception as e1:
                traceback.print_exc()
                send_rogue_error_webhook(f'{type(e1)} - {e1} Could not connect to page when tracking {item_name}. '
                                         f'Cloud Server connection error. Bot managers or server admins please '
                                         f'restart Rogue tracking ({variables.command_prefix}rogue).')
                return

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
            item_quantity = single_item.find(class_='item-qty')
            if item_quantity is None:
                new_item['in_stock'] = 'Out of Stock'
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
            pass
            # new_item = {
            #     'in_stock': 'Notify Me'
            # }
            # page_items.append(new_item)
    elif item_type == 'grab bag':
        if redirect_count == 0:
            page_items = get_data_from_js(page_soup, 'RogueColorSwatches')
        else:
            pass
            # new_item = {
            #     'in_stock': 'Notify Me'
            # }
            # page_items.append(new_item)
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
        item_quantity = page_soup.find(class_='qty-wrapper')
        if item_quantity is None:
            new_item['in_stock'] = 'Out of Stock'
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
