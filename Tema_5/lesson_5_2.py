import asyncio
import time
from random import randint

numbers = [1, 2, 3, 4, 5]

def compute(number_def):
    time.sleep(randint(1,3))
    return number_def*2

async def compute_async(number_def):
    await asyncio.sleep(randint(1,3))
    return number_def*2

async def main():
    tasks = []
    numbers_out = []

    time_1 = time.time()
    for number in numbers:
        numbers_out.append(compute(number))
    print(time.time() - time_1)

    time_2 = time.time()
    for number in numbers:
        tasks.append(asyncio.create_task(compute_async(number)))

    await asyncio.gather(*tasks)
    print(time.time() - time_2)

asyncio.run(main())
