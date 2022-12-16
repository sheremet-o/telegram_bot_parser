import pandas as pd

import os
import logging

from sqlalchemy import create_engine

from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from dotenv import load_dotenv

load_dotenv()

SECRET_TOKEN = os.getenv('SECRET_TOKEN', default='5820046202:AAGloLnkoTlcZphFebSKyREfa076h-x-0KM')


'''Создание или обновление баззы данных'''
engine = create_engine('sqlite:///sqlite.db', echo=False)

data = pd.read_excel('downloads/urls.xlsx')
data_dict = data.to_sql('urls', engine, if_exists='append')


'''Конфигурация бота'''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Загрузи файл с информацией в формате (название, URL, xpath запрос)'.format(name),
    )


def upload_file(update, context):
    chat = update.effective_chat
    context.bot.get_file(update.message.document).download()
    with open('downloads/urls.xlsx', 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    
    dataframe1 = pd.read_excel('downloads/urls.xlsx')

    string_data = dataframe1.to_string()

    context.bot.send_message(chat_id=chat.id, text=string_data)

    context.bot.send_message(
        chat_id=chat.id,
        text='База данных обновлена'
    )


def main():
    updater = Updater(token=SECRET_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(
         MessageHandler(Filters.document, upload_file))

    updater.start_polling(poll_interval=0.10)
    updater.idle()


if __name__ == '__main__':
    main()
