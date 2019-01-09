import pytest
from pycpp.code import Token
from pycpp.patternsearch import  PatternSearch
PATTERN_SEARCH_TESTS = [
    # {
    #     'description': "pattern_search_test_1",
    #     'search_pattern': ('A','B'),
    #     'input': [
    #         Token('A','a', 0), 
    #         Token('A','a', 1), 
    #         Token('B','a', 2), 
    #         Token('A','a', 3), 
    #         Token('A','a', 4)
    #     ],
    #     'output': [
    #         Token('A','a', 1), 
    #         Token('B','a', 2), 
    #     ]
    # }
]

@pytest.mark.parametrize("data", PATTERN_SEARCH_TESTS)
def test_pattern_search(data):
    patternsearch = PatternSearch()
    output = list(patternsearch.search(data['search_pattern'], data['input']))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
