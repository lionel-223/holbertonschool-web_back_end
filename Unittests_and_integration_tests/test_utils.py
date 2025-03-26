#!/usr/bin/env python3
"""
Unittest for utils.py
"""

import unittest
from utils import access_nested_map
from utils import get_json
from unittest.mock import Mock, patch
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """ Test the function access_nested_map """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test the function access_nested_map """
        self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])

    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ Test the function access_nested_map """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected}'")


class TestGetJson(unittest.TestCase):
    """ Test the function get_json """
    @parameterized.expand([
        ("http://example.comm", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """ Test that get_json returns the correct payload and calls requests.get once """
                # patch remplace 'requests.get' par un mock
        with patch("utils.requests.get") as mock_get:
            # On prépare un mock qui retournera un .json() simulé
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)