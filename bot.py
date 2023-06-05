import telegram
from fluent import sender
import asyncio
from telegram.error import TelegramError
from prometheus_client import start_http_server, Counter

TOKEN = '6029933916:AAHQdPGxZVJYVI8rM6GmeuwzWkC5KQ0575U'
fluentd_host = '127.0.0.1'
fluentd_port = 24224

message_counter = Counter('telegram_messages_sent', 'Total number of messages sent')


async def main():
    bot = telegram.Bot(TOKEN)
    logger = sender.FluentSender('telegram_bot', host=fluentd_host, port=fluentd_port)
    bot_response = "Hello world"

    try:
        await bot.send_message(chat_id='611400192', text=bot_response)
        log_data = {
            'bot_response': bot_response,
        }

        message_counter.inc()
    except TelegramError as e:
        log_data = {
            'telegram_error': f"Error occurred while sending message: {e}"
        }
    except Exception as e:
        log_data = {
            'exception': f"An error occurred: {e}"
        }
    logger.emit('telegram_message', log_data)


start_http_server(9091)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())