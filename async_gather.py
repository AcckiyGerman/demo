#!/usr/bin/env python
from dataclasses import dataclass
import aiohttp
import asyncio


@dataclass
class IdNode:
    id: int
    children: list


@dataclass
class MsgNode:
    message: str
    children: list

    def __str__(self, indentation=""):
        return '\n'.join(
            [indentation + self.message] + [child.__str__(indentation + '\t') for child in self.children]
        )


async def get_comment_by_id(x, session):
    async with session.get(f"https://jsonplaceholder.typicode.com/todos/{x}") as res:
        data = await res.json()
        print('request', x, 'finished')
        return data['title']


async def map_tree(node, session):
    message, children = await asyncio.gather(
        get_comment_by_id(node.id, session),
        asyncio.gather(*[map_tree(child, session) for child in node.children])
    )
    return MsgNode(message, children)


async def main(tree):
    async with aiohttp.ClientSession() as session:
        message_tree = await map_tree(tree, session)
        print('\n', message_tree)


tree = IdNode(1, [IdNode(2, []), IdNode(3, [IdNode(4, []), IdNode(5, [])])])
asyncio.run(main(tree))
