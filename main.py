import os
import threading
import multiprocessing
import time
import argparse
import aiohttp
import asyncio
import requests

urls = [
    'https://t3.ftcdn.net/jpg/05/57/92/94/360_F_557929456_H0L12sooeJMSSnI98jMyqfzxd93dKOcP.jpg',
    'https://img.freepik.com/premium-photo/cute-kitten-wearing-scarf-warm-hat-ai-generative_407474-9068.jpg',
    'https://i.pinimg.com/1200x/b1/7f/d3/b17fd354a1e8963a145669a912559260.jpg',
    'https://t4.ftcdn.net/jpg/06/67/21/45/360_F_667214521_BKRRSkuag0gtJGcrkuWmTcOFpL1kpzXv.jpg',
    'https://img.freepik.com/premium-photo/orange-kitten-blanket-with-dark-background_758367-15054.jpg'
]


def save_image(url: str, path: str):
    extensions = ['png', 'jpg', 'jpeg', 'gif', 'tiff']
    start_time = time.time()
    file_name = url.split('/')[-1]
    if file_name.split('.')[-1] in extensions:
        image = requests.get(url)
        with open(os.path.join(path, file_name), 'wb') as file:
            file.write(image.content)
        print(f'Время выполнения: {(time.time() - start_time):.2f} секунд')


def save_image_threading(new_urls: list[str] = urls):
    path = os.path.join(os.getcwd(), 'images', 'threads')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    threads = []
    start_time = time.time()
    for url in new_urls:
        t = threading.Thread(target=save_image, args=(url, path))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(
        f'Общее время выполнения (многопоточность): '
        f'{(time.time() - start_time):.2f} секунд')


def save_image_multiprocessing(new_urls: list[str] = urls):
    path = os.path.join(os.getcwd(), 'images', 'processes')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    processes = []
    start_time = time.time()
    for url in new_urls:
        p = multiprocessing.Process(target=save_image, args=(url, path))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(
        f'Общее время выполнения (многопроцессность): '
        f'{(time.time() - start_time):.2f} секунд')


async def save_image_async(new_url):
    extensions = ['png', 'jpg', 'jpeg', 'gif', 'tiff']
    path = os.path.join(os.getcwd(), 'images', 'async')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    start_time = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(new_url) as image:
                file_name = new_url.split('/')[-1]
                if file_name.split('.')[-1] in extensions:
                    with open(os.path.join(path, file_name), 'wb') as file:
                        file.write(await image.read())
                    print(f'Время выполнения: '
                          f'{(time.time() - start_time):.2f} секунд')
    except Exception as e:
        print(e)


async def save_images_async(new_urls: list[str] = urls):
    tasks = []
    start_time = time.time()
    for url in new_urls:
        task = asyncio.ensure_future(save_image_async(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(
        f'Общее время выполнения (асинхронность): '
        f'{(time.time() - start_time):.2f} секунд')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save images from URLs')
    parser.add_argument('urls', type=str, nargs='*',
                        help='Введите адреса изображений')
    args = parser.parse_args()
    if args.urls:
        save_image_threading(args.urls)
        save_image_multiprocessing(args.urls)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(save_images_async(args.urls))
    else:
        save_image_threading()
        save_image_multiprocessing()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(save_images_async())
