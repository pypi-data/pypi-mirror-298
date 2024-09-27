import functools
import inspect
import typing
from typing import TypeVar, Type, List, get_type_hints, cast
from unittest.mock import create_autospec, MagicMock, PropertyMock

T = TypeVar('T')


def spec_mock(spec: Type[T], strict: bool = True) -> T:
    return _spec_mock_inner(spec, strict)


def _spec_mock_inner(spec: Type[T], strict: bool, *, previous_classes: List[Type] = None) -> T:
    previous_classes = [spec, *(previous_classes if previous_classes else [])]

    mock_instance = create_autospec(spec, instance=True)
    init_signature = inspect.signature(spec.__init__)

    # Use typing.get_type_hints to resolve any string-based type annotations
    type_hints = get_type_hints(spec.__init__)

    for param_name, param in init_signature.parameters.items():
        if param_name == 'self':
            continue

        param_type = type_hints.get(param_name, None)
        # If it's a type from 'typing' then get its origin
        param_type = typing.get_origin(param_type) or param_type

        if param_type in previous_classes:
            # To avoid exceeding recursion depth, evaluate this lazily
            property_mock = PropertyMock(
                side_effect=functools.partial(
                    _cached_spec_mock_inner,
                    type(mock_instance),
                    param_name,
                    param_type,
                    strict,
                    previous_classes=previous_classes
                )
            )
            setattr(type(mock_instance), param_name, property_mock)
        else:
            if inspect.isclass(param_type):
                param_mock = _spec_mock_inner(cast(Type[T], param_type), strict, previous_classes=previous_classes)
            else:
                if strict:
                    class Empty:
                        pass

                    param_mock = MagicMock(spec_set=Empty)
                else:
                    param_mock = MagicMock()
            setattr(mock_instance, param_name, param_mock)

    return mock_instance


cache = {}


def _cached_spec_mock_inner(
        instance_type: Type,
        param_name: str,
        spec: Type[T],
        strict: bool,
        *,
        previous_classes: List[Type] = None
) -> T:
    if cached_result := cache.get((instance_type, param_name)):
        return cached_result
    cache[(instance_type, param_name)] = result = _spec_mock_inner(spec, strict, previous_classes=previous_classes)
    return result
