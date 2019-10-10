#!/usr/bin/env python
import requests
from data_structures import IdNode, MsgNode, tree

api_url = "https://my-json-server.typicode.com/AcckiyGerman/demo/messages/"


def get_comment_by_id(x):
    url = api_url + str(x)
    r = requests.get(url).json()
    print(f"request {x} finished: {r['message']}")
    return r["message"]


def map_tree(node):
    return MsgNode(
        message=get_comment_by_id(node.id),
        children=[map_tree(child) for child in node.children]
    )


message_tree = map_tree(tree)
