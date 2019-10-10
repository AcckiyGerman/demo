# https://habr.com/ru/post/469441/#comment_20717375

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Generic, Sequence, TypeVar

from aiohttp import ClientSession

T = TypeVar("T")


@dataclass
class Comment:
    id: int
    title: str

    def __repr__(self):
        return f"{self.id} - {self.title}"


@dataclass
class Tree(Generic[T]):
    value: T
    children: Sequence[Tree] = field(default_factory=list)

    def print(self, indentation: str = "") -> None:
        print(f"{indentation}{self.value}")

        for child in self.children:
            child.print(indentation + "\t")


async def get_comment(client: ClientSession, id: int) -> Comment:
    async with client.get(f"https://jsonplaceholder.typicode.com/todos/{id}") as resp:
        raw_comment = await resp.json()
        print(f"request {id} finished: {raw_comment['title']}")
        return Comment(id=raw_comment["id"], title=raw_comment["title"])


async def get_comments_tree(client: ClientSession, tree: Tree[int]):
    children = [get_comments_tree(client, child) for child in tree.children]
    value = await get_comment(client, tree.value)
    chilren_results = await asyncio.gather(*children)
    return Tree[Comment](value, chilren_results)


async def main():
    async with ClientSession() as client:
        tree = Tree(1, children=[Tree(2), Tree(3, children=[Tree(4), Tree(5)])])
        tree.print()

        comment_tree = await get_comments_tree(client, tree)
        comment_tree.print()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())