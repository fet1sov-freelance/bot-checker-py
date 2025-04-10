import asyncio, datetime
from decouple import config
from pyrogram import Client
import sqlite3 as database
from utils import check_online_status
import time

db = database.connect("radar.db")
db.execute('''CREATE TABLE IF NOT EXISTS history (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    accountid INTEGER,
    date      TEXT,
    online    INTEGER
);
''')

bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))
bot.start()

async def onlineChecker():
    with open('radarids.txt', 'r', encoding='UTF-8') as file:
        while line := file.readline():
            onlineStatus = await check_online_status(bot, line.rstrip())
            db.execute(f"""
                INSERT INTO history (
                    online,
                    date,
                    accountid
                )
                VALUES (
                    \'{onlineStatus}\',
                    \'{time.time()}\',
                    \'{line.rstrip()}\'
                )
            """)
            db.commit()

            print("ONLINE CHECKED ON: " + line.rstrip())

bot.send_message(chat_id='me', text='Скрипт по обнаружению запущен')

async def at_minute_start(cb):
    while True:
        now = datetime.datetime.now()
        after_minute = now.second + now.microsecond / 1_000_000
        if after_minute:
            await asyncio.sleep(60 - after_minute)
        await cb()

loop = asyncio.get_event_loop()
loop.create_task(at_minute_start(lambda: onlineChecker()))
loop.run_forever()