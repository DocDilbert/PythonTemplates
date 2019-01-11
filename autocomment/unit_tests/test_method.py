from unittest.mock import Mock, MagicMock
from pycpp.method import Method, MethodFactory


def test_method_factory():

    arguments = Mock()
    argument_factory = MagicMock()
    argument_factory.return_value = arguments
    method_factory = MethodFactory(argument_factory)

    method = method_factory(
        'name_token0',
        'returns0',
        'pass_by0',
        ['argument0', 'argument1'])

    assert method.name_token == 'name_token0'
    assert method.returns_token == 'returns0'
    assert method.pass_by == 'pass_by0'
    argument_factory.assert_called_with(['argument0', 'argument1'])
    assert method.arguments == arguments

def test_method_properties():

    name_token = MagicMock()
    name_token.val = "name"

    returns_token = MagicMock()
    returns_token.val = "returns"

    method = Method(
        name_token,
        returns_token,
        'pass_by',
        []
    )

    assert method.name == "name"
    assert method.returns == "returns"
