from dataclasses import dataclass
import requests


@dataclass
class IdNode:
    id: int
    children: list


@dataclass
class MsgNode:
    message: str
    children: list


tree = IdNode(1, [
    IdNode(2, []),
    IdNode(3, [
        IdNode(4, []),
        IdNode(5, [])
    ])
])

print(tree)


def get_comment_by_id(x):
    return f"comment {x}"


def map_tree(func, node):
    return MsgNode(
        message=get_comment_by_id(node.id),
        children=[map_tree(func, child) for child in node.children]
    )


if __name__ == "__main__":
    message_tree = map_tree(get_comment_by_id, tree)
    print(message_tree)


r = requests.get('https://my-json-server.typicode.com/AcckiyGerman/demo/messages/1').json()
print(r['title'])