import asyncio

from src.database.db_client import DBClient
from src.worker import run_worker


async def main():
    DBClient.create_db()
    await run_worker()

asyncio.run(main())
