import asyncio
import time
from random import randint

texts_message = ["Привет!", "Как дела?", "До свидания!"]

time1 = time.time()
async def print_message_with_timer(message):
    await asyncio.sleep(randint(1,3))
    print(message)

async def main():
    tasks = []

    for message in texts_message:
        tasks.append(asyncio.create_task(print_message_with_timer(message)))

    await asyncio.gather(*tasks)

asyncio.run(main())
print(time.time() - time1)
