import pytest
from pycpp.code import Token, Block
from pycpp.blockfactory import BlockFactory
from pycpp.patternsearch import PatternSearch
from pycpp.lexer import Lexer

PATTERN_SEARCH_TESTS = [
    {
        'description': "pattern_search_test_0",
        'input': '''
            // testMethod
            void testMethod();
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': []
        }]
    },
    {
        'description': "pattern_search_test_1",
        'input': '''
            // testMethod
            void testMethod(A1 a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 58)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_1",
        'input': '''
            // testMethod
            void testMethod(A1 *a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_1",
        'input': '''
            // testMethod
            void testMethod(ABC::A1 *a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 60),
                    'name': Token('STRING', 'a1', 64)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_1",
        'input': '''
            // testMethod
            void testMethod(A1* a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_1",
        'input': '''
            // testMethod
            void testMethod(A1 &a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_1",
        'input': '''
            // testMethod
            void testMethod(A1& a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_2",
        'input': '''
            // testMethod
            void testMethod(A1 a1, A2 a2);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 58)
                },
                {
                    'type': Token('STRING', 'A2', 62),
                    'name': Token('STRING', 'a2', 65)
                }
            ]
        }]
    },
    {
        'description': "pattern_search_test_3",
        'input': '''
            class testClass
            {
                // testMethod
                void testMethod();
            }
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 89),
            'name': Token('STRING', 'testMethod', 94),
            'args': []
        }]
    },
    {
        'description': "pattern_search_test_4",
        'input': '''
            // testClass1
            class testClass1
            {
                // testClass2
                class testClass2
                {
                    // testMethod
                    void testMethod();
                }
            }
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 205),
            'name': Token('STRING', 'testMethod', 210),
            'args': []
        }]
    },
    {
        'description': "pattern_search_test_5",
        'input': '''
            class testClass
            {
                // testMethod1
                void testMethod1();

                // testMethod2
                int testMethod2();
            }
        ''',
        'output': [
            {
                'returns': Token('STRING', 'void', 90),
                'name': Token('STRING', 'testMethod1', 95),
                'args': []
            },
            {
                'returns': Token('STRING', 'int', 158),
                'name': Token('STRING', 'testMethod2', 162),
                'args': []
            }
        ]
    }
]


@pytest.mark.parametrize("data", PATTERN_SEARCH_TESTS)
def test_pattern_search(data):

    lexer = Lexer()
    lexer.input(data['input'])
    i1 = list(lexer.tokens())

    cb_factory = BlockFactory()
    i2 = cb_factory.tree(i1)

    patternsearch = PatternSearch()

    output = list(patternsearch.search(i2))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
