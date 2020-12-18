from crawler import crawl
import asyncio
from concurrent.futures import ThreadPoolExecutor

io_pool_exc = ThreadPoolExecutor()

MAX_COROUTINE = 10
data = []


async def process(titleId):
    await asyncio.sleep(0.5)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(io_pool_exc, crawl, titleId)


async def main():
    corutines = set()
    while len(data) > 0 or len(corutines) > 0:
        if len(data) > 0 and len(corutines) < MAX_COROUTINE:
            corutines.add(asyncio.create_task(
                process(data.pop())))
        else:
            # await asyncio.gather(*corutines)
            done, pending = await asyncio.wait(corutines, return_when=asyncio.FIRST_COMPLETED)
            corutines = pending


if __name__ == "__main__":
    with open('titleId.txt', 'r') as t_list:
        data += t_list.read().splitlines()
    asyncio.run(main())
