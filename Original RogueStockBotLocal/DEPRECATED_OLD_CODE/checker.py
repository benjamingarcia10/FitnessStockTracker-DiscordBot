from items import search_urls
from getData import get_data_from_url
import threading
from datetime import datetime
from playsound import playsound
from notifications import send_discord_webhook, send_startup_discord_webhook
import json

check_interval = ''
items_to_check = {}
check_counter = 1
start_time = None
longest_run_time = None
average_run_time = None
total_run_time = None


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
    send_startup_discord_webhook(items_to_check, check_interval)


# Check items from items received in setup() function
def check_items():
    global check_interval, items_to_check, check_counter, start_time, longest_run_time, average_run_time, total_run_time
    start_time = datetime.now()                     # Set start time to calculate code execution length
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
    checked_items = {}
    for item in items_to_check:
        checked_items[item], items_to_check[item]['image_url'] = get_data_from_url(items_to_check.get(item))

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
            for item_variations in in_stock_items.get(item):
                item_variations_string += f'\t\t{item_variations}: ' \
                                          f'{in_stock_items.get(item).get(item_variations)["price"]}\n' \
                                          f'\t\tIn Stock: ✅\n\n'
            item_variations_string += f'\t\tLink: {items_to_check[item]["link"]}\n'
            send_discord_webhook(item, item_variations_string, item_link=items_to_check[item]["link"],
                                 image_url=items_to_check[item]['image_url'][0])
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


clear_stock_status()
setup()
check_items()
