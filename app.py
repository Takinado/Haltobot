import asyncio
import logging

from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook

from data.config import WEBHOOK_URL_PATH, WEBAPP_HOST, WEBAPP_PORT, NOTIF_PERIOD, WEBHOOK_URL
from loader import bot, storage
from utils.db_api.models import get_accounts_to_sending
from utils.site.parsing import get_data


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    await bot.set_webhook(WEBHOOK_URL)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    commands = [
        BotCommand(command='/start', description='Начать'),
        BotCommand(command='/help', description='Получить справку'),
        BotCommand(command='/register', description='Регистрация'),
        BotCommand(command='/now', description='Получить данные по отключениям сейчас'),
    ]
    await bot.set_my_commands(commands)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await storage.close()
    await storage.wait_closed()
    logging.warning('Bye!')


async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        accounts = get_accounts_to_sending()
        for account in accounts:
            records = get_data(account.account)
            for record in records:
                await bot.send_message(account.profile.external_id,
                                       f"{record['date']} {record['time']}\n{account.address}\n{record['comment']}",
                                       disable_notification=True)


if __name__ == '__main__':
    from handlers import dp
    dp.loop.create_task(periodic(NOTIF_PERIOD))
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
