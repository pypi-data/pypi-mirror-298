# coding: utf-8

"""
    lakeFS API

    lakeFS HTTP API

    The version of the OpenAPI document: 1.0.0
    Contact: services@treeverse.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

import lakefs_sdk
from lakefs_sdk.api.commits_api import CommitsApi  # noqa: E501
from lakefs_sdk.rest import ApiException


class TestCommitsApi(unittest.TestCase):
    """CommitsApi unit test stubs"""

    def setUp(self):
        self.api = lakefs_sdk.api.commits_api.CommitsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_commit(self):
        """Test case for commit

        create commit  # noqa: E501
        """
        pass

    def test_get_commit(self):
        """Test case for get_commit

        get commit  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
