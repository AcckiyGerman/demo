#!/usr/bin/env python
from dataclasses import dataclass
import typing
import trio
import asks

session = asks.sessions.Session(connections=5)


@dataclass
class Tree:
    id: int
    children: list
    value: 'typing.Any' = None

    def __str__(self, tab=""):
        return '\n'.join(
            [f"{tab}{self.id}: {self.value}"] + [child.__str__(tab + '\t') for child in self.children]
        )


async def map_tree(func, node):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(func, node)
        for child in node.children:
            nursery.start_soon(map_tree, func, child)


async def get_value_for_node(node):
    r = await session.get(f"https://jsonplaceholder.typicode.com/todos/{node.id}")
    print(f"id {node.id} {'ok' if r.status_code==200 else 'err'}")
    if r.status_code == 200:
        node.value = r.json()['title']


async def main(tree):
    await map_tree(get_value_for_node, tree)
    print('\n', tree)

trio.run(main, Tree(0, [Tree(2, [Tree(4, []), Tree(5, [])]), Tree(3, [])]))
