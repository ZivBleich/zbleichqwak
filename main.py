import asyncio
import aiohttp
import aiofiles
import os
import sys
from typing import List
from pydantic import BaseModel
from pprint import pprint

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
    """
    https://api.github.com/search/issues?q=factory in:file language:java repo:openjdk/jdk
    https://api.github.com/search/issues?q=cache in:file repo:scala/scala
    SEARCH_KEYWORD_1 SEARCH_KEYWORD_N QUALIFIER_1 QUALIFIER_N
    """
    full_query: str


class Result(BaseModel):
    total_count: int
    items: List


class HttpClient:
    """
    For unauthenticated requests, the rate limit allows you to make up to 10 requests per minute.
    """
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get(self, url: str):
        return await self.session.get(url)

    async def close_session(self):
        await self.session.close()


class Invoker:

    def __init__(self, queries_path: str, http_client: HttpClient):
        self.queries_path = queries_path
        self.http_client = http_client
        self.total_count = 0
        self.items = []

    async def _load_queries(self) -> List[Query]:
        queries = []
        async with aiofiles.open(self.queries_path) as fh:
            async for line in fh:
                queries.append(Query(full_query=line.strip()))

        return queries

    async def invoke(self, queries: List[Query]):
        for q in queries:
            try:
                response = await self.http_client.get(q.full_query)
                response.raise_for_status()
            except aiohttp.ClientResponseError as e:
                print(f"query {q.full_query} failed with {e}")
                continue
            j = await response.json()
            result = Result(**j)
            self.total_count += result.total_count
            self.items.extend(result.items)

    async def run(self):
        queries: List[Query] = await self._load_queries()
        tasks = [asyncio.create_task(self.invoke([q])) for q in queries]
        await asyncio.gather(*tasks)
        self.display()

    def display(self):
        pprint(self.total_count)
        pprint(self.items)


async def main():
    queries_path = sys.argv[1]
    http_client = HttpClient(aiohttp.ClientSession())
    invoker = Invoker(queries_path, http_client)
    await invoker.run()
    await http_client.close_session()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <main.py> <queries file>")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("Usage: <main.py> <queries file>")
        sys.exit(1)

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
