import pytest
from pycpp.code import Token, Block
from pycpp.blockfactory import BlockFactory
from pycpp.patternsearch import PatternSearch
from pycpp.lexer import Lexer

PATTERN_SEARCH_TESTS = [
    {
        'description': "pattern_search_test_1",
        'search_pattern': ('A', 'B'),
        'input': '''
            // testMethod
            void testMethod();
        ''',
        'output': [{
            'returns' : Token('STRING', 'void', 39),
            'name' : Token('STRING', 'testMethod', 44)
        }]
    },
    {
        'description': "pattern_search_test_1",
        'search_pattern': ('A', 'B'),
        'input': '''
            class testClass
            {
                // testMethod
                void testMethod();
            }
        ''',
        'output': [{
            'returns' : Token('STRING', 'void', 89),
            'name' : Token('STRING', 'testMethod', 94)
        }]
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
