"""
some tests for pytmx

WIP - all code that isn't abandoned is WIP
"""
from unittest import TestCase, skip
import sys

# from mock import Mock, patch

import pytmx
from pytmx import convert_to_bool
from pytmx import TiledElement


class TiledMapTest(TestCase):
    filename = 'test01.tmx'

    def setUp(self):
        self.m = pytmx.TiledMap(self.filename)

    def test_get_tile_image(self):
        image = self.m.get_tile_image(0, 0, 0)

    def test_get_tile_image_by_gid(self):
        image = self.m.get_tile_image_by_gid(0)
        self.assertIsNone(image)

        image = self.m.get_tile_image_by_gid(1)
        self.assertIsNotNone(image)

    @skip('Need to make a better test')
    def test_import_pytmx_doesnt_import_pygame(self):
        self.assertTrue('pygame' not in sys.modules)


class handle_bool_TestCase(TestCase):
    def test_when_passed_true_it_should_return_true(self):
        self.assertTrue(convert_to_bool("true"))

    def test_when_passed_yes_it_should_return_true(self):
        self.assertTrue(convert_to_bool("yes"))

    def test_when_passed_false_it_should_return_false(self):
        self.assertFalse(convert_to_bool("false"))

    def test_when_passed_no_it_should_return_false(self):
        self.assertFalse(convert_to_bool("no"))

    def test_when_passed_zero_it_should_return_false(self):
        self.assertFalse(convert_to_bool("0"))

    def test_when_passed_non_zero_it_should_return_true(self):
        self.assertTrue(convert_to_bool("1337"))

    def test_when_passed_garbage_it_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_bool("garbage")

    def test_when_passed_None_it_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            convert_to_bool(None)


class TiledElementTestCase(TestCase):
    def setUp(self):
        self.element = TiledElement()

    def test_from_xml_string_should_raise_on_TiledElement(self):
        with self.assertRaises(AttributeError):
            TiledElement.from_xml_string("<element></element>")

    def test_contains_reserved_property_name(self):
        """ Reserved names are checked from any attributes in the instance
            after it is created.  Instance attributes are defaults from the
            specification.  We check that new properties are not named same
            as existing attributes.
        """
        self.element.name ='foo'
        items = {'name': None}
        result = self.element.contains_invalid_property_name(items.items())
        self.assertTrue(result)

    def test_not_contains_reserved_property_name(self):
        """ Reserved names are checked from any attributes in the instance
            after it is created.  Instance attributes are defaults from the
            specification.  We check that new properties are not named same
            as existing attributes.
        """
        items = {'name': None}
        result = self.element.contains_invalid_property_name(items.items())
        self.assertFalse(result)

    def test_reserved_names_check_disabled_with_option(self):
        """ Reserved names are checked from any attributes in the instance
            after it is created.  Instance attributes are defaults from the
            specification.  We check that new properties are not named same
            as existing attributes.

            Check that passing an option will disable the check
        """
        pytmx.TiledElement.allow_duplicate_names = True
        self.element.name = 'foo'
        items = {'name': None}
        result = self.element.contains_invalid_property_name(items.items())
        self.assertFalse(result)

    def test_repr(self):
        self.element.name = 'foo'
        self.assertEqual("<TiledElement: \"foo\">", self.element.__repr__())
