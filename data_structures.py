from dataclasses import dataclass


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
