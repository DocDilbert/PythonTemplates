import unittest
from pycpp.code import Block
from pycpp.code import Token

def test_block_str_1():
    block = Block(
        Token('STRING', 'a', 0),
        Token('STRING', 'c', 2),
        [
            Token('STRING', 'b', 1)
        ]
    )

    assert '-->STRING("b"#1)' == str(block)


def test_block_str_2():
    block = Block(
        Token('STRING', 'a', 0),
        Token('STRING', 'c', 2),
        [
            Token('STRING', 'b', 1)
        ],
        trail_start="",
        trail_advance=""
    )

    assert 'STRING("b"#1)' == str(block)

def test_block_str_3():
    block = Block(
        Token('STRING', 'a', 0),
        Token('STRING', 'c', 4),
        [
            Block(
                Token('STRING', 'a', 1),
                Token('STRING', 'c', 3),
                [
                    Token('STRING', 'b', 2)
                ],
                trail_start="",
                trail_advance=""
            )
        ],
        trail_start="",
        trail_advance=""
    )

    assert 'STRING("b"#2)' == str(block)

