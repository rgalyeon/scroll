import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import questionary
from loguru import logger
from questionary import Choice

from settings import (
    RANDOM_WALLET,
    SLEEP_TO,
    SLEEP_FROM,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO, REMOVE_WALLET
)
from modules_settings import *
from utils.helpers import remove_wallet
from utils.sleeping import sleep
from utils.logs_handler import filter_out_utils
from utils.password_handler import get_wallet_data
from itertools import count


def get_module():
    counter = count(1)
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice(f"{next(counter)}) Encrypt private keys", encrypt_privates),
            Choice(f"{next(counter)}) Deposit to Scroll", deposit_scroll),
            Choice(f"{next(counter)}) Withdraw OKX", withdraw_okx),
            Choice(f"{next(counter)}) Withdraw from Scroll", withdraw_scroll),
            Choice(f"{next(counter)}) Bridge Orbiter", bridge_orbiter),
            Choice(f"{next(counter)}) Bridge Layerswap", bridge_layerswap),
            Choice(f"{next(counter)}) Wrap ETH", wrap_eth),
            Choice(f"{next(counter)}) Unwrap ETH", unwrap_eth),
            Choice(f"{next(counter)}) Swap on Skydrome", swap_skydrome),
            Choice(f"{next(counter)}) Swap on Zebra", swap_zebra),
            Choice(f"{next(counter)}) Swap on SyncSwap", swap_syncswap),
            Choice(f"{next(counter)}) Deposit LayerBank", deposit_layerbank),
            Choice(f"{next(counter)}) Withdraw LayerBank", withdraw_layerbank),
            Choice(f"{next(counter)}) Deposit RocketSam", deposit_rocketsam),
            Choice(f"{next(counter)}) Withdraw RocketSam", withdraw_rocketsam),
            Choice(f"{next(counter)}) Mint and Bridge Zerius NFT", mint_zerius),
            Choice(f"{next(counter)}) Mint ZkStars NFT", mint_zkstars),
            Choice(f"{next(counter)}) Create NFT collection on Omnisea", create_omnisea),
            Choice(f"{next(counter)}) Mint NFT on NFTS2ME", mint_nft),
            Choice(f"{next(counter)}) Parse NFTS2ME collections", parse_nfts2me_contracts),
            Choice(f"{next(counter)}) Dmail send email", send_mail),
            Choice(f"{next(counter)}) Create gnosis safe", create_safe),
            Choice(f"{next(counter)}) Deploy contract", deploy_contract),
            Choice(f"{next(counter)}) Mint Scroll Origins NFT", nft_origins),
            Choice(f"{next(counter)}) Swap tokens to ETH", swap_tokens),
            Choice(f"{next(counter)}) Use Multiswap", swap_multiswap),
            Choice(f"{next(counter)}) Use custom routes", custom_routes),
            Choice(f"{next(counter)}) Check transaction count", "tx_checker"),
            Choice(f"{next(counter)}) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("❤️ Author – https://t.me/sybilwave")
        print("❤️ Fork Author – https://t.me/rgalyeon\n")
        sys.exit()
    return result


def get_wallets():
    wallet_data = get_wallet_data()

    wallets = [
        {
            "id": _id,
            "key": wallet_data[address]['private_key'],
            "okx_address": wallet_data[address]['okx_address'],
        } for _id, address, in enumerate(wallet_data, start=1)
    ]

    return wallets


async def run_module(module, account_id, key):
    try:
        await module(account_id, key)
    except Exception as e:
        logger.error(e)

    if REMOVE_WALLET:
        remove_wallet(key)

    await sleep(SLEEP_FROM, SLEEP_TO)


def _async_run_module(module, account_id, key):
    asyncio.run(run_module(module, account_id, key))


def main(module):
    if module == encrypt_privates:
        return encrypt_privates(force=True)
    if module == parse_nfts2me_contracts:
        return parse_nfts2me_contracts()

    wallets = get_wallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                _async_run_module,
                module,
                account.get("id"),
                account.get("key"),
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':
    print("❤️ Author – https://t.me/sybilwave")
    print("❤️ Fork Author – https://t.me/rgalyeon\n")

    logger.add('logs.txt', filter=filter_out_utils)

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("❤️ Author – https://t.me/sybilwave")
    print("❤️ Fork Author – https://t.me/rgalyeon\n")
