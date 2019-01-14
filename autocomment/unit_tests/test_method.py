from unittest.mock import Mock, MagicMock
from pycpp.method import Method, MethodFactory


def test_method_factory_1():

    arguments = Mock()
    argument_factory = Mock()
    argument_factory.return_value = arguments

    tokens = [
        Mock(pos=1),
        Mock(pos=2),
        Mock(pos=3),
        Mock(pos=4),
    ]
    method_factory = MethodFactory(tokens, argument_factory)

    method = method_factory(
        1,
        2,
        3,
        [4, 5]
    )

    assert method.name_token.pos == 1
    assert method.returns_token.pos == 2
    assert method.pass_by_token.pos == 3
    argument_factory.assert_called_with([4, 5])
    assert method.arguments == arguments

def test_method_factory_2():

    arguments = Mock()
    argument_factory = Mock()
    argument_factory.return_value = arguments

    tokens = [
        Mock(pos=1),
        Mock(pos=2),
        Mock(pos=30),
        Mock(pos=4),
    ]
    method_factory = MethodFactory(tokens, argument_factory)

    method = method_factory(
        1,
        2,
        3,
        [4, 5]
    )

    assert method.name_token.pos == 1
    assert method.returns_token.pos == 2
    assert method.pass_by_token is None
    argument_factory.assert_called_with([4, 5])
    assert method.arguments == arguments


def test_method_properties():
    method = Method(
        Mock(val = "name"),
        Mock(val = "returns"),
        'pass_by',
        []
    )

    assert method.name == "name"
    assert method.returns == "returns"


def test_method_str_0():
    mock = MagicMock()
    mock.__len__.return_value = 0
    mock.__str__.return_value = None

    method = Method(
        Mock(val='name0'),
        Mock(val='returns0'),
        'pass_by',
        mock
    )
    assert str(method) == '/// name0\n/// \\return'

def test_method_str_1():
    mock = MagicMock()
    mock.__len__.return_value = 0
    mock.__str__.return_value = None

    method = Method(
        Mock(val='name0'),
        Mock(val='returns0'),
        'pass_by',
        mock
    )
    method.return_description = "description"
    assert str(method) == '/// name0\n/// \\return description'

def test_method_str_2():
    mock = MagicMock()
    mock.__len__.return_value = 0
    mock.__str__.return_value = None

    method = Method(
        Mock(val='name0'),
        Mock(val='void'),
        'pass_by',
        mock
    )
    assert str(method) == '/// name0'


def test_method_str_3():
    mock = MagicMock()
    mock.__len__.return_value = 1
    mock.__str__.return_value = "/// \\param para"

    method = Method(
        Mock(val='name0'),
        Mock(val='returns0'),
        'pass_by',
        mock
    )
    assert str(method) == '/// name0\n/// \\param para\n/// \\return'

def test_method_str_4():
    mock = MagicMock()
    mock.__len__.return_value = 1
    mock.__str__.return_value = "/// \\param para"

    method = Method(
        Mock(val='name0'),
        Mock(val='returns0'),
        'pass_by',
        mock
    )
    method.return_description = "description"
    assert str(method) == '/// name0\n/// \\param para\n/// \\return description'

def test_method_str_5():
    mock = MagicMock()
    mock.__len__.return_value = 1
    mock.__str__.return_value = "/// \\param para"

    method = Method(
        Mock(val='name0'),
        Mock(val='void'),
        'pass_by',
        mock
    )
    assert str(method) == '/// name0\n/// \\param para'

def test_method_str_6():
    mock = MagicMock()
    mock.__len__.return_value = 1
    mock.__str__.return_value = "/// \\param para"

    method = Method(
        Mock(val='name0'),
        Mock(val='void'),
        'pass_by',
        mock
    )
    method.return_description = "description"
    assert str(method) == '/// name0\n/// \\param para'
