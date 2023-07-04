# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from grafeas.grafeas_v1.services.grafeas import GrafeasAsyncClient
from grafeas.grafeas_v1.services.grafeas import GrafeasClient
from grafeas.grafeas_v1.services.grafeas import pagers
from grafeas.grafeas_v1.services.grafeas import transports
from grafeas.grafeas_v1.types import attestation
from grafeas.grafeas_v1.types import build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import compliance
from grafeas.grafeas_v1.types import cvss
from grafeas.grafeas_v1.types import deployment
from grafeas.grafeas_v1.types import discovery
from grafeas.grafeas_v1.types import dsse_attestation
from grafeas.grafeas_v1.types import grafeas
from grafeas.grafeas_v1.types import image
from grafeas.grafeas_v1.types import intoto_provenance
from grafeas.grafeas_v1.types import intoto_statement
from grafeas.grafeas_v1.types import package
from grafeas.grafeas_v1.types import provenance
from grafeas.grafeas_v1.types import severity
from grafeas.grafeas_v1.types import slsa_provenance
from grafeas.grafeas_v1.types import slsa_provenance_zero_two
from grafeas.grafeas_v1.types import upgrade
from grafeas.grafeas_v1.types import vex
from grafeas.grafeas_v1.types import vulnerability
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert GrafeasClient._get_default_mtls_endpoint(None) is None
    assert GrafeasClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert GrafeasClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert GrafeasClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert GrafeasClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert GrafeasClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (GrafeasClient, "grpc"),
    (GrafeasAsyncClient, "grpc_asyncio"),
    (GrafeasClient, "rest"),
])
def test_grafeas_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'containeranalysis.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://containeranalysis.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.GrafeasGrpcTransport, "grpc"),
    (transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.GrafeasRestTransport, "rest"),
])
def test_grafeas_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (GrafeasClient, "grpc"),
    (GrafeasAsyncClient, "grpc_asyncio"),
    (GrafeasClient, "rest"),
])
def test_grafeas_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'containeranalysis.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://containeranalysis.googleapis.com'
        )


def test_grafeas_client_get_transport_class():
    transport = GrafeasClient.get_transport_class()
    available_transports = [
        transports.GrafeasGrpcTransport,
        transports.GrafeasRestTransport,
    ]
    assert transport in available_transports

    transport = GrafeasClient.get_transport_class("grpc")
    assert transport == transports.GrafeasGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (GrafeasClient, transports.GrafeasGrpcTransport, "grpc"),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio"),
    (GrafeasClient, transports.GrafeasRestTransport, "rest"),
])
@mock.patch.object(GrafeasClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GrafeasClient))
@mock.patch.object(GrafeasAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GrafeasAsyncClient))
def test_grafeas_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(GrafeasClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(GrafeasClient, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (GrafeasClient, transports.GrafeasGrpcTransport, "grpc", "true"),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (GrafeasClient, transports.GrafeasGrpcTransport, "grpc", "false"),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (GrafeasClient, transports.GrafeasRestTransport, "rest", "true"),
    (GrafeasClient, transports.GrafeasRestTransport, "rest", "false"),
])
@mock.patch.object(GrafeasClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GrafeasClient))
@mock.patch.object(GrafeasAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GrafeasAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_grafeas_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [
    GrafeasClient, GrafeasAsyncClient
])
@mock.patch.object(GrafeasClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GrafeasClient))
@mock.patch.object(GrafeasAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GrafeasAsyncClient))
def test_grafeas_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (GrafeasClient, transports.GrafeasGrpcTransport, "grpc"),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio"),
    (GrafeasClient, transports.GrafeasRestTransport, "rest"),
])
def test_grafeas_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (GrafeasClient, transports.GrafeasGrpcTransport, "grpc", grpc_helpers),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (GrafeasClient, transports.GrafeasRestTransport, "rest", None),
])
def test_grafeas_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

def test_grafeas_client_client_options_from_dict():
    with mock.patch('grafeas.grafeas_v1.services.grafeas.transports.GrafeasGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = GrafeasClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (GrafeasClient, transports.GrafeasGrpcTransport, "grpc", grpc_helpers),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_grafeas_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "containeranalysis.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
),
            scopes=None,
            default_host="containeranalysis.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  grafeas.GetOccurrenceRequest,
  dict,
])
def test_get_occurrence(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name='name_value',
            resource_uri='resource_uri_value',
            note_name='note_name_value',
            kind=common.NoteKind.VULNERABILITY,
            remediation='remediation_value',
        )
        response = client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


def test_get_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        client.get_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceRequest()

@pytest.mark.asyncio
async def test_get_occurrence_async(transport: str = 'grpc_asyncio', request_type=grafeas.GetOccurrenceRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence(
            name='name_value',
            resource_uri='resource_uri_value',
            note_name='note_name_value',
            kind=common.NoteKind.VULNERABILITY,
            remediation='remediation_value',
        ))
        response = await client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


@pytest.mark.asyncio
async def test_get_occurrence_async_from_dict():
    await test_get_occurrence_async(request_type=dict)


def test_get_occurrence_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        call.return_value = grafeas.Occurrence()
        client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_occurrence_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        await client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_occurrence_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_occurrence(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_occurrence_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_occurrence(
            grafeas.GetOccurrenceRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_occurrence_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_occurrence(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_occurrence_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_occurrence(
            grafeas.GetOccurrenceRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  grafeas.ListOccurrencesRequest,
  dict,
])
def test_list_occurrences(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListOccurrencesResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOccurrencesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_occurrences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        client.list_occurrences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListOccurrencesRequest()

@pytest.mark.asyncio
async def test_list_occurrences_async(transport: str = 'grpc_asyncio', request_type=grafeas.ListOccurrencesRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListOccurrencesResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOccurrencesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_occurrences_async_from_dict():
    await test_list_occurrences_async(request_type=dict)


def test_list_occurrences_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListOccurrencesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        call.return_value = grafeas.ListOccurrencesResponse()
        client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_occurrences_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListOccurrencesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListOccurrencesResponse())
        await client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_occurrences_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListOccurrencesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_occurrences(
            parent='parent_value',
            filter='filter_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val


def test_list_occurrences_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_occurrences(
            grafeas.ListOccurrencesRequest(),
            parent='parent_value',
            filter='filter_value',
        )

@pytest.mark.asyncio
async def test_list_occurrences_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListOccurrencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListOccurrencesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_occurrences(
            parent='parent_value',
            filter='filter_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_occurrences_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_occurrences(
            grafeas.ListOccurrencesRequest(),
            parent='parent_value',
            filter='filter_value',
        )


def test_list_occurrences_pager(transport_name: str = "grpc"):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_occurrences(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Occurrence)
                   for i in results)
def test_list_occurrences_pages(transport_name: str = "grpc"):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_occurrences(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_occurrences_async_pager():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_occurrences(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grafeas.Occurrence)
                for i in responses)


@pytest.mark.asyncio
async def test_list_occurrences_async_pages():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_occurrences),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_occurrences(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  grafeas.DeleteOccurrenceRequest,
  dict,
])
def test_delete_occurrence(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        client.delete_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteOccurrenceRequest()

@pytest.mark.asyncio
async def test_delete_occurrence_async(transport: str = 'grpc_asyncio', request_type=grafeas.DeleteOccurrenceRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_occurrence_async_from_dict():
    await test_delete_occurrence_async(request_type=dict)


def test_delete_occurrence_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteOccurrenceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        call.return_value = None
        client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_occurrence_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteOccurrenceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_occurrence_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_occurrence(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_occurrence_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_occurrence(
            grafeas.DeleteOccurrenceRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_occurrence_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_occurrence(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_occurrence_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_occurrence(
            grafeas.DeleteOccurrenceRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  grafeas.CreateOccurrenceRequest,
  dict,
])
def test_create_occurrence(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name='name_value',
            resource_uri='resource_uri_value',
            note_name='note_name_value',
            kind=common.NoteKind.VULNERABILITY,
            remediation='remediation_value',
        )
        response = client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


def test_create_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        client.create_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateOccurrenceRequest()

@pytest.mark.asyncio
async def test_create_occurrence_async(transport: str = 'grpc_asyncio', request_type=grafeas.CreateOccurrenceRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence(
            name='name_value',
            resource_uri='resource_uri_value',
            note_name='note_name_value',
            kind=common.NoteKind.VULNERABILITY,
            remediation='remediation_value',
        ))
        response = await client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


@pytest.mark.asyncio
async def test_create_occurrence_async_from_dict():
    await test_create_occurrence_async(request_type=dict)


def test_create_occurrence_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateOccurrenceRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        call.return_value = grafeas.Occurrence()
        client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_occurrence_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateOccurrenceRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        await client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_occurrence_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_occurrence(
            parent='parent_value',
            occurrence=grafeas.Occurrence(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name='name_value')
        assert arg == mock_val


def test_create_occurrence_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_occurrence(
            grafeas.CreateOccurrenceRequest(),
            parent='parent_value',
            occurrence=grafeas.Occurrence(name='name_value'),
        )

@pytest.mark.asyncio
async def test_create_occurrence_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_occurrence(
            parent='parent_value',
            occurrence=grafeas.Occurrence(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name='name_value')
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_occurrence_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_occurrence(
            grafeas.CreateOccurrenceRequest(),
            parent='parent_value',
            occurrence=grafeas.Occurrence(name='name_value'),
        )


@pytest.mark.parametrize("request_type", [
  grafeas.BatchCreateOccurrencesRequest,
  dict,
])
def test_batch_create_occurrences(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateOccurrencesResponse(
        )
        response = client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateOccurrencesResponse)


def test_batch_create_occurrences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        client.batch_create_occurrences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateOccurrencesRequest()

@pytest.mark.asyncio
async def test_batch_create_occurrences_async(transport: str = 'grpc_asyncio', request_type=grafeas.BatchCreateOccurrencesRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.BatchCreateOccurrencesResponse(
        ))
        response = await client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateOccurrencesResponse)


@pytest.mark.asyncio
async def test_batch_create_occurrences_async_from_dict():
    await test_batch_create_occurrences_async(request_type=dict)


def test_batch_create_occurrences_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateOccurrencesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        call.return_value = grafeas.BatchCreateOccurrencesResponse()
        client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_batch_create_occurrences_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateOccurrencesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.BatchCreateOccurrencesResponse())
        await client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_batch_create_occurrences_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateOccurrencesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_occurrences(
            parent='parent_value',
            occurrences=[grafeas.Occurrence(name='name_value')],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].occurrences
        mock_val = [grafeas.Occurrence(name='name_value')]
        assert arg == mock_val


def test_batch_create_occurrences_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_occurrences(
            grafeas.BatchCreateOccurrencesRequest(),
            parent='parent_value',
            occurrences=[grafeas.Occurrence(name='name_value')],
        )

@pytest.mark.asyncio
async def test_batch_create_occurrences_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateOccurrencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.BatchCreateOccurrencesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_occurrences(
            parent='parent_value',
            occurrences=[grafeas.Occurrence(name='name_value')],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].occurrences
        mock_val = [grafeas.Occurrence(name='name_value')]
        assert arg == mock_val

@pytest.mark.asyncio
async def test_batch_create_occurrences_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_occurrences(
            grafeas.BatchCreateOccurrencesRequest(),
            parent='parent_value',
            occurrences=[grafeas.Occurrence(name='name_value')],
        )


@pytest.mark.parametrize("request_type", [
  grafeas.UpdateOccurrenceRequest,
  dict,
])
def test_update_occurrence(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name='name_value',
            resource_uri='resource_uri_value',
            note_name='note_name_value',
            kind=common.NoteKind.VULNERABILITY,
            remediation='remediation_value',
        )
        response = client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


def test_update_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        client.update_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateOccurrenceRequest()

@pytest.mark.asyncio
async def test_update_occurrence_async(transport: str = 'grpc_asyncio', request_type=grafeas.UpdateOccurrenceRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence(
            name='name_value',
            resource_uri='resource_uri_value',
            note_name='note_name_value',
            kind=common.NoteKind.VULNERABILITY,
            remediation='remediation_value',
        ))
        response = await client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


@pytest.mark.asyncio
async def test_update_occurrence_async_from_dict():
    await test_update_occurrence_async(request_type=dict)


def test_update_occurrence_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateOccurrenceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        call.return_value = grafeas.Occurrence()
        client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_occurrence_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateOccurrenceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        await client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_update_occurrence_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_occurrence(
            name='name_value',
            occurrence=grafeas.Occurrence(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_occurrence_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_occurrence(
            grafeas.UpdateOccurrenceRequest(),
            name='name_value',
            occurrence=grafeas.Occurrence(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_occurrence_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_occurrence),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_occurrence(
            name='name_value',
            occurrence=grafeas.Occurrence(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_occurrence_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_occurrence(
            grafeas.UpdateOccurrenceRequest(),
            name='name_value',
            occurrence=grafeas.Occurrence(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  grafeas.GetOccurrenceNoteRequest,
  dict,
])
def test_get_occurrence_note(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        )
        response = client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_get_occurrence_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        client.get_occurrence_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceNoteRequest()

@pytest.mark.asyncio
async def test_get_occurrence_note_async(transport: str = 'grpc_asyncio', request_type=grafeas.GetOccurrenceNoteRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        ))
        response = await client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


@pytest.mark.asyncio
async def test_get_occurrence_note_async_from_dict():
    await test_get_occurrence_note_async(request_type=dict)


def test_get_occurrence_note_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        call.return_value = grafeas.Note()
        client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_occurrence_note_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        await client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_occurrence_note_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_occurrence_note(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_occurrence_note_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_occurrence_note(
            grafeas.GetOccurrenceNoteRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_occurrence_note_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_occurrence_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_occurrence_note(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_occurrence_note_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_occurrence_note(
            grafeas.GetOccurrenceNoteRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  grafeas.GetNoteRequest,
  dict,
])
def test_get_note(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        )
        response = client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_get_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        client.get_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetNoteRequest()

@pytest.mark.asyncio
async def test_get_note_async(transport: str = 'grpc_asyncio', request_type=grafeas.GetNoteRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        ))
        response = await client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


@pytest.mark.asyncio
async def test_get_note_async_from_dict():
    await test_get_note_async(request_type=dict)


def test_get_note_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        call.return_value = grafeas.Note()
        client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_note_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        await client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_note_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_note(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_note_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_note(
            grafeas.GetNoteRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_note_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_note(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_note_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_note(
            grafeas.GetNoteRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  grafeas.ListNotesRequest,
  dict,
])
def test_list_notes(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNotesResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_notes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        client.list_notes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNotesRequest()

@pytest.mark.asyncio
async def test_list_notes_async(transport: str = 'grpc_asyncio', request_type=grafeas.ListNotesRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListNotesResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_notes_async_from_dict():
    await test_list_notes_async(request_type=dict)


def test_list_notes_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNotesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        call.return_value = grafeas.ListNotesResponse()
        client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_notes_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNotesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListNotesResponse())
        await client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_notes_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNotesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_notes(
            parent='parent_value',
            filter='filter_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val


def test_list_notes_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notes(
            grafeas.ListNotesRequest(),
            parent='parent_value',
            filter='filter_value',
        )

@pytest.mark.asyncio
async def test_list_notes_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNotesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListNotesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_notes(
            parent='parent_value',
            filter='filter_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_notes_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notes(
            grafeas.ListNotesRequest(),
            parent='parent_value',
            filter='filter_value',
        )


def test_list_notes_pager(transport_name: str = "grpc"):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                    grafeas.Note(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNotesResponse(
                notes=[],
                next_page_token='def',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_notes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Note)
                   for i in results)
def test_list_notes_pages(transport_name: str = "grpc"):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                    grafeas.Note(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNotesResponse(
                notes=[],
                next_page_token='def',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_notes(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_notes_async_pager():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                    grafeas.Note(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNotesResponse(
                notes=[],
                next_page_token='def',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_notes(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grafeas.Note)
                for i in responses)


@pytest.mark.asyncio
async def test_list_notes_async_pages():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_notes),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                    grafeas.Note(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNotesResponse(
                notes=[],
                next_page_token='def',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_notes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  grafeas.DeleteNoteRequest,
  dict,
])
def test_delete_note(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteNoteRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        client.delete_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteNoteRequest()

@pytest.mark.asyncio
async def test_delete_note_async(transport: str = 'grpc_asyncio', request_type=grafeas.DeleteNoteRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteNoteRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_note_async_from_dict():
    await test_delete_note_async(request_type=dict)


def test_delete_note_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        call.return_value = None
        client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_note_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_note_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_note(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_note_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_note(
            grafeas.DeleteNoteRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_note_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_note(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_note_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_note(
            grafeas.DeleteNoteRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  grafeas.CreateNoteRequest,
  dict,
])
def test_create_note(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        )
        response = client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_create_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        client.create_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateNoteRequest()

@pytest.mark.asyncio
async def test_create_note_async(transport: str = 'grpc_asyncio', request_type=grafeas.CreateNoteRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        ))
        response = await client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


@pytest.mark.asyncio
async def test_create_note_async_from_dict():
    await test_create_note_async(request_type=dict)


def test_create_note_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateNoteRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        call.return_value = grafeas.Note()
        client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_note_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateNoteRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        await client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_note_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_note(
            parent='parent_value',
            note_id='note_id_value',
            note=grafeas.Note(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].note_id
        mock_val = 'note_id_value'
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name='name_value')
        assert arg == mock_val


def test_create_note_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_note(
            grafeas.CreateNoteRequest(),
            parent='parent_value',
            note_id='note_id_value',
            note=grafeas.Note(name='name_value'),
        )

@pytest.mark.asyncio
async def test_create_note_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_note(
            parent='parent_value',
            note_id='note_id_value',
            note=grafeas.Note(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].note_id
        mock_val = 'note_id_value'
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name='name_value')
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_note_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_note(
            grafeas.CreateNoteRequest(),
            parent='parent_value',
            note_id='note_id_value',
            note=grafeas.Note(name='name_value'),
        )


@pytest.mark.parametrize("request_type", [
  grafeas.BatchCreateNotesRequest,
  dict,
])
def test_batch_create_notes(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateNotesResponse(
        )
        response = client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateNotesResponse)


def test_batch_create_notes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        client.batch_create_notes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateNotesRequest()

@pytest.mark.asyncio
async def test_batch_create_notes_async(transport: str = 'grpc_asyncio', request_type=grafeas.BatchCreateNotesRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.BatchCreateNotesResponse(
        ))
        response = await client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateNotesResponse)


@pytest.mark.asyncio
async def test_batch_create_notes_async_from_dict():
    await test_batch_create_notes_async(request_type=dict)


def test_batch_create_notes_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateNotesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        call.return_value = grafeas.BatchCreateNotesResponse()
        client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_batch_create_notes_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateNotesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.BatchCreateNotesResponse())
        await client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_batch_create_notes_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateNotesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_notes(
            parent='parent_value',
            notes={'key_value': grafeas.Note(name='name_value')},
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].notes
        mock_val = {'key_value': grafeas.Note(name='name_value')}
        assert arg == mock_val


def test_batch_create_notes_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_notes(
            grafeas.BatchCreateNotesRequest(),
            parent='parent_value',
            notes={'key_value': grafeas.Note(name='name_value')},
        )

@pytest.mark.asyncio
async def test_batch_create_notes_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_notes),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateNotesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.BatchCreateNotesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_notes(
            parent='parent_value',
            notes={'key_value': grafeas.Note(name='name_value')},
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].notes
        mock_val = {'key_value': grafeas.Note(name='name_value')}
        assert arg == mock_val

@pytest.mark.asyncio
async def test_batch_create_notes_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_notes(
            grafeas.BatchCreateNotesRequest(),
            parent='parent_value',
            notes={'key_value': grafeas.Note(name='name_value')},
        )


@pytest.mark.parametrize("request_type", [
  grafeas.UpdateNoteRequest,
  dict,
])
def test_update_note(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        )
        response = client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_update_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        client.update_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateNoteRequest()

@pytest.mark.asyncio
async def test_update_note_async(transport: str = 'grpc_asyncio', request_type=grafeas.UpdateNoteRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note(
            name='name_value',
            short_description='short_description_value',
            long_description='long_description_value',
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=['related_note_names_value'],
        ))
        response = await client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


@pytest.mark.asyncio
async def test_update_note_async_from_dict():
    await test_update_note_async(request_type=dict)


def test_update_note_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        call.return_value = grafeas.Note()
        client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_note_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateNoteRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        await client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_update_note_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_note(
            name='name_value',
            note=grafeas.Note(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_note_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_note(
            grafeas.UpdateNoteRequest(),
            name='name_value',
            note=grafeas.Note(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_note_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_note),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_note(
            name='name_value',
            note=grafeas.Note(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_note_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_note(
            grafeas.UpdateNoteRequest(),
            name='name_value',
            note=grafeas.Note(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  grafeas.ListNoteOccurrencesRequest,
  dict,
])
def test_list_note_occurrences(request_type, transport: str = 'grpc'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNoteOccurrencesResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNoteOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNoteOccurrencesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_note_occurrences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        client.list_note_occurrences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNoteOccurrencesRequest()

@pytest.mark.asyncio
async def test_list_note_occurrences_async(transport: str = 'grpc_asyncio', request_type=grafeas.ListNoteOccurrencesRequest):
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListNoteOccurrencesResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNoteOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNoteOccurrencesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_note_occurrences_async_from_dict():
    await test_list_note_occurrences_async(request_type=dict)


def test_list_note_occurrences_field_headers():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNoteOccurrencesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        call.return_value = grafeas.ListNoteOccurrencesResponse()
        client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_note_occurrences_field_headers_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNoteOccurrencesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListNoteOccurrencesResponse())
        await client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_list_note_occurrences_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNoteOccurrencesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_note_occurrences(
            name='name_value',
            filter='filter_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val


def test_list_note_occurrences_flattened_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_note_occurrences(
            grafeas.ListNoteOccurrencesRequest(),
            name='name_value',
            filter='filter_value',
        )

@pytest.mark.asyncio
async def test_list_note_occurrences_flattened_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNoteOccurrencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.ListNoteOccurrencesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_note_occurrences(
            name='name_value',
            filter='filter_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].filter
        mock_val = 'filter_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_note_occurrences_flattened_error_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_note_occurrences(
            grafeas.ListNoteOccurrencesRequest(),
            name='name_value',
            filter='filter_value',
        )


def test_list_note_occurrences_pager(transport_name: str = "grpc"):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('name', ''),
            )),
        )
        pager = client.list_note_occurrences(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Occurrence)
                   for i in results)
def test_list_note_occurrences_pages(transport_name: str = "grpc"):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_note_occurrences(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_note_occurrences_async_pager():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_note_occurrences(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grafeas.Occurrence)
                for i in responses)


@pytest.mark.asyncio
async def test_list_note_occurrences_async_pages():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_note_occurrences),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_note_occurrences(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    grafeas.GetOccurrenceRequest,
    dict,
])
def test_get_occurrence_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Occurrence(
              name='name_value',
              resource_uri='resource_uri_value',
              note_name='note_name_value',
              kind=common.NoteKind.VULNERABILITY,
              remediation='remediation_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Occurrence.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_occurrence(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


def test_get_occurrence_rest_required_fields(request_type=grafeas.GetOccurrenceRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Occurrence()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Occurrence.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_occurrence(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_occurrence_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_occurrence._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_occurrence_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_get_occurrence") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_get_occurrence") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.GetOccurrenceRequest.pb(grafeas.GetOccurrenceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Occurrence.to_json(grafeas.Occurrence())

        request = grafeas.GetOccurrenceRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Occurrence()

        client.get_occurrence(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_occurrence_rest_bad_request(transport: str = 'rest', request_type=grafeas.GetOccurrenceRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_occurrence(request)


def test_get_occurrence_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Occurrence()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/occurrences/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Occurrence.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_occurrence(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/occurrences/*}" % client.transport._host, args[1])


def test_get_occurrence_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_occurrence(
            grafeas.GetOccurrenceRequest(),
            name='name_value',
        )


def test_get_occurrence_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.ListOccurrencesRequest,
    dict,
])
def test_list_occurrences_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.ListOccurrencesResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.ListOccurrencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_occurrences(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOccurrencesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_occurrences_rest_required_fields(request_type=grafeas.ListOccurrencesRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_occurrences._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_occurrences._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.ListOccurrencesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.ListOccurrencesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_occurrences(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_occurrences_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_occurrences._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_occurrences_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_list_occurrences") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_list_occurrences") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.ListOccurrencesRequest.pb(grafeas.ListOccurrencesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.ListOccurrencesResponse.to_json(grafeas.ListOccurrencesResponse())

        request = grafeas.ListOccurrencesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.ListOccurrencesResponse()

        client.list_occurrences(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_occurrences_rest_bad_request(transport: str = 'rest', request_type=grafeas.ListOccurrencesRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_occurrences(request)


def test_list_occurrences_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.ListOccurrencesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            filter='filter_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.ListOccurrencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_occurrences(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*}/occurrences" % client.transport._host, args[1])


def test_list_occurrences_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_occurrences(
            grafeas.ListOccurrencesRequest(),
            parent='parent_value',
            filter='filter_value',
        )


def test_list_occurrences_rest_pager(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(grafeas.ListOccurrencesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1'}

        pager = client.list_occurrences(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Occurrence)
                for i in results)

        pages = list(client.list_occurrences(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    grafeas.DeleteOccurrenceRequest,
    dict,
])
def test_delete_occurrence_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_occurrence(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_occurrence_rest_required_fields(request_type=grafeas.DeleteOccurrenceRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ''

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_occurrence(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_occurrence_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_occurrence._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_occurrence_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_delete_occurrence") as pre:
        pre.assert_not_called()
        pb_message = grafeas.DeleteOccurrenceRequest.pb(grafeas.DeleteOccurrenceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = grafeas.DeleteOccurrenceRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_occurrence(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()


def test_delete_occurrence_rest_bad_request(transport: str = 'rest', request_type=grafeas.DeleteOccurrenceRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_occurrence(request)


def test_delete_occurrence_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/occurrences/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_occurrence(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/occurrences/*}" % client.transport._host, args[1])


def test_delete_occurrence_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_occurrence(
            grafeas.DeleteOccurrenceRequest(),
            name='name_value',
        )


def test_delete_occurrence_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.CreateOccurrenceRequest,
    dict,
])
def test_create_occurrence_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request_init["occurrence"] = {'name': 'name_value', 'resource_uri': 'resource_uri_value', 'note_name': 'note_name_value', 'kind': 1, 'remediation': 'remediation_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'vulnerability': {'type_': 'type__value', 'severity': 1, 'cvss_score': 0.1082, 'cvssv3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'package_issue': [{'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'fix_available': True, 'package_type': 'package_type_value', 'effective_severity': 1, 'file_location': [{'file_path': 'file_path_value'}]}], 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_urls': [{'url': 'url_value', 'label': 'label_value'}], 'effective_severity': 1, 'fix_available': True, 'cvss_version': 1, 'cvss_v2': {}, 'vex_assessment': {'cve': 'cve_value', 'related_uris': {}, 'note_name': 'note_name_value', 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}], 'justification': {'justification_type': 1, 'details': 'details_value'}}}, 'build': {'provenance': {'id': 'id_value', 'project_id': 'project_id_value', 'commands': [{'name': 'name_value', 'env': ['env_value1', 'env_value2'], 'args': ['args_value1', 'args_value2'], 'dir_': 'dir__value', 'id': 'id_value', 'wait_for': ['wait_for_value1', 'wait_for_value2']}], 'built_artifacts': [{'checksum': 'checksum_value', 'id': 'id_value', 'names': ['names_value1', 'names_value2']}], 'create_time': {}, 'start_time': {}, 'end_time': {}, 'creator': 'creator_value', 'logs_uri': 'logs_uri_value', 'source_provenance': {'artifact_storage_source_uri': 'artifact_storage_source_uri_value', 'file_hashes': {}, 'context': {'cloud_repo': {'repo_id': {'project_repo_id': {'project_id': 'project_id_value', 'repo_name': 'repo_name_value'}, 'uid': 'uid_value'}, 'revision_id': 'revision_id_value', 'alias_context': {'kind': 1, 'name': 'name_value'}}, 'gerrit': {'host_uri': 'host_uri_value', 'gerrit_project': 'gerrit_project_value', 'revision_id': 'revision_id_value', 'alias_context': {}}, 'git': {'url': 'url_value', 'revision_id': 'revision_id_value'}, 'labels': {}}, 'additional_contexts': {}}, 'trigger_id': 'trigger_id_value', 'build_options': {}, 'builder_version': 'builder_version_value'}, 'provenance_bytes': 'provenance_bytes_value', 'intoto_provenance': {'builder_config': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': [{'type_url': 'type.googleapis.com/google.protobuf.Duration', 'value': b'\x08\x0c\x10\xdb\x07'}], 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': ['materials_value1', 'materials_value2']}, 'intoto_statement': {'type_': 'type__value', 'subject': [{'name': 'name_value', 'digest': {}}], 'predicate_type': 'predicate_type_value', 'provenance': {}, 'slsa_provenance': {'builder': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': {}, 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}, 'slsa_provenance_zero_two': {'builder': {'id': 'id_value'}, 'build_type': 'build_type_value', 'invocation': {'config_source': {'uri': 'uri_value', 'digest': {}, 'entry_point': 'entry_point_value'}, 'parameters': {'fields': {}}, 'environment': {}}, 'build_config': {}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'parameters': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}}}, 'image': {'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}, 'distance': 843, 'layer_info': [{'directive': 'directive_value', 'arguments': 'arguments_value'}], 'base_resource_url': 'base_resource_url_value'}, 'package': {'name': 'name_value', 'location': [{'cpe_uri': 'cpe_uri_value', 'version': {}, 'path': 'path_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'version': {}}, 'deployment': {'user_email': 'user_email_value', 'deploy_time': {}, 'undeploy_time': {}, 'config': 'config_value', 'address': 'address_value', 'resource_uri': ['resource_uri_value1', 'resource_uri_value2'], 'platform': 1}, 'discovery': {'continuous_analysis': 1, 'analysis_status': 1, 'analysis_completed': {'analysis_type': ['analysis_type_value1', 'analysis_type_value2']}, 'analysis_error': [{'code': 411, 'message': 'message_value', 'details': {}}], 'analysis_status_error': {}, 'cpe': 'cpe_value', 'last_scan_time': {}, 'archive_time': {}}, 'attestation': {'serialized_payload': b'serialized_payload_blob', 'signatures': [{'signature': b'signature_blob', 'public_key_id': 'public_key_id_value'}], 'jwts': [{'compact_jwt': 'compact_jwt_value'}]}, 'upgrade': {'package': 'package_value', 'parsed_version': {}, 'distribution': {'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}, 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'non_compliant_files': [{'path': 'path_value', 'display_command': 'display_command_value', 'reason': 'reason_value'}], 'non_compliance_reason': 'non_compliance_reason_value'}, 'dsse_attestation': {'envelope': {'payload': b'payload_blob', 'payload_type': 'payload_type_value', 'signatures': [{'sig': b'sig_blob', 'keyid': 'keyid_value'}]}, 'statement': {}}, 'envelope': {}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Occurrence(
              name='name_value',
              resource_uri='resource_uri_value',
              note_name='note_name_value',
              kind=common.NoteKind.VULNERABILITY,
              remediation='remediation_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Occurrence.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_occurrence(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


def test_create_occurrence_rest_required_fields(request_type=grafeas.CreateOccurrenceRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Occurrence()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Occurrence.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_occurrence(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_occurrence_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_occurrence._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "occurrence", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_occurrence_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_create_occurrence") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_create_occurrence") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.CreateOccurrenceRequest.pb(grafeas.CreateOccurrenceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Occurrence.to_json(grafeas.Occurrence())

        request = grafeas.CreateOccurrenceRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Occurrence()

        client.create_occurrence(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_occurrence_rest_bad_request(transport: str = 'rest', request_type=grafeas.CreateOccurrenceRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request_init["occurrence"] = {'name': 'name_value', 'resource_uri': 'resource_uri_value', 'note_name': 'note_name_value', 'kind': 1, 'remediation': 'remediation_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'vulnerability': {'type_': 'type__value', 'severity': 1, 'cvss_score': 0.1082, 'cvssv3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'package_issue': [{'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'fix_available': True, 'package_type': 'package_type_value', 'effective_severity': 1, 'file_location': [{'file_path': 'file_path_value'}]}], 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_urls': [{'url': 'url_value', 'label': 'label_value'}], 'effective_severity': 1, 'fix_available': True, 'cvss_version': 1, 'cvss_v2': {}, 'vex_assessment': {'cve': 'cve_value', 'related_uris': {}, 'note_name': 'note_name_value', 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}], 'justification': {'justification_type': 1, 'details': 'details_value'}}}, 'build': {'provenance': {'id': 'id_value', 'project_id': 'project_id_value', 'commands': [{'name': 'name_value', 'env': ['env_value1', 'env_value2'], 'args': ['args_value1', 'args_value2'], 'dir_': 'dir__value', 'id': 'id_value', 'wait_for': ['wait_for_value1', 'wait_for_value2']}], 'built_artifacts': [{'checksum': 'checksum_value', 'id': 'id_value', 'names': ['names_value1', 'names_value2']}], 'create_time': {}, 'start_time': {}, 'end_time': {}, 'creator': 'creator_value', 'logs_uri': 'logs_uri_value', 'source_provenance': {'artifact_storage_source_uri': 'artifact_storage_source_uri_value', 'file_hashes': {}, 'context': {'cloud_repo': {'repo_id': {'project_repo_id': {'project_id': 'project_id_value', 'repo_name': 'repo_name_value'}, 'uid': 'uid_value'}, 'revision_id': 'revision_id_value', 'alias_context': {'kind': 1, 'name': 'name_value'}}, 'gerrit': {'host_uri': 'host_uri_value', 'gerrit_project': 'gerrit_project_value', 'revision_id': 'revision_id_value', 'alias_context': {}}, 'git': {'url': 'url_value', 'revision_id': 'revision_id_value'}, 'labels': {}}, 'additional_contexts': {}}, 'trigger_id': 'trigger_id_value', 'build_options': {}, 'builder_version': 'builder_version_value'}, 'provenance_bytes': 'provenance_bytes_value', 'intoto_provenance': {'builder_config': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': [{'type_url': 'type.googleapis.com/google.protobuf.Duration', 'value': b'\x08\x0c\x10\xdb\x07'}], 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': ['materials_value1', 'materials_value2']}, 'intoto_statement': {'type_': 'type__value', 'subject': [{'name': 'name_value', 'digest': {}}], 'predicate_type': 'predicate_type_value', 'provenance': {}, 'slsa_provenance': {'builder': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': {}, 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}, 'slsa_provenance_zero_two': {'builder': {'id': 'id_value'}, 'build_type': 'build_type_value', 'invocation': {'config_source': {'uri': 'uri_value', 'digest': {}, 'entry_point': 'entry_point_value'}, 'parameters': {'fields': {}}, 'environment': {}}, 'build_config': {}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'parameters': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}}}, 'image': {'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}, 'distance': 843, 'layer_info': [{'directive': 'directive_value', 'arguments': 'arguments_value'}], 'base_resource_url': 'base_resource_url_value'}, 'package': {'name': 'name_value', 'location': [{'cpe_uri': 'cpe_uri_value', 'version': {}, 'path': 'path_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'version': {}}, 'deployment': {'user_email': 'user_email_value', 'deploy_time': {}, 'undeploy_time': {}, 'config': 'config_value', 'address': 'address_value', 'resource_uri': ['resource_uri_value1', 'resource_uri_value2'], 'platform': 1}, 'discovery': {'continuous_analysis': 1, 'analysis_status': 1, 'analysis_completed': {'analysis_type': ['analysis_type_value1', 'analysis_type_value2']}, 'analysis_error': [{'code': 411, 'message': 'message_value', 'details': {}}], 'analysis_status_error': {}, 'cpe': 'cpe_value', 'last_scan_time': {}, 'archive_time': {}}, 'attestation': {'serialized_payload': b'serialized_payload_blob', 'signatures': [{'signature': b'signature_blob', 'public_key_id': 'public_key_id_value'}], 'jwts': [{'compact_jwt': 'compact_jwt_value'}]}, 'upgrade': {'package': 'package_value', 'parsed_version': {}, 'distribution': {'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}, 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'non_compliant_files': [{'path': 'path_value', 'display_command': 'display_command_value', 'reason': 'reason_value'}], 'non_compliance_reason': 'non_compliance_reason_value'}, 'dsse_attestation': {'envelope': {'payload': b'payload_blob', 'payload_type': 'payload_type_value', 'signatures': [{'sig': b'sig_blob', 'keyid': 'keyid_value'}]}, 'statement': {}}, 'envelope': {}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_occurrence(request)


def test_create_occurrence_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Occurrence()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            occurrence=grafeas.Occurrence(name='name_value'),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Occurrence.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_occurrence(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*}/occurrences" % client.transport._host, args[1])


def test_create_occurrence_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_occurrence(
            grafeas.CreateOccurrenceRequest(),
            parent='parent_value',
            occurrence=grafeas.Occurrence(name='name_value'),
        )


def test_create_occurrence_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.BatchCreateOccurrencesRequest,
    dict,
])
def test_batch_create_occurrences_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.BatchCreateOccurrencesResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.BatchCreateOccurrencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.batch_create_occurrences(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateOccurrencesResponse)


def test_batch_create_occurrences_rest_required_fields(request_type=grafeas.BatchCreateOccurrencesRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_create_occurrences._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_create_occurrences._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.BatchCreateOccurrencesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.BatchCreateOccurrencesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.batch_create_occurrences(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_batch_create_occurrences_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.batch_create_occurrences._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "occurrences", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_create_occurrences_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_batch_create_occurrences") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_batch_create_occurrences") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.BatchCreateOccurrencesRequest.pb(grafeas.BatchCreateOccurrencesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.BatchCreateOccurrencesResponse.to_json(grafeas.BatchCreateOccurrencesResponse())

        request = grafeas.BatchCreateOccurrencesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.BatchCreateOccurrencesResponse()

        client.batch_create_occurrences(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_create_occurrences_rest_bad_request(transport: str = 'rest', request_type=grafeas.BatchCreateOccurrencesRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_create_occurrences(request)


def test_batch_create_occurrences_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.BatchCreateOccurrencesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            occurrences=[grafeas.Occurrence(name='name_value')],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.BatchCreateOccurrencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.batch_create_occurrences(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*}/occurrences:batchCreate" % client.transport._host, args[1])


def test_batch_create_occurrences_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_occurrences(
            grafeas.BatchCreateOccurrencesRequest(),
            parent='parent_value',
            occurrences=[grafeas.Occurrence(name='name_value')],
        )


def test_batch_create_occurrences_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.UpdateOccurrenceRequest,
    dict,
])
def test_update_occurrence_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request_init["occurrence"] = {'name': 'name_value', 'resource_uri': 'resource_uri_value', 'note_name': 'note_name_value', 'kind': 1, 'remediation': 'remediation_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'vulnerability': {'type_': 'type__value', 'severity': 1, 'cvss_score': 0.1082, 'cvssv3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'package_issue': [{'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'fix_available': True, 'package_type': 'package_type_value', 'effective_severity': 1, 'file_location': [{'file_path': 'file_path_value'}]}], 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_urls': [{'url': 'url_value', 'label': 'label_value'}], 'effective_severity': 1, 'fix_available': True, 'cvss_version': 1, 'cvss_v2': {}, 'vex_assessment': {'cve': 'cve_value', 'related_uris': {}, 'note_name': 'note_name_value', 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}], 'justification': {'justification_type': 1, 'details': 'details_value'}}}, 'build': {'provenance': {'id': 'id_value', 'project_id': 'project_id_value', 'commands': [{'name': 'name_value', 'env': ['env_value1', 'env_value2'], 'args': ['args_value1', 'args_value2'], 'dir_': 'dir__value', 'id': 'id_value', 'wait_for': ['wait_for_value1', 'wait_for_value2']}], 'built_artifacts': [{'checksum': 'checksum_value', 'id': 'id_value', 'names': ['names_value1', 'names_value2']}], 'create_time': {}, 'start_time': {}, 'end_time': {}, 'creator': 'creator_value', 'logs_uri': 'logs_uri_value', 'source_provenance': {'artifact_storage_source_uri': 'artifact_storage_source_uri_value', 'file_hashes': {}, 'context': {'cloud_repo': {'repo_id': {'project_repo_id': {'project_id': 'project_id_value', 'repo_name': 'repo_name_value'}, 'uid': 'uid_value'}, 'revision_id': 'revision_id_value', 'alias_context': {'kind': 1, 'name': 'name_value'}}, 'gerrit': {'host_uri': 'host_uri_value', 'gerrit_project': 'gerrit_project_value', 'revision_id': 'revision_id_value', 'alias_context': {}}, 'git': {'url': 'url_value', 'revision_id': 'revision_id_value'}, 'labels': {}}, 'additional_contexts': {}}, 'trigger_id': 'trigger_id_value', 'build_options': {}, 'builder_version': 'builder_version_value'}, 'provenance_bytes': 'provenance_bytes_value', 'intoto_provenance': {'builder_config': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': [{'type_url': 'type.googleapis.com/google.protobuf.Duration', 'value': b'\x08\x0c\x10\xdb\x07'}], 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': ['materials_value1', 'materials_value2']}, 'intoto_statement': {'type_': 'type__value', 'subject': [{'name': 'name_value', 'digest': {}}], 'predicate_type': 'predicate_type_value', 'provenance': {}, 'slsa_provenance': {'builder': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': {}, 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}, 'slsa_provenance_zero_two': {'builder': {'id': 'id_value'}, 'build_type': 'build_type_value', 'invocation': {'config_source': {'uri': 'uri_value', 'digest': {}, 'entry_point': 'entry_point_value'}, 'parameters': {'fields': {}}, 'environment': {}}, 'build_config': {}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'parameters': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}}}, 'image': {'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}, 'distance': 843, 'layer_info': [{'directive': 'directive_value', 'arguments': 'arguments_value'}], 'base_resource_url': 'base_resource_url_value'}, 'package': {'name': 'name_value', 'location': [{'cpe_uri': 'cpe_uri_value', 'version': {}, 'path': 'path_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'version': {}}, 'deployment': {'user_email': 'user_email_value', 'deploy_time': {}, 'undeploy_time': {}, 'config': 'config_value', 'address': 'address_value', 'resource_uri': ['resource_uri_value1', 'resource_uri_value2'], 'platform': 1}, 'discovery': {'continuous_analysis': 1, 'analysis_status': 1, 'analysis_completed': {'analysis_type': ['analysis_type_value1', 'analysis_type_value2']}, 'analysis_error': [{'code': 411, 'message': 'message_value', 'details': {}}], 'analysis_status_error': {}, 'cpe': 'cpe_value', 'last_scan_time': {}, 'archive_time': {}}, 'attestation': {'serialized_payload': b'serialized_payload_blob', 'signatures': [{'signature': b'signature_blob', 'public_key_id': 'public_key_id_value'}], 'jwts': [{'compact_jwt': 'compact_jwt_value'}]}, 'upgrade': {'package': 'package_value', 'parsed_version': {}, 'distribution': {'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}, 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'non_compliant_files': [{'path': 'path_value', 'display_command': 'display_command_value', 'reason': 'reason_value'}], 'non_compliance_reason': 'non_compliance_reason_value'}, 'dsse_attestation': {'envelope': {'payload': b'payload_blob', 'payload_type': 'payload_type_value', 'signatures': [{'sig': b'sig_blob', 'keyid': 'keyid_value'}]}, 'statement': {}}, 'envelope': {}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Occurrence(
              name='name_value',
              resource_uri='resource_uri_value',
              note_name='note_name_value',
              kind=common.NoteKind.VULNERABILITY,
              remediation='remediation_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Occurrence.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_occurrence(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == 'name_value'
    assert response.resource_uri == 'resource_uri_value'
    assert response.note_name == 'note_name_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == 'remediation_value'


def test_update_occurrence_rest_required_fields(request_type=grafeas.UpdateOccurrenceRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_occurrence._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_occurrence._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Occurrence()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Occurrence.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_occurrence(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_occurrence_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_occurrence._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("name", "occurrence", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_occurrence_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_update_occurrence") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_update_occurrence") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.UpdateOccurrenceRequest.pb(grafeas.UpdateOccurrenceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Occurrence.to_json(grafeas.Occurrence())

        request = grafeas.UpdateOccurrenceRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Occurrence()

        client.update_occurrence(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_occurrence_rest_bad_request(transport: str = 'rest', request_type=grafeas.UpdateOccurrenceRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request_init["occurrence"] = {'name': 'name_value', 'resource_uri': 'resource_uri_value', 'note_name': 'note_name_value', 'kind': 1, 'remediation': 'remediation_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'vulnerability': {'type_': 'type__value', 'severity': 1, 'cvss_score': 0.1082, 'cvssv3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'package_issue': [{'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'fix_available': True, 'package_type': 'package_type_value', 'effective_severity': 1, 'file_location': [{'file_path': 'file_path_value'}]}], 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_urls': [{'url': 'url_value', 'label': 'label_value'}], 'effective_severity': 1, 'fix_available': True, 'cvss_version': 1, 'cvss_v2': {}, 'vex_assessment': {'cve': 'cve_value', 'related_uris': {}, 'note_name': 'note_name_value', 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}], 'justification': {'justification_type': 1, 'details': 'details_value'}}}, 'build': {'provenance': {'id': 'id_value', 'project_id': 'project_id_value', 'commands': [{'name': 'name_value', 'env': ['env_value1', 'env_value2'], 'args': ['args_value1', 'args_value2'], 'dir_': 'dir__value', 'id': 'id_value', 'wait_for': ['wait_for_value1', 'wait_for_value2']}], 'built_artifacts': [{'checksum': 'checksum_value', 'id': 'id_value', 'names': ['names_value1', 'names_value2']}], 'create_time': {}, 'start_time': {}, 'end_time': {}, 'creator': 'creator_value', 'logs_uri': 'logs_uri_value', 'source_provenance': {'artifact_storage_source_uri': 'artifact_storage_source_uri_value', 'file_hashes': {}, 'context': {'cloud_repo': {'repo_id': {'project_repo_id': {'project_id': 'project_id_value', 'repo_name': 'repo_name_value'}, 'uid': 'uid_value'}, 'revision_id': 'revision_id_value', 'alias_context': {'kind': 1, 'name': 'name_value'}}, 'gerrit': {'host_uri': 'host_uri_value', 'gerrit_project': 'gerrit_project_value', 'revision_id': 'revision_id_value', 'alias_context': {}}, 'git': {'url': 'url_value', 'revision_id': 'revision_id_value'}, 'labels': {}}, 'additional_contexts': {}}, 'trigger_id': 'trigger_id_value', 'build_options': {}, 'builder_version': 'builder_version_value'}, 'provenance_bytes': 'provenance_bytes_value', 'intoto_provenance': {'builder_config': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': [{'type_url': 'type.googleapis.com/google.protobuf.Duration', 'value': b'\x08\x0c\x10\xdb\x07'}], 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': ['materials_value1', 'materials_value2']}, 'intoto_statement': {'type_': 'type__value', 'subject': [{'name': 'name_value', 'digest': {}}], 'predicate_type': 'predicate_type_value', 'provenance': {}, 'slsa_provenance': {'builder': {'id': 'id_value'}, 'recipe': {'type_': 'type__value', 'defined_in_material': 1971, 'entry_point': 'entry_point_value', 'arguments': {}, 'environment': {}}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'arguments': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}, 'slsa_provenance_zero_two': {'builder': {'id': 'id_value'}, 'build_type': 'build_type_value', 'invocation': {'config_source': {'uri': 'uri_value', 'digest': {}, 'entry_point': 'entry_point_value'}, 'parameters': {'fields': {}}, 'environment': {}}, 'build_config': {}, 'metadata': {'build_invocation_id': 'build_invocation_id_value', 'build_started_on': {}, 'build_finished_on': {}, 'completeness': {'parameters': True, 'environment': True, 'materials': True}, 'reproducible': True}, 'materials': [{'uri': 'uri_value', 'digest': {}}]}}}, 'image': {'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}, 'distance': 843, 'layer_info': [{'directive': 'directive_value', 'arguments': 'arguments_value'}], 'base_resource_url': 'base_resource_url_value'}, 'package': {'name': 'name_value', 'location': [{'cpe_uri': 'cpe_uri_value', 'version': {}, 'path': 'path_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'version': {}}, 'deployment': {'user_email': 'user_email_value', 'deploy_time': {}, 'undeploy_time': {}, 'config': 'config_value', 'address': 'address_value', 'resource_uri': ['resource_uri_value1', 'resource_uri_value2'], 'platform': 1}, 'discovery': {'continuous_analysis': 1, 'analysis_status': 1, 'analysis_completed': {'analysis_type': ['analysis_type_value1', 'analysis_type_value2']}, 'analysis_error': [{'code': 411, 'message': 'message_value', 'details': {}}], 'analysis_status_error': {}, 'cpe': 'cpe_value', 'last_scan_time': {}, 'archive_time': {}}, 'attestation': {'serialized_payload': b'serialized_payload_blob', 'signatures': [{'signature': b'signature_blob', 'public_key_id': 'public_key_id_value'}], 'jwts': [{'compact_jwt': 'compact_jwt_value'}]}, 'upgrade': {'package': 'package_value', 'parsed_version': {}, 'distribution': {'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}, 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'non_compliant_files': [{'path': 'path_value', 'display_command': 'display_command_value', 'reason': 'reason_value'}], 'non_compliance_reason': 'non_compliance_reason_value'}, 'dsse_attestation': {'envelope': {'payload': b'payload_blob', 'payload_type': 'payload_type_value', 'signatures': [{'sig': b'sig_blob', 'keyid': 'keyid_value'}]}, 'statement': {}}, 'envelope': {}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_occurrence(request)


def test_update_occurrence_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Occurrence()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/occurrences/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            occurrence=grafeas.Occurrence(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Occurrence.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_occurrence(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/occurrences/*}" % client.transport._host, args[1])


def test_update_occurrence_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_occurrence(
            grafeas.UpdateOccurrenceRequest(),
            name='name_value',
            occurrence=grafeas.Occurrence(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_occurrence_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.GetOccurrenceNoteRequest,
    dict,
])
def test_get_occurrence_note_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note(
              name='name_value',
              short_description='short_description_value',
              long_description='long_description_value',
              kind=common.NoteKind.VULNERABILITY,
              related_note_names=['related_note_names_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_occurrence_note(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_get_occurrence_note_rest_required_fields(request_type=grafeas.GetOccurrenceNoteRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_occurrence_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_occurrence_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Note()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Note.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_occurrence_note(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_occurrence_note_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_occurrence_note._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_occurrence_note_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_get_occurrence_note") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_get_occurrence_note") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.GetOccurrenceNoteRequest.pb(grafeas.GetOccurrenceNoteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Note.to_json(grafeas.Note())

        request = grafeas.GetOccurrenceNoteRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Note()

        client.get_occurrence_note(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_occurrence_note_rest_bad_request(transport: str = 'rest', request_type=grafeas.GetOccurrenceNoteRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/occurrences/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_occurrence_note(request)


def test_get_occurrence_note_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/occurrences/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_occurrence_note(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/occurrences/*}/notes" % client.transport._host, args[1])


def test_get_occurrence_note_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_occurrence_note(
            grafeas.GetOccurrenceNoteRequest(),
            name='name_value',
        )


def test_get_occurrence_note_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.GetNoteRequest,
    dict,
])
def test_get_note_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note(
              name='name_value',
              short_description='short_description_value',
              long_description='long_description_value',
              kind=common.NoteKind.VULNERABILITY,
              related_note_names=['related_note_names_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_note(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_get_note_rest_required_fields(request_type=grafeas.GetNoteRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Note()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Note.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_note(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_note_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_note._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_note_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_get_note") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_get_note") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.GetNoteRequest.pb(grafeas.GetNoteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Note.to_json(grafeas.Note())

        request = grafeas.GetNoteRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Note()

        client.get_note(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_note_rest_bad_request(transport: str = 'rest', request_type=grafeas.GetNoteRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_note(request)


def test_get_note_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/notes/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_note(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/notes/*}" % client.transport._host, args[1])


def test_get_note_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_note(
            grafeas.GetNoteRequest(),
            name='name_value',
        )


def test_get_note_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.ListNotesRequest,
    dict,
])
def test_list_notes_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.ListNotesResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.ListNotesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_notes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_notes_rest_required_fields(request_type=grafeas.ListNotesRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_notes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_notes._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.ListNotesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.ListNotesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_notes(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_notes_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_notes._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_notes_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_list_notes") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_list_notes") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.ListNotesRequest.pb(grafeas.ListNotesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.ListNotesResponse.to_json(grafeas.ListNotesResponse())

        request = grafeas.ListNotesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.ListNotesResponse()

        client.list_notes(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_notes_rest_bad_request(transport: str = 'rest', request_type=grafeas.ListNotesRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_notes(request)


def test_list_notes_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.ListNotesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            filter='filter_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.ListNotesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_notes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*}/notes" % client.transport._host, args[1])


def test_list_notes_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notes(
            grafeas.ListNotesRequest(),
            parent='parent_value',
            filter='filter_value',
        )


def test_list_notes_rest_pager(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                    grafeas.Note(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNotesResponse(
                notes=[],
                next_page_token='def',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNotesResponse(
                notes=[
                    grafeas.Note(),
                    grafeas.Note(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(grafeas.ListNotesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1'}

        pager = client.list_notes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Note)
                for i in results)

        pages = list(client.list_notes(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    grafeas.DeleteNoteRequest,
    dict,
])
def test_delete_note_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_note(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_note_rest_required_fields(request_type=grafeas.DeleteNoteRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ''

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_note(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_note_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_note._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_note_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_delete_note") as pre:
        pre.assert_not_called()
        pb_message = grafeas.DeleteNoteRequest.pb(grafeas.DeleteNoteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = grafeas.DeleteNoteRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_note(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()


def test_delete_note_rest_bad_request(transport: str = 'rest', request_type=grafeas.DeleteNoteRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_note(request)


def test_delete_note_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/notes/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_note(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/notes/*}" % client.transport._host, args[1])


def test_delete_note_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_note(
            grafeas.DeleteNoteRequest(),
            name='name_value',
        )


def test_delete_note_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.CreateNoteRequest,
    dict,
])
def test_create_note_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request_init["note"] = {'name': 'name_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'kind': 1, 'related_url': [{'url': 'url_value', 'label': 'label_value'}], 'expiration_time': {'seconds': 751, 'nanos': 543}, 'create_time': {}, 'update_time': {}, 'related_note_names': ['related_note_names_value1', 'related_note_names_value2'], 'vulnerability': {'cvss_score': 0.1082, 'severity': 1, 'details': [{'severity_name': 'severity_name_value', 'description': 'description_value', 'package_type': 'package_type_value', 'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version_start': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'affected_version_end': {}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'is_obsolete': True, 'source_update_time': {}, 'source': 'source_value', 'vendor': 'vendor_value'}], 'cvss_v3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'windows_details': [{'cpe_uri': 'cpe_uri_value', 'name': 'name_value', 'description': 'description_value', 'fixing_kbs': [{'name': 'name_value', 'url': 'url_value'}]}], 'source_update_time': {}, 'cvss_version': 1, 'cvss_v2': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}}, 'build': {'builder_version': 'builder_version_value'}, 'image': {'resource_url': 'resource_url_value', 'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}}, 'package': {'name': 'name_value', 'distribution': [{'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'latest_version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value', 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'digest': [{'algo': 'algo_value', 'digest_bytes': b'digest_bytes_blob'}]}, 'deployment': {'resource_uri': ['resource_uri_value1', 'resource_uri_value2']}, 'discovery': {'analysis_kind': 1}, 'attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'upgrade': {'package': 'package_value', 'version': {}, 'distributions': [{'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}], 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'title': 'title_value', 'description': 'description_value', 'version': [{'cpe_uri': 'cpe_uri_value', 'benchmark_document': 'benchmark_document_value', 'version': 'version_value'}], 'rationale': 'rationale_value', 'remediation': 'remediation_value', 'cis_benchmark': {'profile_level': 1384, 'severity': 1}, 'scan_instructions': b'scan_instructions_blob'}, 'dsse_attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'vulnerability_assessment': {'title': 'title_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'language_code': 'language_code_value', 'publisher': {'name': 'name_value', 'issuing_authority': 'issuing_authority_value', 'publisher_namespace': 'publisher_namespace_value'}, 'product': {'name': 'name_value', 'id': 'id_value', 'generic_uri': 'generic_uri_value'}, 'assessment': {'cve': 'cve_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_uris': {}, 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'justification': {'justification_type': 1, 'details': 'details_value'}, 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}]}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note(
              name='name_value',
              short_description='short_description_value',
              long_description='long_description_value',
              kind=common.NoteKind.VULNERABILITY,
              related_note_names=['related_note_names_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_note(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_create_note_rest_required_fields(request_type=grafeas.CreateNoteRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["note_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "noteId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "noteId" in jsonified_request
    assert jsonified_request["noteId"] == request_init["note_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["noteId"] = 'note_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_note._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("note_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "noteId" in jsonified_request
    assert jsonified_request["noteId"] == 'note_id_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Note()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Note.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_note(request)

            expected_params = [
                (
                    "noteId",
                    "",
                ),
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_note_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_note._get_unset_required_fields({})
    assert set(unset_fields) == (set(("noteId", )) & set(("parent", "noteId", "note", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_note_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_create_note") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_create_note") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.CreateNoteRequest.pb(grafeas.CreateNoteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Note.to_json(grafeas.Note())

        request = grafeas.CreateNoteRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Note()

        client.create_note(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_note_rest_bad_request(transport: str = 'rest', request_type=grafeas.CreateNoteRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request_init["note"] = {'name': 'name_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'kind': 1, 'related_url': [{'url': 'url_value', 'label': 'label_value'}], 'expiration_time': {'seconds': 751, 'nanos': 543}, 'create_time': {}, 'update_time': {}, 'related_note_names': ['related_note_names_value1', 'related_note_names_value2'], 'vulnerability': {'cvss_score': 0.1082, 'severity': 1, 'details': [{'severity_name': 'severity_name_value', 'description': 'description_value', 'package_type': 'package_type_value', 'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version_start': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'affected_version_end': {}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'is_obsolete': True, 'source_update_time': {}, 'source': 'source_value', 'vendor': 'vendor_value'}], 'cvss_v3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'windows_details': [{'cpe_uri': 'cpe_uri_value', 'name': 'name_value', 'description': 'description_value', 'fixing_kbs': [{'name': 'name_value', 'url': 'url_value'}]}], 'source_update_time': {}, 'cvss_version': 1, 'cvss_v2': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}}, 'build': {'builder_version': 'builder_version_value'}, 'image': {'resource_url': 'resource_url_value', 'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}}, 'package': {'name': 'name_value', 'distribution': [{'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'latest_version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value', 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'digest': [{'algo': 'algo_value', 'digest_bytes': b'digest_bytes_blob'}]}, 'deployment': {'resource_uri': ['resource_uri_value1', 'resource_uri_value2']}, 'discovery': {'analysis_kind': 1}, 'attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'upgrade': {'package': 'package_value', 'version': {}, 'distributions': [{'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}], 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'title': 'title_value', 'description': 'description_value', 'version': [{'cpe_uri': 'cpe_uri_value', 'benchmark_document': 'benchmark_document_value', 'version': 'version_value'}], 'rationale': 'rationale_value', 'remediation': 'remediation_value', 'cis_benchmark': {'profile_level': 1384, 'severity': 1}, 'scan_instructions': b'scan_instructions_blob'}, 'dsse_attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'vulnerability_assessment': {'title': 'title_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'language_code': 'language_code_value', 'publisher': {'name': 'name_value', 'issuing_authority': 'issuing_authority_value', 'publisher_namespace': 'publisher_namespace_value'}, 'product': {'name': 'name_value', 'id': 'id_value', 'generic_uri': 'generic_uri_value'}, 'assessment': {'cve': 'cve_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_uris': {}, 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'justification': {'justification_type': 1, 'details': 'details_value'}, 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}]}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_note(request)


def test_create_note_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            note_id='note_id_value',
            note=grafeas.Note(name='name_value'),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_note(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*}/notes" % client.transport._host, args[1])


def test_create_note_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_note(
            grafeas.CreateNoteRequest(),
            parent='parent_value',
            note_id='note_id_value',
            note=grafeas.Note(name='name_value'),
        )


def test_create_note_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.BatchCreateNotesRequest,
    dict,
])
def test_batch_create_notes_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.BatchCreateNotesResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.BatchCreateNotesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.batch_create_notes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateNotesResponse)


def test_batch_create_notes_rest_required_fields(request_type=grafeas.BatchCreateNotesRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_create_notes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_create_notes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.BatchCreateNotesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.BatchCreateNotesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.batch_create_notes(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_batch_create_notes_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.batch_create_notes._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "notes", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_create_notes_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_batch_create_notes") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_batch_create_notes") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.BatchCreateNotesRequest.pb(grafeas.BatchCreateNotesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.BatchCreateNotesResponse.to_json(grafeas.BatchCreateNotesResponse())

        request = grafeas.BatchCreateNotesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.BatchCreateNotesResponse()

        client.batch_create_notes(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_create_notes_rest_bad_request(transport: str = 'rest', request_type=grafeas.BatchCreateNotesRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_create_notes(request)


def test_batch_create_notes_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.BatchCreateNotesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            notes={'key_value': grafeas.Note(name='name_value')},
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.BatchCreateNotesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.batch_create_notes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*}/notes:batchCreate" % client.transport._host, args[1])


def test_batch_create_notes_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_notes(
            grafeas.BatchCreateNotesRequest(),
            parent='parent_value',
            notes={'key_value': grafeas.Note(name='name_value')},
        )


def test_batch_create_notes_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.UpdateNoteRequest,
    dict,
])
def test_update_note_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request_init["note"] = {'name': 'name_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'kind': 1, 'related_url': [{'url': 'url_value', 'label': 'label_value'}], 'expiration_time': {'seconds': 751, 'nanos': 543}, 'create_time': {}, 'update_time': {}, 'related_note_names': ['related_note_names_value1', 'related_note_names_value2'], 'vulnerability': {'cvss_score': 0.1082, 'severity': 1, 'details': [{'severity_name': 'severity_name_value', 'description': 'description_value', 'package_type': 'package_type_value', 'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version_start': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'affected_version_end': {}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'is_obsolete': True, 'source_update_time': {}, 'source': 'source_value', 'vendor': 'vendor_value'}], 'cvss_v3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'windows_details': [{'cpe_uri': 'cpe_uri_value', 'name': 'name_value', 'description': 'description_value', 'fixing_kbs': [{'name': 'name_value', 'url': 'url_value'}]}], 'source_update_time': {}, 'cvss_version': 1, 'cvss_v2': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}}, 'build': {'builder_version': 'builder_version_value'}, 'image': {'resource_url': 'resource_url_value', 'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}}, 'package': {'name': 'name_value', 'distribution': [{'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'latest_version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value', 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'digest': [{'algo': 'algo_value', 'digest_bytes': b'digest_bytes_blob'}]}, 'deployment': {'resource_uri': ['resource_uri_value1', 'resource_uri_value2']}, 'discovery': {'analysis_kind': 1}, 'attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'upgrade': {'package': 'package_value', 'version': {}, 'distributions': [{'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}], 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'title': 'title_value', 'description': 'description_value', 'version': [{'cpe_uri': 'cpe_uri_value', 'benchmark_document': 'benchmark_document_value', 'version': 'version_value'}], 'rationale': 'rationale_value', 'remediation': 'remediation_value', 'cis_benchmark': {'profile_level': 1384, 'severity': 1}, 'scan_instructions': b'scan_instructions_blob'}, 'dsse_attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'vulnerability_assessment': {'title': 'title_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'language_code': 'language_code_value', 'publisher': {'name': 'name_value', 'issuing_authority': 'issuing_authority_value', 'publisher_namespace': 'publisher_namespace_value'}, 'product': {'name': 'name_value', 'id': 'id_value', 'generic_uri': 'generic_uri_value'}, 'assessment': {'cve': 'cve_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_uris': {}, 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'justification': {'justification_type': 1, 'details': 'details_value'}, 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}]}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note(
              name='name_value',
              short_description='short_description_value',
              long_description='long_description_value',
              kind=common.NoteKind.VULNERABILITY,
              related_note_names=['related_note_names_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_note(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == 'name_value'
    assert response.short_description == 'short_description_value'
    assert response.long_description == 'long_description_value'
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ['related_note_names_value']


def test_update_note_rest_required_fields(request_type=grafeas.UpdateNoteRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_note._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_note._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.Note()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.Note.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_note(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_note_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_note._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("name", "note", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_note_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_update_note") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_update_note") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.UpdateNoteRequest.pb(grafeas.UpdateNoteRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.Note.to_json(grafeas.Note())

        request = grafeas.UpdateNoteRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.Note()

        client.update_note(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_note_rest_bad_request(transport: str = 'rest', request_type=grafeas.UpdateNoteRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request_init["note"] = {'name': 'name_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'kind': 1, 'related_url': [{'url': 'url_value', 'label': 'label_value'}], 'expiration_time': {'seconds': 751, 'nanos': 543}, 'create_time': {}, 'update_time': {}, 'related_note_names': ['related_note_names_value1', 'related_note_names_value2'], 'vulnerability': {'cvss_score': 0.1082, 'severity': 1, 'details': [{'severity_name': 'severity_name_value', 'description': 'description_value', 'package_type': 'package_type_value', 'affected_cpe_uri': 'affected_cpe_uri_value', 'affected_package': 'affected_package_value', 'affected_version_start': {'epoch': 527, 'name': 'name_value', 'revision': 'revision_value', 'inclusive': True, 'kind': 1, 'full_name': 'full_name_value'}, 'affected_version_end': {}, 'fixed_cpe_uri': 'fixed_cpe_uri_value', 'fixed_package': 'fixed_package_value', 'fixed_version': {}, 'is_obsolete': True, 'source_update_time': {}, 'source': 'source_value', 'vendor': 'vendor_value'}], 'cvss_v3': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}, 'windows_details': [{'cpe_uri': 'cpe_uri_value', 'name': 'name_value', 'description': 'description_value', 'fixing_kbs': [{'name': 'name_value', 'url': 'url_value'}]}], 'source_update_time': {}, 'cvss_version': 1, 'cvss_v2': {'base_score': 0.1046, 'exploitability_score': 0.21580000000000002, 'impact_score': 0.1273, 'attack_vector': 1, 'attack_complexity': 1, 'authentication': 1, 'privileges_required': 1, 'user_interaction': 1, 'scope': 1, 'confidentiality_impact': 1, 'integrity_impact': 1, 'availability_impact': 1}}, 'build': {'builder_version': 'builder_version_value'}, 'image': {'resource_url': 'resource_url_value', 'fingerprint': {'v1_name': 'v1_name_value', 'v2_blob': ['v2_blob_value1', 'v2_blob_value2'], 'v2_name': 'v2_name_value'}}, 'package': {'name': 'name_value', 'distribution': [{'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'latest_version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value'}], 'package_type': 'package_type_value', 'cpe_uri': 'cpe_uri_value', 'architecture': 1, 'version': {}, 'maintainer': 'maintainer_value', 'url': 'url_value', 'description': 'description_value', 'license_': {'expression': 'expression_value', 'comments': 'comments_value'}, 'digest': [{'algo': 'algo_value', 'digest_bytes': b'digest_bytes_blob'}]}, 'deployment': {'resource_uri': ['resource_uri_value1', 'resource_uri_value2']}, 'discovery': {'analysis_kind': 1}, 'attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'upgrade': {'package': 'package_value', 'version': {}, 'distributions': [{'cpe_uri': 'cpe_uri_value', 'classification': 'classification_value', 'severity': 'severity_value', 'cve': ['cve_value1', 'cve_value2']}], 'windows_update': {'identity': {'update_id': 'update_id_value', 'revision': 879}, 'title': 'title_value', 'description': 'description_value', 'categories': [{'category_id': 'category_id_value', 'name': 'name_value'}], 'kb_article_ids': ['kb_article_ids_value1', 'kb_article_ids_value2'], 'support_url': 'support_url_value', 'last_published_timestamp': {}}}, 'compliance': {'title': 'title_value', 'description': 'description_value', 'version': [{'cpe_uri': 'cpe_uri_value', 'benchmark_document': 'benchmark_document_value', 'version': 'version_value'}], 'rationale': 'rationale_value', 'remediation': 'remediation_value', 'cis_benchmark': {'profile_level': 1384, 'severity': 1}, 'scan_instructions': b'scan_instructions_blob'}, 'dsse_attestation': {'hint': {'human_readable_name': 'human_readable_name_value'}}, 'vulnerability_assessment': {'title': 'title_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'language_code': 'language_code_value', 'publisher': {'name': 'name_value', 'issuing_authority': 'issuing_authority_value', 'publisher_namespace': 'publisher_namespace_value'}, 'product': {'name': 'name_value', 'id': 'id_value', 'generic_uri': 'generic_uri_value'}, 'assessment': {'cve': 'cve_value', 'short_description': 'short_description_value', 'long_description': 'long_description_value', 'related_uris': {}, 'state': 1, 'impacts': ['impacts_value1', 'impacts_value2'], 'justification': {'justification_type': 1, 'details': 'details_value'}, 'remediations': [{'remediation_type': 1, 'details': 'details_value', 'remediation_uri': {}}]}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_note(request)


def test_update_note_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.Note()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/notes/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            note=grafeas.Note(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.Note.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_note(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/notes/*}" % client.transport._host, args[1])


def test_update_note_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_note(
            grafeas.UpdateNoteRequest(),
            name='name_value',
            note=grafeas.Note(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_note_rest_error():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    grafeas.ListNoteOccurrencesRequest,
    dict,
])
def test_list_note_occurrences_rest(request_type):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.ListNoteOccurrencesResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.ListNoteOccurrencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_note_occurrences(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNoteOccurrencesPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_note_occurrences_rest_required_fields(request_type=grafeas.ListNoteOccurrencesRequest):
    transport_class = transports.GrafeasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_note_occurrences._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_note_occurrences._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = grafeas.ListNoteOccurrencesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = grafeas.ListNoteOccurrencesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_note_occurrences(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_note_occurrences_rest_unset_required_fields():
    transport = transports.GrafeasRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_note_occurrences._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "pageSize", "pageToken", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_note_occurrences_rest_interceptors(null_interceptor):
    transport = transports.GrafeasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.GrafeasRestInterceptor(),
        )
    client = GrafeasClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.GrafeasRestInterceptor, "post_list_note_occurrences") as post, \
         mock.patch.object(transports.GrafeasRestInterceptor, "pre_list_note_occurrences") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = grafeas.ListNoteOccurrencesRequest.pb(grafeas.ListNoteOccurrencesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = grafeas.ListNoteOccurrencesResponse.to_json(grafeas.ListNoteOccurrencesResponse())

        request = grafeas.ListNoteOccurrencesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = grafeas.ListNoteOccurrencesResponse()

        client.list_note_occurrences(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_note_occurrences_rest_bad_request(transport: str = 'rest', request_type=grafeas.ListNoteOccurrencesRequest):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/notes/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_note_occurrences(request)


def test_list_note_occurrences_rest_flattened():
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = grafeas.ListNoteOccurrencesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/notes/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            filter='filter_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = grafeas.ListNoteOccurrencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_note_occurrences(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/notes/*}/occurrences" % client.transport._host, args[1])


def test_list_note_occurrences_rest_flattened_error(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_note_occurrences(
            grafeas.ListNoteOccurrencesRequest(),
            name='name_value',
            filter='filter_value',
        )


def test_list_note_occurrences_rest_pager(transport: str = 'rest'):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token='abc',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[],
                next_page_token='def',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                ],
                next_page_token='ghi',
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(grafeas.ListNoteOccurrencesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'name': 'projects/sample1/notes/sample2'}

        pager = client.list_note_occurrences(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Occurrence)
                for i in results)

        pages = list(client.list_note_occurrences(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.GrafeasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = GrafeasClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.GrafeasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = GrafeasClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.GrafeasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = GrafeasClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = GrafeasClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.GrafeasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = GrafeasClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GrafeasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = GrafeasClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GrafeasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.GrafeasGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.GrafeasGrpcTransport,
    transports.GrafeasGrpcAsyncIOTransport,
    transports.GrafeasRestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = GrafeasClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.GrafeasGrpcTransport,
    )

def test_grafeas_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.GrafeasTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_grafeas_base_transport():
    # Instantiate the base transport.
    with mock.patch('grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.GrafeasTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'get_occurrence',
        'list_occurrences',
        'delete_occurrence',
        'create_occurrence',
        'batch_create_occurrences',
        'update_occurrence',
        'get_occurrence_note',
        'get_note',
        'list_notes',
        'delete_note',
        'create_note',
        'batch_create_notes',
        'update_note',
        'list_note_occurrences',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_grafeas_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.GrafeasTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
),
            quota_project_id="octopus",
        )


def test_grafeas_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.GrafeasTransport()
        adc.assert_called_once()


def test_grafeas_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        GrafeasClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.GrafeasGrpcTransport,
        transports.GrafeasGrpcAsyncIOTransport,
    ],
)
def test_grafeas_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.GrafeasGrpcTransport,
        transports.GrafeasGrpcAsyncIOTransport,
        transports.GrafeasRestTransport,
    ],
)
def test_grafeas_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.GrafeasGrpcTransport, grpc_helpers),
        (transports.GrafeasGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_grafeas_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "containeranalysis.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
),
            scopes=["1", "2"],
            default_host="containeranalysis.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport])
def test_grafeas_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )

def test_grafeas_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.GrafeasRestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_grafeas_host_no_port(transport_name):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='containeranalysis.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'containeranalysis.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://containeranalysis.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_grafeas_host_with_port(transport_name):
    client = GrafeasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='containeranalysis.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'containeranalysis.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://containeranalysis.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_grafeas_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = GrafeasClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = GrafeasClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_occurrence._session
    session2 = client2.transport.get_occurrence._session
    assert session1 != session2
    session1 = client1.transport.list_occurrences._session
    session2 = client2.transport.list_occurrences._session
    assert session1 != session2
    session1 = client1.transport.delete_occurrence._session
    session2 = client2.transport.delete_occurrence._session
    assert session1 != session2
    session1 = client1.transport.create_occurrence._session
    session2 = client2.transport.create_occurrence._session
    assert session1 != session2
    session1 = client1.transport.batch_create_occurrences._session
    session2 = client2.transport.batch_create_occurrences._session
    assert session1 != session2
    session1 = client1.transport.update_occurrence._session
    session2 = client2.transport.update_occurrence._session
    assert session1 != session2
    session1 = client1.transport.get_occurrence_note._session
    session2 = client2.transport.get_occurrence_note._session
    assert session1 != session2
    session1 = client1.transport.get_note._session
    session2 = client2.transport.get_note._session
    assert session1 != session2
    session1 = client1.transport.list_notes._session
    session2 = client2.transport.list_notes._session
    assert session1 != session2
    session1 = client1.transport.delete_note._session
    session2 = client2.transport.delete_note._session
    assert session1 != session2
    session1 = client1.transport.create_note._session
    session2 = client2.transport.create_note._session
    assert session1 != session2
    session1 = client1.transport.batch_create_notes._session
    session2 = client2.transport.batch_create_notes._session
    assert session1 != session2
    session1 = client1.transport.update_note._session
    session2 = client2.transport.update_note._session
    assert session1 != session2
    session1 = client1.transport.list_note_occurrences._session
    session2 = client2.transport.list_note_occurrences._session
    assert session1 != session2
def test_grafeas_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.GrafeasGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_grafeas_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.GrafeasGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport])
def test_grafeas_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport])
def test_grafeas_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_note_path():
    project = "squid"
    note = "clam"
    expected = "projects/{project}/notes/{note}".format(project=project, note=note, )
    actual = GrafeasClient.note_path(project, note)
    assert expected == actual


def test_parse_note_path():
    expected = {
        "project": "whelk",
        "note": "octopus",
    }
    path = GrafeasClient.note_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_note_path(path)
    assert expected == actual

def test_occurrence_path():
    project = "oyster"
    occurrence = "nudibranch"
    expected = "projects/{project}/occurrences/{occurrence}".format(project=project, occurrence=occurrence, )
    actual = GrafeasClient.occurrence_path(project, occurrence)
    assert expected == actual


def test_parse_occurrence_path():
    expected = {
        "project": "cuttlefish",
        "occurrence": "mussel",
    }
    path = GrafeasClient.occurrence_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_occurrence_path(path)
    assert expected == actual

def test_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project, )
    actual = GrafeasClient.project_path(project)
    assert expected == actual


def test_parse_project_path():
    expected = {
        "project": "nautilus",
    }
    path = GrafeasClient.project_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_project_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = GrafeasClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = GrafeasClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(folder=folder, )
    actual = GrafeasClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = GrafeasClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = GrafeasClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = GrafeasClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(project=project, )
    actual = GrafeasClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = GrafeasClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = GrafeasClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = GrafeasClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.GrafeasTransport, '_prep_wrapped_messages') as prep:
        client = GrafeasClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.GrafeasTransport, '_prep_wrapped_messages') as prep:
        transport_class = GrafeasClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = GrafeasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = GrafeasClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = GrafeasClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (GrafeasClient, transports.GrafeasGrpcTransport),
    (GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport),
])
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
