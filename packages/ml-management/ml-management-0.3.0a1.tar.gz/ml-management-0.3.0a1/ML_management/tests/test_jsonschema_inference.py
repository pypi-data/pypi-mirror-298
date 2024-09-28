import unittest
from typing import Dict, List, Optional, Union

from ML_management.mlmanagement.jsonschema_exceptions import (
    DictKeysMustBeStringsError,
    FunctionContainsVarArgsError,
    FunctionContainsVarKwArgsError,
    InvalidStructureAnnotationError,
    NoAnnotationError,
    UnsupportedTypeError,
)
from ML_management.mlmanagement.jsonschema_inference import infer_jsonschema


class TestJsonschemaInference(unittest.TestCase):
    def test_jsonschema_generation(self):
        """Tests automatic jsonschema generation from functions signature."""

        def one_1(
            *,
            a: int,
            b: Optional[int],
            c: bool,
            d: Union[int, str],
            e: Dict[str, List[int]],
            f: List[float],
            g: float = 3.23,
        ):
            pass

        result = infer_jsonschema(one_1)
        result["required"].sort()
        expected_result = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": ["integer", "null"]},
                "c": {"type": "boolean"},
                "d": {"anyOf": [{"type": "integer"}, {"type": "string"}]},
                "e": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "integer"},
                    },
                },
                "f": {"type": "array", "items": {"type": "number"}},
                "g": {"type": "number", "default": 3.23},
            },
            "required": ["a", "c", "d", "e", "f"],
            "additionalProperties": False,
        }
        self.assertDictEqual(result, expected_result)

        def one_2(
            a: int,
            b: Optional[int],
            c: bool,
            d: Union[int, str],
            *,
            e: Dict[str, List[int]],
            f: List[float],
            g: float = 3.23,
        ):
            pass

        result = infer_jsonschema(one_2)
        result["required"].sort()
        self.assertDictEqual(result, expected_result)

        def one_3(
            a: int,
            b: Optional[int],
            c: bool,
            d: Union[int, str],
            e: Dict[str, List[int]],
            f: List[float],
            g: float = 3.23,
        ):
            pass

        result = infer_jsonschema(one_3)
        result["required"].sort()
        self.assertDictEqual(result, expected_result)

        def two(a):
            pass

        self.assertRaises(NoAnnotationError, infer_jsonschema, two)

        def three(a: complex):
            pass

        self.assertRaises(UnsupportedTypeError, infer_jsonschema, three)

        def four(a: Dict[int, str]):
            pass

        self.assertRaises(DictKeysMustBeStringsError, infer_jsonschema, four)

        class SomeType:
            def __init__(self) -> None:
                pass

        def five(a: SomeType):
            pass

        self.assertRaises(UnsupportedTypeError, infer_jsonschema, five)

        def six(a: int, **kwargs):
            pass

        self.assertRaises(FunctionContainsVarKwArgsError, infer_jsonschema, six)

        def seven(a: int, *args):
            pass

        self.assertRaises(FunctionContainsVarArgsError, infer_jsonschema, seven)

        def eight(a: List):
            pass

        self.assertRaises(InvalidStructureAnnotationError, infer_jsonschema, eight)


if __name__ == "__main__":
    unittest.main()
