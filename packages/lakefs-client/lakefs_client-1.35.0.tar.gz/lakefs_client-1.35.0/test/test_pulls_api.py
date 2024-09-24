"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import unittest

import lakefs_client
from lakefs_client.api.pulls_api import PullsApi  # noqa: E501


class TestPullsApi(unittest.TestCase):
    """PullsApi unit test stubs"""

    def setUp(self):
        self.api = PullsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_pull_request(self):
        """Test case for create_pull_request

        create pull request  # noqa: E501
        """
        pass

    def test_get_pull_request(self):
        """Test case for get_pull_request

        get pull request  # noqa: E501
        """
        pass

    def test_list_pull_requests(self):
        """Test case for list_pull_requests

        list pull requests  # noqa: E501
        """
        pass

    def test_update_pull_request(self):
        """Test case for update_pull_request

        update pull request  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
