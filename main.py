import aiohttp
import asyncio
import requests
import time
import sys

from more_itertools import chunked
from sqlalchemy import insert
from aiopg.sa import create_engine

import config
from tables import CharacterModel, get_async_session

URL = "https://swapi.dev/api/people/"

req = requests.get(URL)
# print(req.json())
print(f"В базе - {req.json()['count']} - персонажа")


async def get_char(session: aiohttp.client.ClientSession, char_id):
    async with session.get(f'{URL}{char_id}') as response:
        response_json = await response.json()
        try:
            response_json['id'] = char_id
            response_json.pop('created')
            response_json.pop('edited')
            response_json.pop('url')
        except:
            response_json['id'] = char_id

        return response_json


async def get_chars(session: aiohttp.client.ClientSession, range_char_id):
    chars_list = []
    for char_id in range_char_id:
        res = await get_char(session, char_id)
        chars_list.append(res)
    for char_id_chunk in chunked(range_char_id, 10):
        get_char_tasks = [asyncio.create_task(get_char(session, char_id)) for char_id in char_id_chunk]
        await asyncio.gather(*get_char_tasks)
    return chars_list


async def add_character(char):
    async with create_engine(config.db_link_2) as engine:
        async with engine.acquire() as conn:
            try:
                char_add = insert(CharacterModel).values(
                    id=char['id'],
                    birth_year=char['birth_year'],
                    eye_color=char['eye_color'],
                    films=char['films'],
                    gender=char['gender'],
                    hair_color=char['hair_color'],
                    height=char['height'],
                    homeworld=char['homeworld'],
                    mass=char['mass'],
                    name=char['name'],
                    species=char['species'],
                    skin_color=char['skin_color'],
                    starships=char['starships'],
                    vehicles=char['vehicles']
                )
                await conn.execute(char_add)
            except KeyError:
                char_add = insert(CharacterModel).values()
                await conn.execute(char_add)
            except ValueError:
                char_add = insert(CharacterModel).values()
                await conn.execute(char_add)


async def add_characters():
    async with aiohttp.client.ClientSession() as session:
        chars_list = await get_chars(session, range(2, req.json()['count']))
        for char in chars_list:
            await add_character(char)


async def main():
    async with aiohttp.client.ClientSession() as session:
        await get_chars(session, range(2, req.json()['count']))
        await get_async_session(True, True)
        await add_characters()
        time.sleep(0.1)


###     Избежание RuntimeError: Event loop is closed
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f"Добавлено: {req.json()['count']} персонажей, за {time.time() - start} секунд")
