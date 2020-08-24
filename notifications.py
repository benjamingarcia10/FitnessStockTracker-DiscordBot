from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from dotenv import load_dotenv
from datetime import datetime
import traceback
import plivo

load_dotenv(override=True)


# Send Discord Webhook using url from .env file and data arguments
def send_discord_webhook(product_tag, item_variations, item_link='', image_url=''):
    try:
        time_checked = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        stock_description = f'**Time Checked:** {time_checked}\n\n{item_variations}'

        stock_webhook = DiscordWebhook(username='Rogue Stock',
                                       url=os.getenv('ROGUE_FITNESS_WEBHOOK_URL'),
                                       avatar_url='https://i.imgur.com/LbZlRjA.png',
                                       content='@everyone'
                                       )
        stock_embed = DiscordEmbed(color='5111552',
                                   title=f'Item(s) In Stock Matching Search: "{product_tag}"',
                                   description=stock_description,
                                   url=item_link)
        stock_embed.set_footer(text=f'Checked: {time_checked}', icon_url='https://i.imgur.com/LbZlRjA.png')
        if image_url == '' or image_url == 'NOT FOUND':
            pass
        else:
            # stock_embed.set_thumbnail(url=image_url)
            stock_embed.set_image(url=image_url)
        stock_webhook.add_embed(stock_embed)
        response = stock_webhook.execute()
    except:
        print(f'\tCould not send Discord Webhook. Check that the Webhook URL is in your .env file.')


def send_text_notification(product_tag, item_variations, item_link='',):
    try:
        time_checked = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        stock_description = f'Item(s) In Stock Matching Search: "{product_tag}"\n\n' \
                            f'**Time Checked:** {time_checked}\n\n{item_variations}'

        client = plivo.RestClient(os.getenv('PLIVO_AUTH_ID'), os.getenv('PLIVO_AUTH_TOKEN'))

        message_created = client.messages.create(src=os.getenv('PLIVO_SOURCE_PHONE_NUMBER'),
                                                 dst=os.getenv('PHONE_NUMBER_TO_NOTIFY'), text=stock_description)
    except plivo.exceptions.ValidationError as e:
        traceback.print_exc()
        print('Both numbers should be in E.164 format, for example +15671234567.')
