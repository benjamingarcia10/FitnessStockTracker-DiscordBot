from helpers.getData import get_data_from_item, create_new_session
import threading
from datetime import datetime
from helpers.notifications import send_rogue_stock_webhook, send_text_notification
from helpers.redditNotify import notify_stock_reddit_submission
import json
import concurrent.futures
from playsound import playsound
import multiprocessing

import variables

start_time = None
total_run_time = None


# Reset all variables to initial state to run new instance of tracking
def reset_rogue_variables():
    global start_time, total_run_time
    variables.is_tracking_rogue = False
    variables.check_counter = 0
    start_time = None
    variables.longest_run_time = None
    variables.average_run_time = None
    total_run_time = None
    # Reset stock status data only if Rogue persist mode is disabled
    if not variables.rogue_persist:
        clear_stock_status()


# Clear stock_status.json for tracking
def clear_stock_status():
    with open('./data/stock_status.json', 'w') as f:
        json.dump({}, f, indent=4)


# Start thread to track Rogue
def start_tracking_rogue():
    if variables.is_tracking_rogue:
        return
    else:
        variables.last_successful_check_datetime = None
        variables.is_tracking_rogue = True
        rogue_check_thread = threading.Thread(target=check_items)
        rogue_check_thread.start()


# Stop tracking Rogue
def stop_tracking_rogue():
    variables.is_tracking_rogue = False
    # variables.items_to_check = {}
    # variables.checked_items = {}


# Main function call to check items
def check_items():
    while variables.is_tracking_rogue:
        global start_time, total_run_time
        start_time = datetime.now()  # Set start time to calculate code execution length
        variables.check_counter += 1

        # Calculate how many threads to run based on length of items_to_check and max threads set in variables
        threads = min(variables.max_threads, len(variables.items_to_check))
        print(f'Check #{variables.check_counter} ({threads} Threads, {multiprocessing.cpu_count()} Cores): '
              f'{datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")}')

        # Check all items and store them in checked_items
        # Each key in checked_items corresponds to the item tag in items.py
        # The value of each key corresponds to a list of dictionaries of data of all items matching the key
        # Key example: 'plate hi-temp'
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
        create_new_session('https://www.roguefitness.com/')
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(get_data_from_item, variables.items_to_check.keys())
            # executor.map(get_data_from_item, variables.items_to_check.keys(), variables.items_to_check.values())

        # Additional console output if Rogue debug mode is enabled
        if variables.rogue_debug_mode:
            for item in variables.checked_items:
                print(f'\tCHECKED: {item} - {variables.checked_items[item]}')

        # Get any items that are in stock from checking items
        # Each key in in_stock_items corresponds to the item tag in items.py
        # The value of the keys in in_stock_items correspond to another dictionary with the full product name as the key
        #       and data of that specific item variation as the value
        # Key example: 'bike echo'
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
            if variables.play_notification_sound:
                try:
                    playsound('alert.mp3')
                except Exception as e:
                    print(f'{type(e)} - {e} Unable to play alert.')
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
                try:
                    canada_link = variables.items_to_check[item]["link"].replace('roguefitness.com', 'roguecanada.ca', 1)
                except:
                    canada_link = ''
                notification_string += f'Link: {variables.items_to_check[item]["link"]}'
                if canada_link != '':
                    notification_string += f'\n\nCA Link: {canada_link}'

                # items_to_check[item]['image_url'][0] because extracting initial element from tuple with only 1 element
                send_rogue_stock_webhook(item, notification_string, item_link=variables.items_to_check[item]["link"],
                                         image_url=variables.items_to_check[item]['image_url'][0])
                if variables.notify_reddit:
                    support_description = f'Rogue Stock Bot by u/bennykgarcia'
                    reddit_description = f'{notification_string}\n\n{support_description}'
                    notify_stock_reddit_submission(reddit_description)
                if variables.send_text_notification:
                    send_text_notification(item, notification_string)
                print(f'\tItem(s) in stock matching: "{item}"')
                print(item_variations_string)
        else:
            print('\tNo items in stock.\n')

        code_execution_time = datetime.now() - start_time

        if variables.longest_run_time is None or code_execution_time > variables.longest_run_time:
            variables.longest_run_time = code_execution_time

        if total_run_time is None:
            total_run_time = code_execution_time
        else:
            total_run_time += code_execution_time

        if variables.average_run_time is None:
            variables.average_run_time = code_execution_time
        else:
            variables.average_run_time = total_run_time / variables.check_counter

        completed_time = datetime.now()

        print(f'\tCompleted: {completed_time.strftime("%m/%d/%Y %I:%M:%S %p")}')
        print(f'\tCode Execution Time: {code_execution_time}')
        print(f'\tLongest Run Time: {variables.longest_run_time}')
        print(f'\tAverage Run Time: {variables.average_run_time}\n')
        variables.last_successful_check_datetime = completed_time
        variables.last_successful_check = completed_time.strftime("%m/%d/%Y %I:%M:%S %p")
        variables.last_successful_check_runtime = code_execution_time


# Return all in stock items based on passed in dict
def get_in_stock(items):
    out_of_stock_text = ['Notify Me', 'Out of Stock', 'OUT OF STOCK', 'notify me', 'out of stock']
    in_stock_items = {}

    # Load previous stock status data stored in stock_status.json
    with open('./data/stock_status.json') as f:
        stock_status = json.load(f)

    # New stock status dict to be dumped
    new_stock_status_dump = {}

    # Iterate through item
    for item in items:
        item_data = items.get(item)
        item_variations_in_stock = {}
        # Iterate through item variation (multiple variations per item ex. colors, size, weight, etc)
        for item_variations in item_data:
            try:
                previous_stock_status = stock_status[f'{item} - {item_variations["name"]}']
            except:
                previous_stock_status = 0

            # If in_stock key has any values in the out_of_stock_text list, mark it's new stock status as 0
            if item_variations['in_stock'].strip() in out_of_stock_text:
                new_stock_status = 0
                new_stock_status_dump[f'{item} - {item_variations["name"]}'] = new_stock_status
                continue
            # If item name has 'NOT FOUND', don't do anything with it and don't add back to list
            elif item_variations['name'].strip() == 'NOT FOUND':
                continue
            # Otherwise, item is in stock
            # Mark new stock status as 1, add it to new status dump
            # Add to in_stock_items if new status (in stock) is different from previous status (out of stock)
            else:
                new_stock_status = 1
                new_stock_status_dump[f'{item} - {item_variations["name"]}'] = new_stock_status
                if previous_stock_status != new_stock_status:
                    item_variations_in_stock[item_variations['name']] = {
                        'price': item_variations['price'],
                    }
        if len(item_variations_in_stock) != 0:
            in_stock_items[item] = item_variations_in_stock

    # Dump new stock status to json file
    with open('./data/stock_status.json', 'w') as f:
        json.dump(new_stock_status_dump, f, indent=4)

    return in_stock_items
