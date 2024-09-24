"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from lakefs_client.api_client import ApiClient, Endpoint as _Endpoint
from lakefs_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from lakefs_client.model.authentication_token import AuthenticationToken
from lakefs_client.model.error import Error
from lakefs_client.model.external_login_information import ExternalLoginInformation
from lakefs_client.model.external_principal import ExternalPrincipal
from lakefs_client.model.external_principal_creation import ExternalPrincipalCreation
from lakefs_client.model.external_principal_list import ExternalPrincipalList


class ExternalApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_user_external_principal_endpoint = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/auth/users/{userId}/external/principals',
                'operation_id': 'create_user_external_principal',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'user_id',
                    'principal_id',
                    'external_principal_creation',
                ],
                'required': [
                    'user_id',
                    'principal_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'user_id':
                        (str,),
                    'principal_id':
                        (str,),
                    'external_principal_creation':
                        (ExternalPrincipalCreation,),
                },
                'attribute_map': {
                    'user_id': 'userId',
                    'principal_id': 'principalId',
                },
                'location_map': {
                    'user_id': 'path',
                    'principal_id': 'query',
                    'external_principal_creation': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.delete_user_external_principal_endpoint = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/auth/users/{userId}/external/principals',
                'operation_id': 'delete_user_external_principal',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'user_id',
                    'principal_id',
                ],
                'required': [
                    'user_id',
                    'principal_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'user_id':
                        (str,),
                    'principal_id':
                        (str,),
                },
                'attribute_map': {
                    'user_id': 'userId',
                    'principal_id': 'principalId',
                },
                'location_map': {
                    'user_id': 'path',
                    'principal_id': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.external_principal_login_endpoint = _Endpoint(
            settings={
                'response_type': (AuthenticationToken,),
                'auth': [],
                'endpoint_path': '/auth/external/principal/login',
                'operation_id': 'external_principal_login',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'external_login_information',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'external_login_information':
                        (ExternalLoginInformation,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'external_login_information': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.get_external_principal_endpoint = _Endpoint(
            settings={
                'response_type': (ExternalPrincipal,),
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/auth/external/principals',
                'operation_id': 'get_external_principal',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'principal_id',
                ],
                'required': [
                    'principal_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'principal_id':
                        (str,),
                },
                'attribute_map': {
                    'principal_id': 'principalId',
                },
                'location_map': {
                    'principal_id': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.list_user_external_principals_endpoint = _Endpoint(
            settings={
                'response_type': (ExternalPrincipalList,),
                'auth': [
                    'basic_auth',
                    'cookie_auth',
                    'jwt_token',
                    'oidc_auth',
                    'saml_auth'
                ],
                'endpoint_path': '/auth/users/{userId}/external/principals/ls',
                'operation_id': 'list_user_external_principals',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'user_id',
                    'prefix',
                    'after',
                    'amount',
                ],
                'required': [
                    'user_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'amount',
                ]
            },
            root_map={
                'validations': {
                    ('amount',): {

                        'inclusive_maximum': 1000,
                        'inclusive_minimum': -1,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'user_id':
                        (str,),
                    'prefix':
                        (str,),
                    'after':
                        (str,),
                    'amount':
                        (int,),
                },
                'attribute_map': {
                    'user_id': 'userId',
                    'prefix': 'prefix',
                    'after': 'after',
                    'amount': 'amount',
                },
                'location_map': {
                    'user_id': 'path',
                    'prefix': 'query',
                    'after': 'query',
                    'amount': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def create_user_external_principal(
        self,
        user_id,
        principal_id,
        **kwargs
    ):
        """attach external principal to user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_user_external_principal(user_id, principal_id, async_req=True)
        >>> result = thread.get()

        Args:
            user_id (str):
            principal_id (str):

        Keyword Args:
            external_principal_creation (ExternalPrincipalCreation): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            None
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['user_id'] = \
            user_id
        kwargs['principal_id'] = \
            principal_id
        return self.create_user_external_principal_endpoint.call_with_http_info(**kwargs)

    def delete_user_external_principal(
        self,
        user_id,
        principal_id,
        **kwargs
    ):
        """delete external principal from user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_user_external_principal(user_id, principal_id, async_req=True)
        >>> result = thread.get()

        Args:
            user_id (str):
            principal_id (str):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            None
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['user_id'] = \
            user_id
        kwargs['principal_id'] = \
            principal_id
        return self.delete_user_external_principal_endpoint.call_with_http_info(**kwargs)

    def external_principal_login(
        self,
        **kwargs
    ):
        """perform a login using an external authenticator  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.external_principal_login(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            external_login_information (ExternalLoginInformation): [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            AuthenticationToken
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.external_principal_login_endpoint.call_with_http_info(**kwargs)

    def get_external_principal(
        self,
        principal_id,
        **kwargs
    ):
        """describe external principal by id  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_external_principal(principal_id, async_req=True)
        >>> result = thread.get()

        Args:
            principal_id (str):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ExternalPrincipal
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['principal_id'] = \
            principal_id
        return self.get_external_principal_endpoint.call_with_http_info(**kwargs)

    def list_user_external_principals(
        self,
        user_id,
        **kwargs
    ):
        """list user external policies attached to a user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_user_external_principals(user_id, async_req=True)
        >>> result = thread.get()

        Args:
            user_id (str):

        Keyword Args:
            prefix (str): return items prefixed with this value. [optional]
            after (str): return items after this value. [optional]
            amount (int): how many items to return. [optional] if omitted the server will use the default value of 100
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ExternalPrincipalList
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['user_id'] = \
            user_id
        return self.list_user_external_principals_endpoint.call_with_http_info(**kwargs)

