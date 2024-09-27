import inspect
from typing import TypeVar, Type, List, get_type_hints, cast
from unittest.mock import create_autospec, MagicMock, PropertyMock


T = TypeVar('T')


def spec_mock(cls: Type[T], previous_classes: List[Type] = None) -> T:
    previous_classes = [cls, *(previous_classes if previous_classes else [])]

    mock_instance = create_autospec(cls, instance=True)
    init_signature = inspect.signature(cls.__init__)

    # Use typing.get_type_hints to resolve any string-based type annotations
    type_hints = get_type_hints(cls.__init__)

    for param_name, param in init_signature.parameters.items():
        if param_name == 'self':
            continue

        param_type = type_hints.get(param_name, None)

        if param_type in previous_classes:  # To avoid exceeding recursion depth, evaluate this lazily
            property_mock = PropertyMock(side_effect=lambda: spec_mock(param_type, previous_classes))
            setattr(type(mock_instance), param_name, property_mock)
        else:
            if inspect.isclass(param_type):
                param_mock = spec_mock(cast(Type[T], param_type), previous_classes)
            else:
                param_mock = MagicMock()
            setattr(mock_instance, param_name, param_mock)

    return mock_instance
