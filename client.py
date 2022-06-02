import asyncio
import aiohttp

HOST = 'http://127.0.0.1:8080'


async def main():
    async with aiohttp.ClientSession() as session:
        print('POST')
        async with session.post(f'{HOST}/ads/', json={'title':'Продаю','description':'продаю авто',
                                                      'create_date':'02.06.2022','user_id':1}) as response:
            print(await response.json())
        async with session.post(f'{HOST}/ads/', json={'title':'Сдаю','description':'Сдаю дом',
                                                      'create_date':'02.06.2022','user_id':2}) as response:
            print(await response.json())
        print('GET')
        async with session.get(f'{HOST}/ads/3/') as response:
            print(await response.text())
        async with session.get(f'{HOST}/ads/2/') as response:
            print(await response.json())
        print('PUT')
        async with session.put(f'{HOST}/ads/3/', json={'title': 'Не Продаю', 'description': 'не продаю авто',
                                                          'create_date': '02.06.2022', 'user_id': 1}) as response:
                print(await response.json())
        async with session.put(f'{HOST}/ads/1/', json={'title': 'Не Продаю', 'description': 'не продаю авто',
                                                         'create_date': '02.06.2022', 'user_id': 1}) as response:
                print(await response.json())
        print('DELETE')
        async with session.delete(f'{HOST}/ads/4/') as response:
            print(await response.json())
        async with session.delete(f'{HOST}/ads/1/') as response:
            print(await response.json())

asyncio.run(main())