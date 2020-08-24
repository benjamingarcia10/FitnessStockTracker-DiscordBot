from items import search_urls

import threading
from datetime import datetime
from playsound import playsound
from notifications import send_discord_webhook, send_startup_discord_webhook, send_text_notification
import json
import concurrent.futures

# FOR getData FUNCTIONS
import requests
import re
from uselessItems import useless_items
from bs4 import BeautifulSoup as soup

check_interval = ''
items_to_check = {}
check_counter = 1
start_time = None
longest_run_time = None
average_run_time = None
total_run_time = None
checked_items = {}
MAX_THREADS = 20


# Initialize program
def setup():
    global check_interval
    global items_to_check

    # Get items to check for from check.txt file
    try:
        with open('./check.txt', 'r') as file:
            for line in file:
                item = line.strip()
                try:
                    if len(item) <= 0 or item[0] == '#' or item[0:2] == '//':
                        continue
                    elif item not in items_to_check:
                        items_to_check[item] = search_urls[item]
                        print(f'Tracking stock for "{item}": {items_to_check[item]["product_name"]}')
                    else:
                        print(f'Found "{item}" in check.txt which has already been added.')
                except KeyError:
                    print(f'Found "{item}" in check.txt which is not a valid product item. Skipping this item.')
    except FileNotFoundError:
        input('Item file not found. Please create a "check.txt" file in the same directory as this program with what '
              'items you want tracked separated by new lines. Press ENTER to close this window.')
        exit('check.txt file not found.')
    print(f'\nTracking stock for {len(items_to_check)} item(s).\n')

    # Set a tracking interval for how often to recheck once code completes
    check_interval = input('What interval would you like to check items at (in seconds)? ').strip()
    while not isinstance(check_interval, int):
        try:
            check_interval = int(check_interval)
        except:
            print('Invalid interval.')
            check_interval = input('What interval would you like to check items at (excludes code execution time) '
                                   'in seconds? ').strip()
    if check_interval < 0:
        check_interval = 0
    print(f'Tracking {len(items_to_check)} item(s) with an interval of {check_interval} second(s).\n')

    # Send Discord webhook announcing program is starting and what items are being checked
    send_startup_discord_webhook(items_to_check, check_interval)


# Check items from items received in setup() function
def check_items():
    global check_interval, items_to_check, check_counter, start_time, longest_run_time, average_run_time, total_run_time
    start_time = datetime.now()                 # Set start time to calculate code execution length
    print(f'Check #{check_counter}')

    # Check all items and store them in checked_items
    # Each key in checked_items corresponds to the item tag in items.py
    # The value of the keys in checked_items correspond to a list of dictionaries of data of all items matching the key
    # Key example: "plate hi-temp"
    # Value format:
    # [{
    #     'name': FULL ITEM NAME,
    #     'price': ITEM PRICE,
    #     'in_stock': STOCK TEXT
    # },
    # {
    #     'name': FULL ITEM NAME,
    #     'price': ITEM PRICE,
    #     'in_stock': STOCK TEXT
    # },
    # ...}]
    # checked_items = {}
    # for item in items_to_check:
    #     checked_items[item], items_to_check[item]['image_url'] = get_data_from_url(items_to_check.get(item))

    # checked_items = {}
    # for item in items_to_check:
    #     checked_items[item], items_to_check[item]['image_url'] = get_data_from_url(items_to_check.get(item))

    threads = min(MAX_THREADS, len(items_to_check))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_data_from_url, items_to_check.keys())
        # executor.map(get_data_from_url, items_to_check.keys(), items_to_check.values())

    for item in checked_items:
        print(f'\tCHECKED: {item}')
    print()

    # Get any items that are in stock from checking items
    # Each key in in_stock_items corresponds to the item tag in items.py
    # The value of the keys in in_stock_items correspond to another dictionary with the full product name as the key
    #       and data of that specific item variation as the value
    # Key example: "bike echo"
    # Value format:
    # {
    #     'Rogue Echo Bike': {
    #         'price': '$775.00'
    #     },
    #     'Echo Bike Wind Guard': {
    #         'price': '$27.00'
    #     },
    #     'Echo Bike Phone Holder': {
    #         'price': '$6.00'
    #     }
    # }
    in_stock_items = get_in_stock(checked_items)

    # If there are items in stock, play sound and print to console as well as send Discord webhook
    # If no items in stock, print no items in stock
    # Also prints code execution time
    if len(in_stock_items) != 0:
        playsound('alert.mp3')
        for item in in_stock_items:
            item_variations_string = ''
            notification_string = ''
            for item_variations in in_stock_items.get(item):
                item_variations_string += f'\t\t{item_variations}: ' \
                                          f'{in_stock_items.get(item).get(item_variations)["price"]}\n' \
                                          f'\t\tIn Stock: ✅\n\n'
                notification_string += f'{item_variations}: ' \
                                       f'{in_stock_items.get(item).get(item_variations)["price"]}\n' \
                                       f'In Stock: ✅\n\n'
            item_variations_string += f'\t\tLink: {items_to_check[item]["link"]}\n'
            notification_string += f'Link: {items_to_check[item]["link"]}\n'

            # items_to_check[item]['image_url'][0] because extracting initial element from tuple
            # example: ('https://www.roguefitness.com/media/catalog/product/cache/1/rogue_header_2015/472321edac810f9b2465a359d8cdc0b5/c/a/cadillac-us-kettlebell-h2_revised_v2.jpg',)
            send_discord_webhook(item, notification_string, item_link=items_to_check[item]["link"],
                                 image_url=items_to_check[item]['image_url'][0])
            send_text_notification(item, notification_string, item_link=items_to_check[item]["link"])
            print(f'\tItem(s) in stock matching: "{item}"')
            print(item_variations_string)
    else:
        print('\tNo items in stock.\n')

    code_execution_time = datetime.now() - start_time

    if longest_run_time is None or code_execution_time > longest_run_time:
        longest_run_time = code_execution_time

    if total_run_time is None:
        total_run_time = code_execution_time
    else:
        total_run_time += code_execution_time

    if average_run_time is None:
        average_run_time = code_execution_time
    else:
        average_run_time = total_run_time / check_counter

    print(f'\tCode Execution Time: {code_execution_time}')
    print(f'\tLongest Run Time: {longest_run_time}')
    print(f'\tAverage Run Time: {average_run_time}\n')

    # Increase counter and restart function
    check_counter += 1
    threading.Timer(check_interval, check_items).start()


# Return all in stock items based on passed in dict
def get_in_stock(items):
    out_of_stock_text = ['Notify Me', 'Out of Stock', 'OUT OF STOCK', 'notify me', 'out of stock']
    in_stock_items = {}

    with open('./stock_status.json') as f:
        stock_status = json.load(f)

    for item in items:
        item_data = items.get(item)
        item_variations_in_stock = {}
        for item_variations in item_data:
            try:
                previous_stock_status = stock_status[f'{item} - {item_variations["name"]}']
            except:
                previous_stock_status = 0
                stock_status[f'{item} - {item_variations["name"]}'] = previous_stock_status

            if item_variations['in_stock'].strip() in out_of_stock_text:
                new_stock_status = 0
                stock_status[f'{item} - {item_variations["name"]}'] = new_stock_status
                continue
            elif item_variations['name'].strip() == 'NOT FOUND':
                continue
            else:
                new_stock_status = 1
                stock_status[f'{item} - {item_variations["name"]}'] = new_stock_status
                if previous_stock_status != new_stock_status:
                    item_variations_in_stock[item_variations['name']] = {
                        'price': item_variations['price'],
                    }
        if len(item_variations_in_stock) != 0:
            in_stock_items[item] = item_variations_in_stock

    with open('./stock_status.json', 'w') as f:
        json.dump(stock_status, f, indent=4)

    return in_stock_items


def clear_stock_status():
    with open('./stock_status.json', 'w') as f:
        json.dump({}, f, indent=4)


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
    checked_items[item_name] = page_items
    items_to_check[item_name]['image_url'] = image_url


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


if __name__ == '__main__':
    clear_stock_status()
    setup()
    check_items()
