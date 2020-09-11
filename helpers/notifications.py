from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from dotenv import load_dotenv
from datetime import datetime
import traceback
import plivo
import variables

load_dotenv(override=True)


# Send Discord Webhook for in stock Rogue items using url from .env file and data arguments
def send_rogue_stock_webhook(product_tag, item_variations, item_link='', image_url=''):
    try:
        time_checked = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        stock_description = f'**Time Checked:** {time_checked}\n\n{item_variations}'
        support_description = f'Did this help you? Support the Project Here: https://www.buymeacoffee.com/benjamingarcia'
        description = f'{stock_description}\n\n{support_description}'

        stock_webhook = DiscordWebhook(username='Rogue Stock',
                                       url=os.getenv('ROGUE_FITNESS_WEBHOOK_URL'),
                                       avatar_url='https://i.imgur.com/LbZlRjA.png')

        custom_webhook_url = False
        try:
            item_category = variables.items_to_check[product_tag]['category']
            webhook_url = variables.rogue_category_data[item_category]['webhook_url']
            if webhook_url is not None:
                stock_webhook.url = webhook_url
                custom_webhook_url = True
        except:
            pass

        if variables.rogue_notify:
            try:
                item_category = variables.items_to_check[product_tag]['category']
                notify_role = variables.rogue_category_data[item_category]['notify_role']
                if notify_role is not None:
                    stock_webhook.content = f'{variables.items_to_check[product_tag]["product_name"]} ' \
                                            f'{notify_role.mention}'
                else:
                    try:
                        stock_webhook.content = f'{variables.items_to_check[product_tag]["product_name"]} @everyone'
                    except:
                        stock_webhook.content = f'@everyone'
            except:
                try:
                    stock_webhook.content = f'{variables.items_to_check[product_tag]["product_name"]} @everyone'
                except:
                    stock_webhook.content = f'@everyone'

        stock_embed = DiscordEmbed(color='5111552',
                                   title=f'Item(s) In Stock Matching Search: "{product_tag}"',
                                   description=description,
                                   url=item_link)

        if len(stock_embed.description) >= 2048:
            stock_embed.description = f'{stock_embed.description[0:2036]}\n**more...**'

        stock_embed.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
        if image_url == '' or image_url == 'NOT FOUND':
            pass
        else:
            # stock_embed.set_thumbnail(url=image_url)
            stock_embed.set_image(url=image_url)
        stock_webhook.add_embed(stock_embed)
        response = stock_webhook.execute()
    except Exception as e:
        if custom_webhook_url:
            print(f'\t{type(e)} Could not send Discord Webhook: {e}')
            print(f"\tFound webhook URL: {stock_webhook.url}. If that is incorrect, check your "
                  f"environment variables.")
            print(f'\tAttempting to send webhook to main URL.')
            try:
                stock_webhook.url = os.getenv('ROGUE_FITNESS_WEBHOOK_URL')
                response = stock_webhook.execute()
            except Exception as e1:
                print(f'\t{type(e1)} Could not send Discord Webhook: {e1}')
                print(f"\tFound webhook URL: {stock_webhook.url}. If that is incorrect, check your "
                      f"environment variables.")
                send_rogue_error_webhook('ERROR #8: Unable to trigger stock Discord notification. '
                                         'Please check webhook URLs and view console output for more information.')
        else:
            print(f'\t{type(e)} Could not send Discord Webhook: {e}')
            print(f"\tFound webhook URL: {stock_webhook.url}. If that is incorrect, check your "
                  f"environment variables.")
            send_rogue_error_webhook('ERROR #9: Unable to trigger stock Discord notification. Please check webhook '
                                     'URLs and view console output for more information.')


# Send Test Discord Webhooks for Rogue tracker to verify it is functional using urls from .env file and data arguments
def send_test_rogue_webhook():
    try:
        current_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        test_description = f'**Current Time:** {current_time}'

        stock_webhook = DiscordWebhook(username='Rogue Stock',
                                       url=os.getenv('ROGUE_FITNESS_WEBHOOK_URL'),
                                       avatar_url='https://i.imgur.com/LbZlRjA.png')
        stock_embed = DiscordEmbed(color='5111552',
                                   title=f'Item(s) In Stock Matching Search: "TEST WEBHOOK"',
                                   description=test_description)
        stock_embed.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
        stock_webhook.add_embed(stock_embed)
        response = stock_webhook.execute()
    except Exception as e:
        print(f'\t{type(e)} Could not send Discord Webhook: {e}')
        print(f"\tFound webhook URL: {stock_webhook.url}. If that is incorrect, check your "
              f"environment variables.")

    for category in variables.rogue_category_data:
        if variables.rogue_category_data[category]['webhook_url'] is not None:
            try:
                current_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                test_description = f'**Current Time:** {current_time}\n\nNotify Role Set To: ' \
                                   f'{variables.rogue_category_data[category]["notify_role"]}'

                stock_webhook = DiscordWebhook(username='Rogue Stock',
                                               url=variables.rogue_category_data[category]['webhook_url'],
                                               avatar_url='https://i.imgur.com/LbZlRjA.png')
                stock_embed = DiscordEmbed(color='5111552',
                                           title=f'Test Webhook for Item Category: {category}',
                                           description=test_description)
                stock_embed.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
                stock_webhook.add_embed(stock_embed)
                response = stock_webhook.execute()
            except Exception as e:
                print(f'\t{type(e)} Could not send Discord Webhook: {e}')
                print(f"\tFound webhook URL: {stock_webhook.url}. If that is incorrect, check your "
                      f"environment variables.")


# Send Discord Webhook to show that Rogue tracking stopped due to error using url from .env file and data arguments
def send_rogue_error_webhook(error_message, stop_tracking: bool = True):
    print(error_message)
    if stop_tracking:
        variables.is_tracking_rogue = False
        embed_color = '16711680'
        # variables.items_to_check = {}
        # variables.checked_items = {}
    else:
        embed_color = '5111552'
    try:
        current_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        error_description = f'**Current Time:** {current_time}\n\n{error_message}'

        stock_webhook = DiscordWebhook(username='Rogue Stock',
                                       url=os.getenv('ROGUE_FITNESS_WEBHOOK_URL'),
                                       avatar_url='https://i.imgur.com/LbZlRjA.png')
        stock_embed = DiscordEmbed(color=embed_color,
                                   title=f'Rogue Stock Bot Error',
                                   description=error_description)
        if stop_tracking and variables.bot_manager is not None:
            stock_webhook.content = variables.bot_manager.mention
        stock_embed.set_footer(text=f'Developer: Benjamin#9229', icon_url='https://i.imgur.com/1lNJjf3.png')
        stock_webhook.add_embed(stock_embed)
        response = stock_webhook.execute()
    except Exception as e:
        print(f'\t{type(e)} Could not send Discord Webhook: {e}')
        print(f"\tFound webhook URL: {stock_webhook.url}. If that is incorrect, check your "
              f"environment variables.")


# Send text notification to info provided in .env file
def send_text_notification(product_tag, item_variations):
    try:
        time_checked = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        stock_description = f'Item(s) In Stock Matching Search: "{product_tag}"\n\n' \
                            f'**Time Checked:** {time_checked}\n\n{item_variations}'
        support_description = f'Did this help you? Support the Project Here: https://www.buymeacoffee.com/benjamingarcia'
        description = f'{stock_description}\n\n{support_description}'

        client = plivo.RestClient(os.getenv('PLIVO_AUTH_ID'), os.getenv('PLIVO_AUTH_TOKEN'))

        message_created = client.messages.create(src=os.getenv('PLIVO_SOURCE_PHONE_NUMBER'),
                                                 dst=os.getenv('PHONE_NUMBER_TO_NOTIFY'), text=description)
    except plivo.exceptions.ValidationError as e:
        traceback.print_exc()
        print('\tBoth numbers should be in E.164 format, for example +15671234567.')
    except Exception as e1:
        traceback.print_exc()
        print(f'\t{type(e1)} - {e1} Unable to send text message notification. Please verify that all variables are '
              f'configured properly.')
