from loguru import logger
from config import SECONDLIVE_CONTRACT, SECONDLIVE_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from datetime import datetime
import pytz


class SecondLive(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="scroll")

        self.contract = self.get_contract(SECONDLIVE_CONTRACT, SECONDLIVE_ABI)

    @retry
    @check_gas
    async def sign_in(self):
        logger.info(f"[{self.account_id}][{self.address}] Start check-in on SecondLive")

        # Устанавливаем часовой пояс UTC+8
        timezone = pytz.timezone('Etc/GMT+8')

        # Получаем текущее время в UTC
        now_utc = datetime.now(pytz.utc)

        # Преобразуем время в часовой пояс UTC+8
        now_utc_plus_8 = now_utc.astimezone(timezone)

        # Форматируем дату
        formatted_date = int(now_utc_plus_8.strftime('%Y%m%d'))

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.signIn(formatted_date).build_transaction(tx_data)
        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())
