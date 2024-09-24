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
from lakefs_sdk.models.import_creation_response import ImportCreationResponse  # noqa: E501
from lakefs_sdk.rest import ApiException

class TestImportCreationResponse(unittest.TestCase):
    """ImportCreationResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ImportCreationResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ImportCreationResponse`
        """
        model = lakefs_sdk.models.import_creation_response.ImportCreationResponse()  # noqa: E501
        if include_optional :
            return ImportCreationResponse(
                id = ''
            )
        else :
            return ImportCreationResponse(
                id = '',
        )
        """

    def testImportCreationResponse(self):
        """Test ImportCreationResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
