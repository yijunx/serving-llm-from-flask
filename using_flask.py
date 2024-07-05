import requests
import asyncio
import os, threading
import time
from concurrent.futures import ThreadPoolExecutor


def do_one_task_but_sync(i: int, mock: bool):
    now = time.perf_counter()
    print(f"this is request {i}, now is {now}")
    print(f"executing request with process id: {os.getpid()}")
    print(f"executing request with thread id : {threading.current_thread().ident}")
    url = (
        "http://localhost:8000/apis/q-and-a/mock-q"
        if mock
        else "http://localhost:8000/apis/q-and-a/q"
    )
    r = requests.post(
        url,
        json={"content": "how to avoid diabetes", "query_option": True},
    )
    # here can log based on i
    print(
        f"obtained response for request {i}: {r.status_code} in {time.perf_counter() - now} seconds"
    )


# class Counter:
#     def __init__(self, log_internal: int = 10):
#         self.log_interval = log_internal
#         self.count = 0

#     def update(self, task_count):
#         self.count += 1
#         # log every time X tasks are completed
#         if self.count % self.log_interval == 0:
#             print(f"tasks completed: {self.count} / {task_count}")


# counter = Counter(log_internal=1)


# async def increment_counter(lock, task_count):
#     # avoid two parallel task incremening coutner at the same time
#     # async with Lock ensures that only one task enters code inside async with lock block
#     # so other task waits until current task finished updated
#     # this solves two task updating coutner at the same time
#     async with lock:
#         counter.update(task_count)


async def execute_single_task(i, mock):
    # print(f"task {i} started")

    # execute claim flow in other thread
    # here actually we can pass arguments to the task
    await asyncio.to_thread(do_one_task_but_sync, i=i, mock=mock)

    # increment counter for log purpose
    # await increment_counter(lock, task_count)

    # await asyncio.sleep(5)
    # print(f"task {i} ended")


async def main(task_count: int, interval: float, mock: bool):
    tasks = []
    # to increase the number of concurrencies.., now it can do up to 200 threads
    loop = asyncio.get_running_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=200))
    # lock = asyncio.Lock()
    for i in range(task_count):
        task = asyncio.create_task(execute_single_task(i=i, mock=mock))
        tasks.append(task)
        # await interval seconds before creating new task in next loop
        await asyncio.sleep(interval)
    # wait for all task to end after creating all task
    # without this, program ends before all task ends and cannot check whether all tasks ended successfully
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main(task_count=20, interval=0.1, mock=False))
