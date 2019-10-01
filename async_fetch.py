#!/usr/bin/env python
import aiohttp
import asyncio
from data_structures import IdNode, MsgNode, tree

api_url = "https://my-json-server.typicode.com/AcckiyGerman/demo/messages/"
messages = {}
tasks = []


async def get_comment_by_id(x, session):
    global messages
    url = api_url + str(x)
    r = await session.get(url)
    data = await r.json()
    messages[x] = data['message']
    print(f"request {x} finished")


def initiate_tasks(node, session):
    """ starts a task for each message id in the tree, but not await for result """
    global tasks
    tasks.append(get_comment_by_id(node.id, session))
    for child in node.children:
        initiate_tasks(child, session)


def map_tree(node):
    global messages
    return MsgNode(
        message=messages[node.id],
        children=[map_tree(child) for child in node.children]
    )


async def main():
    async with aiohttp.ClientSession() as session:
        initiate_tasks(tree, session)
        await asyncio.gather(*tasks)
        message_tree = map_tree(tree)
        print(message_tree)

if __name__ == "__main__":
    asyncio.run(main())
