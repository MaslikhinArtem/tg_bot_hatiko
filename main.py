import asyncio
from aiogram import Bot, Dispatcher, types
from http_client import IMEIHTTPClient
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('API_TOKEN_TG'))
dp = Dispatcher(bot=bot)

@dp.message()
async def handle_message(message: types.Message):
    white_users = ['MaslikhinAV', 'Rider87']
    if message.from_user.username not in white_users:
        await message.answer(text=f'нет доступа\nВаш user_id - {message.from_user.username}')
        return

    client = IMEIHTTPClient(base_url='https://api.imeicheck.net', headers = {
            'Authorization': f'Bearer {os.getenv('API_TOKEN_IMEI')}',
            'Accept-Language': 'en',
            'Content-Type': 'application/json'
        }
)
    response = await client.get_listings(message.text)
    await client.close()

    try:
        json_response = response['properties']
    except KeyError:
        await message.answer(str(json.loads(response)["errors"].get('deviceId', ['Неизвестная ошибка'])[0]))
        return

    list_result = [f'{value} - {json_response[value]}' for value in json_response]
    await message.answer(text=('\n'.join(list_result)))
    print(list_result)
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())