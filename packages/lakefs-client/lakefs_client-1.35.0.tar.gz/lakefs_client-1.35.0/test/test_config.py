"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import lakefs_client
from lakefs_client.model.storage_config import StorageConfig
from lakefs_client.model.version_config import VersionConfig
globals()['StorageConfig'] = StorageConfig
globals()['VersionConfig'] = VersionConfig
from lakefs_client.model.config import Config


class TestConfig(unittest.TestCase):
    """Config unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConfig(self):
        """Test Config"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Config()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
