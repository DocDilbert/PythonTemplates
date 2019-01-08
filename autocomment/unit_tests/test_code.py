import unittest
from pycpp.code import Block
from pycpp.code import Token

def test_block_str():
    Block(
        Token('STRING', 'a', 0),
        Token('STRING', 'a', 1),
        [
            Token('STRING', 'a', 2)
        ]
    )
