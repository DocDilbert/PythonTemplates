from unittest.mock import Mock, MagicMock
from pycpp.method import Method, MethodFactory


def test_arguments_factory():

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
