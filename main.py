from aiogram.filters import Command
from aiogram import Bot, Dispatcher
import asyncio
import requests
from aiogram.types import Message
from aiogram import F
import json

work = False
API_TOKEN_TG = "7579540908:AAFvS3S4FSNSIr2mawod9C7IfQM9PJ2i5DQ"
bot = Bot(token=API_TOKEN_TG)
dp = Dispatcher(bot=bot)


@dp.message(Command('start'))
async def start_command(message):
    if message.from_user.username == "MaslikhinAV" or "Rider87":
        global work
        work = True
        await message.reply(
            "Привет!\nЯ бот для тестового задания в Хатико-Техника!\nОбратите внимание: доступ к моим возможностям есть только у @MaslikhinAV и @Rider87")

    else:
        await message.reply(f'доступ закрыт:( {message.from_user.username}')


@dp.message(F.text)
async def get_imei(message: Message):
    white_users = ['MaslikhinAV', 'Rider87']
    if message.from_user.username not in white_users:
        await message.answer(text=f'нет доступа\nВаш user_id - {message.from_user.username}')
        return

    url = "https://api.imeicheck.net/v1/checks"

    payload = json.dumps({
            "deviceId": message.text,
            "serviceId": 12
        })
    headers = {
            'Authorization': f'Bearer e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b',
            'Accept-Language': 'en',
            'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        json_response = json.loads(str(response.text))["properties"]
    except:
        await message.answer(str(json.loads(response.text)["errors"]['deviceId'][0]))
        return
    list_result = []
    for value in json_response:
        list_result.append(f'{value} - {json_response[value]}')


    await message.answer(text=('\n'.join(list_result)))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




