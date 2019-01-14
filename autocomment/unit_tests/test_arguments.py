from unittest.mock import Mock, MagicMock
from pycpp.arguments import ArgumentsFactory
from pycpp.arguments import Argument
from pycpp.arguments import Arguments


def test_arguments_factory():

    testvector = [
        (0, 1, 2),
        (1, 2, 3),
        (4, 5, 6)
    ]
    tokens = [
        Mock(pos=0),
        Mock(pos=1),
        Mock(pos=2),
        Mock(pos=3),
        Mock(pos=4),
        Mock(pos=5),
        Mock(pos=6),
    ]
    arguments_factory = ArgumentsFactory(tokens)
    args = arguments_factory(testvector)

    assert len(args.arglist) == 3

    assert args.arglist[0].name_token.pos == 0
    assert args.arglist[0].type_token.pos == 1
    assert args.arglist[0].pass_by_token.pos  == 2

    assert args.arglist[1].name_token.pos == 1
    assert args.arglist[1].type_token.pos == 2
    assert args.arglist[1].pass_by_token.pos  == 3

    assert args.arglist[2].name_token.pos == 4
    assert args.arglist[2].type_token.pos == 5
    assert args.arglist[2].pass_by_token.pos  == 6



def test_arguments_len():

    args = Arguments()

    args.add('name', 'type', 'pass_by')
    assert len(args) == 1

    args.add('name', 'type', 'pass_by')
    assert len(args) == 2


def test_arguments_iter():

    args = Arguments()

    args.add('name', 'type', 'pass_by')
    args.add('name', 'type', 'pass_by')

    results = list(args)
    assert len(results) == 2
    

def test_argument_properties():

    name_token = MagicMock()
    name_token.val = "name"

    type_token = MagicMock()
    type_token.val = "type"

    arg = Argument(
        name_token,
        type_token,
        'pass_by'
    )

    assert arg.name == "name"
    assert arg.type == "type"

def test_argument_str():
    arg = Argument(
        Mock(val="name"),
        Mock(val="type"),
        'pass_by'
    )

    assert str(arg)== "/// \\param name"

    arg.description = "description"
    assert str(arg) == "/// \\param name description"

def test_arguments_str():
    args = Arguments()

    assert str(args)== ""

    args.add(Mock(val="name0"),
             Mock(val="type0"),
             'pass_by')
    args.add(Mock(val="name1"),
             Mock(val="type1"),
             'pass_by')

    assert str(args)== "/// \\param name0\n/// \\param name1"

    argiter = iter(args)
    next(argiter).description = "description0"
    next(argiter).description = "description1"

    assert str(args)== "/// \\param name0 description0\n/// \\param name1 description1"

