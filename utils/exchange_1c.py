import asyncio
import aiohttp
import json
import config


async def get_user_data_1c(phone_number):
    auth = aiohttp.BasicAuth(config.USER_1C_API, config.PSW_1C_API)
    headers = {'Accept': 'application/json'}
    async with aiohttp.ClientSession(auth=auth, headers=headers) as session:
        async with session.get(f'{config.URL_1C_API}profile/?phone_number={phone_number}') as resp:
            data = await resp.text(encoding='utf-8-sig')
            data = json.loads(data)
            data['phone_number'] = phone_number
            return data
    # data = {
    #     'find_user': False,
    #     'name': 'TEST222 SDS',
    #     'barcode': '3235438764532',
    #     'ref': '00000-0000-00000-00',
    #     'phone_number': '+2 324 443 32 32'
    # }
    # return data


async def create_user_discount(description, phone_number, email):
    auth = aiohttp.BasicAuth(config.USER_1C_API, config.PSW_1C_API)
    phone_number = phone_number.replace(' ', '.')
    data = {
        'description': description,
        'phone_number': phone_number,
        'email': email
    }
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(f'{config.URL_1C_API}profile/',
                                json=data) as resp:
            data_response = await resp.text(encoding='utf-8-sig')
            data_response = json.loads(data_response)
            return data_response
    # data = {
    #     'error': False,
    #     'name': 'TEST222 SDS',
    #     'barcode': '3235438764532',
    #     'ref': '00000-0000-00000-00',
    #     'phone_number': '+2 324 443 32 32'
    # }
    # return data
