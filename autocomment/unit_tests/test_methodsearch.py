import pytest
from pycpp.code import Token, Block
from pycpp.blockfactory import BlockFactory
from pycpp.methodsearch import MethodSearch
from pycpp.lexer import Lexer
from pycpp.serializer import Serializer, getTokenSummary

PATTERN_SEARCH_TESTS = [
    {
        'description': "methodsearch_test_0",
        'input': '''
            // testMethod
            void testMethod();
        ''',
        'output': [{
            'returns': 39,
            'pass_by': -1,
            'name': 44,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type':  55,
                    'name':  58,
                    'pass_by': -1,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 59,
                    'pass_by': 58,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 60,
                    'name': 64,
                    'pass_by': 63,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 59,
                    'pass_by': 57,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 59,
                    'pass_by': 58,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 59,
                    'pass_by': 57,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 58,
                    'pass_by': -1,
                },
                {
                    'type': 62,
                    'name': 65,
                    'pass_by': -1,
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
            'returns': 89,
            'pass_by': -1,
            'name': 94,
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
            'returns': 205,
            'pass_by': -1,
            'name': 210,
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
                'returns': 90,
                'pass_by': -1,
                'name': 95,
                'args': []
            },
            {
                'returns': 158,
                'pass_by': -1,
                'name': 162,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
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
            'returns': 39,
            'pass_by': 42,
            'name': 44,
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
            'returns': 63,
            'pass_by': 66,
            'name': 68,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 79,
                    'name': 83,
                    'pass_by': 82,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 85,
                    'name': 89,
                    'pass_by' : 88,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 58,
                    'pass_by': -1,
                },
                {
                    'type': 91,
                    'name': 94,
                    'pass_by': -1,
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
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 55,
                    'name': 58,
                    'pass_by': -1,
                },
                {
                    'type': 91,
                    'name': 94,
                    'pass_by': -1,
                }
            ]
        }]
    },
    {
        'description': "methodsearch_test_18",
        'input': '''
            // testMethod
            void testMethod(
                Namespace::A1 a1
            );
        ''',
        'output': [{
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 83,
                    'name': 86,
                    'pass_by': -1,
                }
            ]
        }]
    },

]


def arguments_factory(argList):
    output = [
        {
            'name': name_pos,
            'type': type_pos,
            'pass_by': pass_by_pos
        } for (name_pos, type_pos, pass_by_pos) in argList
    ]
    return output

def method_factory(name_pos, returns_pos, pass_by_pos, arguments_generator):
    output = {'name': name_pos,
              'returns': returns_pos,
              'pass_by': pass_by_pos,
              'args': arguments_factory(arguments_generator)}
    return output

@pytest.mark.parametrize("data", PATTERN_SEARCH_TESTS)
def test_methodsearch(data):

    lexer = Lexer()
    lexer.input(data['input'])
    i1 = list(lexer.tokens())

    cb_factory = BlockFactory()
    i2 = cb_factory.tree(i1)


    patternsearch = MethodSearch(method_factory)

    serializer = Serializer()

    buf = serializer.toString(i2, getTokenSummary)

    output = list(patternsearch.search(buf, i2))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
