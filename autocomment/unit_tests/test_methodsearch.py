import pytest
from pycpp.methodsearch import MethodSearch


PATTERN_SEARCH_TESTS = [
    {
        #
        # // testMethod
        # void testMethod();
        #
        'description': "methodsearch_test_0",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_(39)STRING_"
                 "(43)WS_(44)STRING_(54)LP_(55)RP_(56)EOC_(57)NL_(58)WS_",
        'output': [{
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': []
        }]
    },
    {
        #
        # // testMethod
        # void testMethod(A1 a1);
        #
        'description': "methodsearch_test_1",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_(39)STRING_"
                 "(43)WS_(44)STRING_(54)LP_(55)STRING_(57)WS_(58)STRING_(60)RP_"
                 "(61)EOC_(62)NL_(63)WS_",
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
        #
        # // testMethod
        # void testMethod(A1 *a1);
        #
        'description': "methodsearch_test_2",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_(39)STRING_(43)WS_"
                 "(44)STRING_(54)LP_(55)STRING_(57)WS_(58)MULTIPLY_(59)STRING_(61)RP_"
                 "(62)EOC_(63)NL_(64)WS_",
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
        #
        # // testMethod
        # void testMethod(ABC::A1 *a1);
        #
        'description': "methodsearch_test_3",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_(39)STRING_(43)WS_"
                 "(44)STRING_(54)LP_(55)STRING_(58)2COLONS_(60)STRING_(62)WS_(63)MULTIPLY_"
                 "(64)STRING_(66)RP_(67)EOC_(68)NL_(69)WS_",
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
        #
        # // testMethod
        # void testMethod(A1* a1);
        #
        'description': "methodsearch_test_4",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_(39)STRING_(43)WS_"
                 "(44)STRING_(54)LP_(55)STRING_(57)MULTIPLY_(58)WS_(59)STRING_"
                 "(61)RP_(62)EOC_(63)NL_(64)WS_",
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
        #
        # // testMethod
        # void testMethod(A1 &a1);
        #
        'description': "methodsearch_test_5",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_"
                 "(39)STRING_(43)WS_(44)STRING_(54)LP_(55)STRING_(57)WS_"
                 "(58)AND_(59)STRING_(61)RP_(62)EOC_(63)NL_(64)WS_",
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
        #
        # // testMethod
        # void testMethod(A1& a1);
        #
        'description': "methodsearch_test_6",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_"
                 "(39)STRING_(43)WS_(44)STRING_(54)LP_(55)STRING_(57)AND_"
                 "(58)WS_(59)STRING_(61)RP_(62)EOC_(63)NL_(64)WS_",
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
        #
        # // testMethod
        # void testMethod(A1 a1, A2 a2);
        #
        'description': "methodsearch_test_7",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_"
                 "(39)STRING_(43)WS_(44)STRING_(54)LP_(55)STRING_(57)WS_"
                 "(58)STRING_(60)COMMA_(61)WS_(62)STRING_(64)WS_(65)STRING_"
                 "(67)RP_(68)EOC_(69)NL_(70)WS_",
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
        #
        # class testClass
        # {
        #   // testMethod
        #   void testMethod();
        # }
        #
        'description': "methodsearch_test_8",
        'input': "(0)NL_(1)WS_(13)STRING_(18)WS_(19)STRING_(28)NL_(29)WS_"
                 "(41)BEGIN_(42)NL_(43)WS_(59)COMMENT_(61)WS_(62)STRING_"
                 "(72)NL_(73)WS_(89)STRING_(93)WS_(94)STRING_(104)LP_"
                 "(105)RP_(106)EOC_(107)NL_(108)WS_(120)END_(121)NL_(122)WS_",
        'output': [{
            'returns': 89,
            'pass_by': -1,
            'name': 94,
            'args': []
        }]
    },
    {
        # // testClass1
        # class testClass1
        # {
        #   // testClass2
        #   class testClass2
        #   {
        #       // testMethod
        #       void testMethod();
        #   }
        # }
        #
        'description': "methodsearch_test_9",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_"
                 "(39)STRING_(44)WS_(45)STRING_(55)NL_(56)WS_(68)BEGIN_"
                 "(69)NL_(70)WS_(86)COMMENT_(88)WS_(89)STRING_(99)NL_"
                 "(100)WS_(116)STRING_(121)WS_(122)STRING_(132)NL_"
                 "(133)WS_(149)BEGIN_(150)NL_(151)WS_(171)COMMENT_"
                 "(173)WS_(174)STRING_(184)NL_(185)WS_(205)STRING_"
                 "(209)WS_(210)STRING_(220)LP_(221)RP_(222)EOC_(223)NL_"
                 "(224)WS_(240)END_(241)NL_(242)WS_(254)END_(255)NL_(256)WS_",
        'output': [{
            'returns': 205,
            'pass_by': -1,
            'name': 210,
            'args': []
        }]
    },
    {
        #
        # class testClass
        # {
        #   // testMethod1
        #   void testMethod1();

        #   // testMethod2
        #   int testMethod2();
        # }
        #
        'description': "methodsearch_test_10",
        'input': "(0)NL_(1)WS_(13)STRING_(18)WS_(19)STRING_(28)NL_"
                 "(29)WS_(41)BEGIN_(42)NL_(43)WS_(59)COMMENT_(61)WS_"
                 "(62)STRING_(73)NL_(74)WS_(90)STRING_(94)WS_"
                 "(95)STRING_(106)LP_(107)RP_(108)EOC_(109)NL_"
                 "(110)NL_(111)WS_(127)COMMENT_(129)WS_(130)STRING_"
                 "(141)NL_(142)WS_(158)STRING_(161)WS_(162)STRING_"
                 "(173)LP_(174)RP_(175)EOC_(176)NL_(177)WS_"
                 "(189)END_(190)NL_(191)WS_",
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
        #
        # // testMethod
        # void testMethod() const;
        #
        'description': "methodsearch_test_11",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(43)WS_(44)STRING_(54)LP_(55)RP_"
                 "(56)WS_(57)CONST_(62)EOC_(63)NL_(64)WS_",
        'output': [{
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': []
        }]
    },
    {
        #
        # // testMethod
        # int* testMethod() const;
        #
        'description': "methodsearch_test_12",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(42)MULTIPLY_(43)WS_(44)STRING_"
                 "(54)LP_(55)RP_(56)WS_(57)CONST_(62)EOC_(63)NL_(64)WS_",
        'output': [{
            'returns': 39,
            'pass_by': 42,
            'name': 44,
            'args': []
        }]
    },
    {
        #
        # // testMethod
        # Namespace1::Namespace2::Var* testMethod() const;
        #
        'description': "methodsearch_test_13",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(49)2COLONS_(51)STRING_"
                 "(61)2COLONS_(63)STRING_(66)MULTIPLY_(67)WS_"
                 "(68)STRING_(78)LP_(79)RP_(80)WS_(81)CONST_"
                 "(86)EOC_(87)NL_(88)WS_",
        'output': [{
            'returns': 63,
            'pass_by': 66,
            'name': 68,
            'args': []
        }]
    },
    {
        #
        # // testMethod
        # void testMethod(Namespace1::Namespace2::A1 *a1);
        #
        'description': "methodsearch_test_14",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(43)WS_(44)STRING_(54)LP_"
                 "(55)STRING_(65)2COLONS_(67)STRING_(77)2COLONS_"
                 "(79)STRING_(81)WS_(82)MULTIPLY_(83)STRING_"
                 "(85)RP_(86)EOC_(87)NL_(88)WS_",
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
        #
        # // testMethod
        # void testMethod(const Namespace1::Namespace2::A1 *a1);
        #
        'description': "methodsearch_test_15",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(43)WS_(44)STRING_(54)LP_"
                 "(55)CONST_(60)WS_(61)STRING_(71)2COLONS_(73)STRING_"
                 "(83)2COLONS_(85)STRING_(87)WS_(88)MULTIPLY_"
                 "(89)STRING_(91)RP_(92)EOC_(93)NL_(94)WS_",
        'output': [{
            'returns': 39,
            'pass_by': -1,
            'name': 44,
            'args': [
                {
                    'type': 85,
                    'name': 89,
                    'pass_by': 88,
                }
            ]
        }]
    },
    {
        #
        #  // testMethod
        #  void testMethod(A1 a1,
        #                  A2 a2);
        #
        'description': "methodsearch_test_16",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_(27)WS_"
                 "(39)STRING_(43)WS_(44)STRING_(54)LP_(55)STRING_(57)WS_"
                 "(58)STRING_(60)COMMA_(61)WS_(62)NL_(63)WS_(91)STRING_"
                 "(93)WS_(94)STRING_(96)RP_(97)EOC_(98)NL_(99)WS_",
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
        #
        # // testMethod
        # void testMethod(A1 a1,
        #                 A2 a2
        # );
        #
        'description': "methodsearch_test_17",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(43)WS_(44)STRING_(54)LP_(55)STRING_"
                 "(57)WS_(58)STRING_(60)COMMA_(61)WS_(62)NL_(63)WS_"
                 "(91)STRING_(93)WS_(94)STRING_(96)NL_(97)WS_"
                 "(109)RP_(110)EOC_(111)NL_(112)WS_",
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
        #
        # // testMethod
        # void testMethod(
        #   Namespace::A1 a1
        # );
        #
        'description': "methodsearch_test_18",
        'input': "(0)NL_(1)WS_(13)COMMENT_(15)WS_(16)STRING_(26)NL_"
                 "(27)WS_(39)STRING_(43)WS_(44)STRING_(54)LP_"
                 "(55)NL_(56)WS_(72)STRING_(81)2COLONS_(83)STRING_"
                 "(85)WS_(86)STRING_(88)NL_(89)WS_(101)RP_"
                 "(102)EOC_(103)NL_(104)WS_",
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
    {
        # // testMethod
        # void testMethod(Namespace::A1 a1)
        # {
        #   Code
        # }
        'description': "methodsearch_test_19",
        'input': "(0)WS_(1)NL_(2)WS_(10)COMMENT_(12)WS_(13)STRING_(23)NL_"
                 "(24)WS_(32)STRING_(36)WS_(37)STRING_(47)LP_(48)STRING_"
                 "(57)2COLONS_(59)STRING_(61)WS_(62)STRING_(64)RP_(65)NL_"
                 "(66)WS_(74)BEGIN_(75)NL_(76)WS_(86)STRING_(90)NL_"
                 "(91)WS_(99)END_(100)NL_(101)WS_",
        'output': [{
            'returns': 32,
            'pass_by': -1,
            'name': 37,
            'args': [
                {
                    'type': 59,
                    'name': 62,
                    'pass_by': -1,
                }
            ]
        }]
    },
    {
        #
        # // testMethod
        # void Namespace::testMethod(Namespace::A1 a1)
        # {
        #   Code
        # }
        #
        'description': "methodsearch_test_20",
        'input': "(0)WS_(1)NL_(2)WS_(10)COMMENT_(12)WS_(13)STRING_"
                 "(23)NL_(24)WS_(32)STRING_(36)WS_(37)STRING_(46)2COLONS_"
                 "(48)STRING_(58)LP_(59)STRING_(68)2COLONS_(70)STRING_"
                 "(72)WS_(73)STRING_(75)RP_(76)NL_(77)WS_(85)BEGIN_"
                 "(86)NL_(87)WS_(97)STRING_(101)NL_(102)WS_(110)END_"
                 "(111)NL_(112)WS_",
        'output': [{
            'returns': 32,
            'pass_by': -1,
            'name': 48,
            'args': [
                {
                    'type': 70,
                    'name': 73,
                    'pass_by': -1,
                }
            ]
        }]
    },
    {
        #
        # FLOAT32 method (FLOAT32 p);
        #
        'description': "methodsearch_test_21",
        'input': "(0)WS_(1)NL_(2)WS_(10)STRING_(17)WS_(18)STRING_(24)WS_"
                 "(25)LP_(26)STRING_(33)WS_(34)STRING_(35)RP_(36)EOC_"
                 "(37)NL_(38)WS_",
        'output': [{
            'returns': 10,
            'pass_by': -1,
            'name': 18,
            'args': [
                {
                    'type': 26,
                    'name': 34,
                    'pass_by': -1,
                }
            ]
        }]
    },
    {
        #
        # FLOAT32 method (FLOAT32 p = TEXT);
        #
        'description': "methodsearch_test_22",
        'input': "(0)WS_(1)NL_(2)WS_(10)STRING_(17)WS_(18)STRING_(24)WS_"
                 "(25)LP_(26)STRING_(33)WS_(34)STRING_(35)WS_"
                 "(36)EQUALS_(37)WS_(38)STRING_(42)RP_(43)EOC_(44)NL_(45)WS_",
        'output': [{
            'returns': 10,
            'pass_by': -1,
            'name': 18,
            'args': [
                {
                    'type': 26,
                    'name': 34,
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
    patternsearch = MethodSearch(method_factory)
    output = list(patternsearch.search(data['input']))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
