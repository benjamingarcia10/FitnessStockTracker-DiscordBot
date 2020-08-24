from getData import get_data_from_url
import threading
from datetime import datetime
from notifications import send_discord_webhook, send_text_notification
import json
import concurrent.futures
from playsound import playsound

import variables

check_counter = 0
start_time = None
longest_run_time = None
average_run_time = None
total_run_time = None
MAX_THREADS = 20


# Reset all variables to initial state to run new instance of tracking
def reset_rogue_variables():
    global check_counter, start_time, longest_run_time, average_run_time, total_run_time
    variables.is_tracking_rogue = False
    check_counter = 0
    start_time = None
    longest_run_time = None
    average_run_time = None
    total_run_time = None
    clear_stock_status()


# Clear stock_status.json for tracking
def clear_stock_status():
    with open('./stock_status.json', 'w') as f:
        json.dump({}, f, indent=4)


# Start thread to track rogue
def start_tracking_rogue():
    variables.is_tracking_rogue = True
    rogue_check_thread = threading.Thread(target=check_items)
    rogue_check_thread.start()


# Stop tracking rogue
def stop_tracking_rogue():
    variables.is_tracking_rogue = False


# Main function call to check items
def check_items():
    if not variables.is_tracking_rogue:
        return

    global check_counter, start_time, longest_run_time, average_run_time, total_run_time
    start_time = datetime.now()  # Set start time to calculate code execution length
    check_counter += 1
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
    threads = min(MAX_THREADS, len(variables.items_to_check))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_data_from_url, variables.items_to_check.keys())
        # executor.map(get_data_from_url, items_to_check.keys(), items_to_check.values())

    for item in variables.checked_items:
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
    in_stock_items = get_in_stock(variables.checked_items)

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
            item_variations_string += f'\t\tLink: {variables.items_to_check[item]["link"]}\n'
            notification_string += f'Link: {variables.items_to_check[item]["link"]}\n'

            # items_to_check[item]['image_url'][0] because extracting initial element from tuple
            # example: ('https://www.roguefitness.com/media/catalog/product/cache/1/rogue_header_2015/472321edac810f9b2465a359d8cdc0b5/c/a/cadillac-us-kettlebell-h2_revised_v2.jpg',)
            send_discord_webhook(item, notification_string, item_link=variables.items_to_check[item]["link"],
                                 image_url=variables.items_to_check[item]['image_url'][0])
            # send_text_notification(item, notification_string, item_link=variables.items_to_check[item]["link"])
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

    check_items()


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
