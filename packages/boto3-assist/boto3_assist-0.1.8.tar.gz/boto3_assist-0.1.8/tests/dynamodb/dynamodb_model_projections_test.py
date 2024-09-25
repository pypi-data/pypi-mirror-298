"""
Geek Cafe, LLC
Maintainers: Eric Wilson
MIT License.  See Project Root for the license information.
"""

import unittest


from tests.dynamodb.models.user_model import User
from tests.dynamodb.models.simple_model import Simple


class DynamoDBModeProjectionlUnitTest(unittest.TestCase):
    "Serialization Tests"

    def test_projection_expressions_transformation(self):
        """Test Basic Serlization"""
        # Arrange
        data = {
            "id": "123456",
            "first_name": "John",
            "age": 30,
            "email": "john@example.com",
            "status": "active",
        }

        # Act
        model: User = User().map(data)

        # Assert

        self.assertEqual(model.first_name, "John")
        self.assertEqual(model.age, 30)
        self.assertEqual(model.email, "john@example.com")
        self.assertIsInstance(model, User)

        key = model.indexes.primary.key()
        self.assertIsInstance(key, dict)

        expressions = model.projection_expression
        self.assertIsInstance(expressions, str)

        self.assertIn("#status", expressions)

        print(expressions)

        attribute_names = model.projection_expression_attribute_names
        self.assertIsInstance(attribute_names, dict)

        self.assertIn("#status", attribute_names)

        self.assertIn("status", attribute_names["#status"])

    def test_simple_model(self):
        """Test Basic Serlization"""
        # Arrange
        data = {
            "id": "123456",
        }

        # Act
        model: Simple = Simple().map(data)

        # Assert

        self.assertEqual(model.id, "123456")

        self.assertIsInstance(model, Simple)

        key = model.indexes.primary.key()
        self.assertIsInstance(key, dict)

        expressions = model.projection_expression
        self.assertIsInstance(expressions, str)

        self.assertIn("id", expressions)

        print(expressions)

        attribute_names = model.projection_expression_attribute_names
        self.assertIsNone(attribute_names)
