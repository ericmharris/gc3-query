# coding: utf-8

"""
    SecRules

    A security rule defines network access over a specified protocol between instances in two security lists, or from a set of external hosts (an IP list) to instances in a security list.<p>Security rules tie the security list, security IP list, and security application entities together.<p>You can create, delete, update, and view security rules using the HTTP requests listed below. For more information about security rules, see <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=STCSG-GUID-1AEDDA2C-3561-4759-B5AD-FB4CD9C2FBD8\">About Security Rules</a> in <em>Using Oracle Cloud Infrastructure Compute Classic</em>.  # noqa: E501

    OpenAPI spec version: 18.1.2-20180126.052521
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.models.sec_rule_response import SecRuleResponse  # noqa: E501
from swagger_client.rest import ApiException


class TestSecRuleResponse(unittest.TestCase):
    """SecRuleResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSecRuleResponse(self):
        """Test SecRuleResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = swagger_client.models.sec_rule_response.SecRuleResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
