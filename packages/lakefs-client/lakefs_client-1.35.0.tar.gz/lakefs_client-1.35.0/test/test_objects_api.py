"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import unittest

import lakefs_client
from lakefs_client.api.objects_api import ObjectsApi  # noqa: E501


class TestObjectsApi(unittest.TestCase):
    """ObjectsApi unit test stubs"""

    def setUp(self):
        self.api = ObjectsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_copy_object(self):
        """Test case for copy_object

        create a copy of an object  # noqa: E501
        """
        pass

    def test_delete_object(self):
        """Test case for delete_object

        delete object. Missing objects will not return a NotFound error.  # noqa: E501
        """
        pass

    def test_delete_objects(self):
        """Test case for delete_objects

        delete objects. Missing objects will not return a NotFound error.  # noqa: E501
        """
        pass

    def test_get_object(self):
        """Test case for get_object

        get object content  # noqa: E501
        """
        pass

    def test_get_underlying_properties(self):
        """Test case for get_underlying_properties

        get object properties on underlying storage  # noqa: E501
        """
        pass

    def test_head_object(self):
        """Test case for head_object

        check if object exists  # noqa: E501
        """
        pass

    def test_list_objects(self):
        """Test case for list_objects

        list objects under a given prefix  # noqa: E501
        """
        pass

    def test_stat_object(self):
        """Test case for stat_object

        get object metadata  # noqa: E501
        """
        pass

    def test_upload_object(self):
        """Test case for upload_object

        """
        pass


if __name__ == '__main__':
    unittest.main()
