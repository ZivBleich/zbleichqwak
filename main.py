import asyncio
import aiohttp
import os
import sys
from typing import List, Tuple
from pydantic import BaseModel

"""
The time frame is not enough to do everything perfectly.
Git hub has an api that allows searching for issues.
The documenation is import because github has a rate limit.
We want to take queries from a file and pass them ("invoke") to github's issues api.
The final result needs to sum the results and concat the items to a single list.

Phase 1:
Can you estimate how much time it will take you?
1. load queries with regex ~ 5 minutes
2. execution ~ 30 minutes but depending on how clear the docs.
3. Print ~ 1 minute I guess.


Phase 2:
To control the parallelism with a parameter... maybe it is tricky  with asyncio 
I have the number of tasks to gather depend on that parameter.
"""


class Query(BaseModel):
    pass


class HttpClient:

    def __init__(self, session):
        self.session = session

    def get(self):
        pass


class Invoker:

    def __init__(self, queries_path: str, http_client):
        self.queries_path = queries_path
        self.queries: List[Query] = self._load_queries()
        self.http_client = http_client

    def _load_queries(self) -> List[Query]:
        return []

    async def invoke(self, queries: List[Query]) -> Tuple[int, List]:
        pass

    async def run(self):
        total_count = 0
        items = []

        # generate the tasks
        # run gather

    @staticmethod
    def display(total_count: int, items: []):
        print(total_count, items)


async def main():
    queries_path = sys.argv[1]
    invoker = Invoker(queries_path, HttpClient(aiohttp.ClientSession()))
    await invoker.run()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <main.py> <queries file>")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("Usage: <main.py> <queries file>")
        sys.exit(1)

    asyncio.run(main())
