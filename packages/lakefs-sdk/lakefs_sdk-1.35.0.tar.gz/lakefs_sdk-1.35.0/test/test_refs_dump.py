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
import datetime

import lakefs_sdk
from lakefs_sdk.models.refs_dump import RefsDump  # noqa: E501
from lakefs_sdk.rest import ApiException

class TestRefsDump(unittest.TestCase):
    """RefsDump unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RefsDump
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RefsDump`
        """
        model = lakefs_sdk.models.refs_dump.RefsDump()  # noqa: E501
        if include_optional :
            return RefsDump(
                commits_meta_range_id = '', 
                tags_meta_range_id = '', 
                branches_meta_range_id = ''
            )
        else :
            return RefsDump(
                commits_meta_range_id = '',
                tags_meta_range_id = '',
                branches_meta_range_id = '',
        )
        """

    def testRefsDump(self):
        """Test RefsDump"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
