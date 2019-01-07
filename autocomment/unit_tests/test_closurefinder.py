
import unittest
from pycpp.closurefinder import ClosureFinder
from pycpp.code import Token
from pycpp.code import Closure


class TestClosureFinder(unittest.TestCase):
    def test_closure_finder(self):
        closurefinder = ClosureFinder()

        for test in self.closure_finder_basic:
            closurefinder.input(test['input'])

            output = closurefinder.tree()
            self.assertEqual(len(output), len(
                test['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge")

            for element in zip(output, test['output']):
                self.assertEqual(element[0], element[1])

    closure_finder_basic = [{
        'input': [
            Token('CB_BEGIN', '{', 0),
            Token('CB_END', '}', 1)
        ],
        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 1),
                []
            )
        ]
    }, {
        'input': [
            Token('CB_BEGIN', '{', 0),
            Token('CB_BEGIN', '{', 1),
            Token('CB_END', '}', 2),
            Token('CB_END', '}', 3)
        ],

        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 3),
                [
                    Closure(
                        Token('CB_BEGIN', '{', 1),
                        Token('CB_END', '}', 2),
                        []
                    )
                ]
            )
        ]
    }, {
        'input': [
            Closure(
                [
                    Token('CB_BEGIN', '{', 0),
                    Token('CB_END', '}', 1)
                ]
            )
        ],

        'output': [
            Closure(
                [
                    Token('CB_BEGIN', '{', 0),
                    Token('CB_END', '}', 1)
                ]
            )
        ]
    }, {
        'input': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 3),
                [
                    Closure(
                        Token('CB_BEGIN', '{', 1),
                        Token('CB_END', '}', 2),
                        []
                    )
                ]
            )
        ],

        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 3),
                [
                    Closure(
                        Token('CB_BEGIN', '{', 1),
                        Token('CB_END', '}', 2),
                        []
                    )
                ]
            )
        ]
    }]


if __name__ == '__main__':
    unittest.main()
