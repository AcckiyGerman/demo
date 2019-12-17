#!/usr/bin/env python
from dataclasses import dataclass
import typing
import trio
import asks

session = asks.sessions.Session(connections=2)


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
        # get the value from API and set it asynchronously
        nursery.start_soon(func, node)
        for child in node.children:
            nursery.start_soon(map_tree, func, child)


async def get_value_for_node(node):
    res = await session.get(f"https://jsonplaceholder.typicode.com/todos/{node.id}")
    data = res.json()
    print(f'response {node.id}: {data}')
    node.value = data['title']


async def main():
    tree = Tree(1, [Tree(2, [Tree(4, []), Tree(5, [])]), Tree(3, [])])
    print(tree)

    await map_tree(get_value_for_node, tree)
    print(tree)


trio.run(main)
