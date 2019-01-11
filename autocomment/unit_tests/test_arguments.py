from unittest.mock import Mock, MagicMock
from pycpp.arguments import arguments_factory
from pycpp.arguments import Argument
from pycpp.arguments import Arguments


def test_arguments_factory():

    testvector = [
        ('name0', 'type0', 'pass_by0'),
        ('name1', 'type1', 'pass_by1'),
        ('name2', 'type2', 'pass_by2')
    ]

    args = arguments_factory(testvector)

    assert len(args.arglist) == 3

    assert args.arglist[0] == Argument('name0', 'type0', 'pass_by0')
    assert args.arglist[1] == Argument('name1', 'type1', 'pass_by1')
    assert args.arglist[2] == Argument('name2', 'type2', 'pass_by2')


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

