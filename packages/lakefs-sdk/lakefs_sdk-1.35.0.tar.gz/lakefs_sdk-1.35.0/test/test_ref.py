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
from lakefs_sdk.models.ref import Ref  # noqa: E501
from lakefs_sdk.rest import ApiException

class TestRef(unittest.TestCase):
    """Ref unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Ref
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Ref`
        """
        model = lakefs_sdk.models.ref.Ref()  # noqa: E501
        if include_optional :
            return Ref(
                id = '', 
                commit_id = ''
            )
        else :
            return Ref(
                id = '',
                commit_id = '',
        )
        """

    def testRef(self):
        """Test Ref"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
