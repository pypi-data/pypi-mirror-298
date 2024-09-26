import ast
import unittest
from aind_flake8_extensions.plugin import run_ast_checks


class TestPlugin(unittest.TestCase):

    def check_code(self, code: str):
        """Helper method to run the PydanticFieldChecker on the provided code."""
        tree = ast.parse(code)
        return list(run_ast_checks(tree))

    def test_datetime(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    timestamp: datetime = Field(..., default_factory=datetime.now)
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF003 Field 'timestamp' should use 'AwareDatetimeWithDefault' instead of datetime")

    def test_datetime_correct(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    timestamp: AwareDatetimeWithDefault = Field(...)
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
