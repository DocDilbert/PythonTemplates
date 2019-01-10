import pytest
from pycpp.code import Token, Block
from pycpp.blockfactory import BlockFactory
from pycpp.methodsearch import MethodSearch
from pycpp.lexer import Lexer

PATTERN_SEARCH_TESTS = [
    {
        'description': "methodsearch_test_0",
        'input': '''
            // testMethod
            void testMethod();
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': []
        }]
    },
    {
        'description': "methodsearch_test_1",
        'input': '''
            // testMethod
            void testMethod(A1 a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 58),
                    'pass_by' : 'value',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_2",
        'input': '''
            // testMethod
            void testMethod(A1 *a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59),
                    'pass_by' : 'pointer',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_3",
        'input': '''
            // testMethod
            void testMethod(ABC::A1 *a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 60),
                    'name': Token('STRING', 'a1', 64),
                    'pass_by' : 'pointer',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_4",
        'input': '''
            // testMethod
            void testMethod(A1* a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59),
                    'pass_by' : 'pointer',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_5",
        'input': '''
            // testMethod
            void testMethod(A1 &a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59),
                    'pass_by' : 'reference',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_6",
        'input': '''
            // testMethod
            void testMethod(A1& a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 59),
                    'pass_by' : 'reference',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_7",
        'input': '''
            // testMethod
            void testMethod(A1 a1, A2 a2);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 58),
                    'pass_by' : 'value',
                },
                {
                    'type': Token('STRING', 'A2', 62),
                    'name': Token('STRING', 'a2', 65),
                    'pass_by' : 'value',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_8",
        'input': '''
            class testClass
            {
                // testMethod
                void testMethod();
            }
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 89),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 94),
            'args': []
        }]
    },
    {
        'description': "methodsearch_test_9",
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
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 210),
            'args': []
        }]
    },
    {
        'description': "methodsearch_test_10",
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
                'pass_by': 'value',
                'name': Token('STRING', 'testMethod1', 95),
                'args': []
            },
            {
                'returns': Token('STRING', 'int', 158),
                'pass_by': 'value',
                'name': Token('STRING', 'testMethod2', 162),
                'args': []
            }
        ]
    },
    {
        'description': "methodsearch_test_11",
        'input': '''
            // testMethod
            void testMethod() const;
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': []
        }]
    },
    {
        'description': "methodsearch_test_12",
        'input': '''
            // testMethod
            int* testMethod() const;
        ''',
        'output': [{
            'returns': Token('STRING', 'int', 39),
            'pass_by': 'pointer',
            'name': Token('STRING', 'testMethod', 44),
            'args': []
        }]
    },
    {
        'description': "methodsearch_test_13",
        'input': '''
            // testMethod
            Namespace1::Namespace2::Var* testMethod() const;
        ''',
        'output': [{
            'returns': Token('STRING', 'Var', 63),
            'pass_by': 'pointer',
            'name': Token('STRING', 'testMethod', 68),
            'args': []
        }]
    },
    {
        'description': "methodsearch_test_14",
        'input': '''
            // testMethod
            void testMethod(Namespace1::Namespace2::A1 *a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 79),
                    'name': Token('STRING', 'a1', 83),
                    'pass_by' : 'pointer',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_15",
        'input': '''
            // testMethod
            void testMethod(const Namespace1::Namespace2::A1 *a1);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 85),
                    'name': Token('STRING', 'a1', 89),
                    'pass_by' : 'pointer',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_16",
        'input': '''
            // testMethod
            void testMethod(A1 a1, 
                            A2 a2);
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 58),
                    'pass_by' : 'value',
                },
                {
                    'type': Token('STRING', 'A2', 91),
                    'name': Token('STRING', 'a2', 94),
                    'pass_by' : 'value',
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_17",
        'input': '''
            // testMethod
            void testMethod(A1 a1, 
                            A2 a2
            );
        ''',
        'output': [{
            'returns': Token('STRING', 'void', 39),
            'pass_by': 'value',
            'name': Token('STRING', 'testMethod', 44),
            'args': [
                {
                    'type': Token('STRING', 'A1', 55),
                    'name': Token('STRING', 'a1', 58),
                    'pass_by' : 'value',
                },
                {
                    'type': Token('STRING', 'A2', 91),
                    'name': Token('STRING', 'a2', 94),
                    'pass_by' : 'value',
                }
            ]
        }]
    },
    
]


@pytest.mark.parametrize("data", PATTERN_SEARCH_TESTS)
def test_methodsearch(data):

    lexer = Lexer()
    lexer.input(data['input'])
    i1 = list(lexer.tokens())

    cb_factory = BlockFactory()
    i2 = cb_factory.tree(i1)

    patternsearch = MethodSearch()

    output = list(patternsearch.search(i2))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
