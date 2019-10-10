#!/usr/bin/env python
from dataclasses import dataclass, field
import aiohttp
import asyncio


@dataclass
class IdNode:
    id: int
    children: list = field(default_factory=list)


@dataclass
class MsgNode:
    message: str
    children: list

    def __str__(self, indentation=""):
        message = f"{indentation}{self.message}"
        children_messages = [child.__str__(indentation + '\t') for child in self.children]
        return '\n'.join([message, *children_messages])


async def get_comment_by_id(x, session):
    r = await session.get(f"https://jsonplaceholder.typicode.com/todos/{x}")
    data = await r.json()
    print('request', x, 'finished')
    return data['title']


async def map_tree(node, session):
    message, children = await asyncio.gather(
        get_comment_by_id(node.id, session),
        asyncio.gather(*[map_tree(child, session) for child in node.children])
    )
    return MsgNode(message, children)


async def main():
    async with aiohttp.ClientSession() as session:
        message_tree = await map_tree(
            node=IdNode(1, [IdNode(2), IdNode(3, [IdNode(4), IdNode(5)])]),
            session=session
        )
        print('\n', message_tree)


asyncio.run(main())
