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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials   # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc                        # type: ignore
from grpc.experimental import aio  # type: ignore

from google.protobuf import empty_pb2  # type: ignore
from grafeas.grafeas_v1.types import grafeas
from .base import GrafeasTransport, DEFAULT_CLIENT_INFO
from .grpc import GrafeasGrpcTransport


class GrafeasGrpcAsyncIOTransport(GrafeasTransport):
    """gRPC AsyncIO backend transport for Grafeas.

    `Grafeas <https://grafeas.io>`__ API.

    Retrieves analysis results of Cloud components such as Docker
    container images.

    Analysis results are stored as a series of occurrences. An
    ``Occurrence`` contains information about a specific analysis
    instance on a resource. An occurrence refers to a ``Note``. A note
    contains details describing the analysis and is generally stored in
    a separate project, called a ``Provider``. Multiple occurrences can
    refer to the same note.

    For example, an SSL vulnerability could affect multiple images. In
    this case, there would be one note for the vulnerability and an
    occurrence for each image with the vulnerability referring to that
    note.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(cls,
                       host: str = 'containeranalysis.googleapis.com',
                       credentials: ga_credentials.Credentials = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs
        )

    def __init__(self, *,
            host: str = 'containeranalysis.googleapis.com',
            credentials: ga_credentials.Credentials = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            channel: aio.Channel = None,
            api_mtls_endpoint: str = None,
            client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
            ssl_channel_credentials: grpc.ChannelCredentials = None,
            client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
            quota_project_id=None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def get_occurrence(self) -> Callable[
            [grafeas.GetOccurrenceRequest],
            Awaitable[grafeas.Occurrence]]:
        r"""Return a callable for the get occurrence method over gRPC.

        Gets the specified occurrence.

        Returns:
            Callable[[~.GetOccurrenceRequest],
                    Awaitable[~.Occurrence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_occurrence' not in self._stubs:
            self._stubs['get_occurrence'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/GetOccurrence',
                request_serializer=grafeas.GetOccurrenceRequest.serialize,
                response_deserializer=grafeas.Occurrence.deserialize,
            )
        return self._stubs['get_occurrence']

    @property
    def list_occurrences(self) -> Callable[
            [grafeas.ListOccurrencesRequest],
            Awaitable[grafeas.ListOccurrencesResponse]]:
        r"""Return a callable for the list occurrences method over gRPC.

        Lists occurrences for the specified project.

        Returns:
            Callable[[~.ListOccurrencesRequest],
                    Awaitable[~.ListOccurrencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_occurrences' not in self._stubs:
            self._stubs['list_occurrences'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/ListOccurrences',
                request_serializer=grafeas.ListOccurrencesRequest.serialize,
                response_deserializer=grafeas.ListOccurrencesResponse.deserialize,
            )
        return self._stubs['list_occurrences']

    @property
    def delete_occurrence(self) -> Callable[
            [grafeas.DeleteOccurrenceRequest],
            Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete occurrence method over gRPC.

        Deletes the specified occurrence. For example, use
        this method to delete an occurrence when the occurrence
        is no longer applicable for the given resource.

        Returns:
            Callable[[~.DeleteOccurrenceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_occurrence' not in self._stubs:
            self._stubs['delete_occurrence'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/DeleteOccurrence',
                request_serializer=grafeas.DeleteOccurrenceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_occurrence']

    @property
    def create_occurrence(self) -> Callable[
            [grafeas.CreateOccurrenceRequest],
            Awaitable[grafeas.Occurrence]]:
        r"""Return a callable for the create occurrence method over gRPC.

        Creates a new occurrence.

        Returns:
            Callable[[~.CreateOccurrenceRequest],
                    Awaitable[~.Occurrence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_occurrence' not in self._stubs:
            self._stubs['create_occurrence'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/CreateOccurrence',
                request_serializer=grafeas.CreateOccurrenceRequest.serialize,
                response_deserializer=grafeas.Occurrence.deserialize,
            )
        return self._stubs['create_occurrence']

    @property
    def batch_create_occurrences(self) -> Callable[
            [grafeas.BatchCreateOccurrencesRequest],
            Awaitable[grafeas.BatchCreateOccurrencesResponse]]:
        r"""Return a callable for the batch create occurrences method over gRPC.

        Creates new occurrences in batch.

        Returns:
            Callable[[~.BatchCreateOccurrencesRequest],
                    Awaitable[~.BatchCreateOccurrencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'batch_create_occurrences' not in self._stubs:
            self._stubs['batch_create_occurrences'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/BatchCreateOccurrences',
                request_serializer=grafeas.BatchCreateOccurrencesRequest.serialize,
                response_deserializer=grafeas.BatchCreateOccurrencesResponse.deserialize,
            )
        return self._stubs['batch_create_occurrences']

    @property
    def update_occurrence(self) -> Callable[
            [grafeas.UpdateOccurrenceRequest],
            Awaitable[grafeas.Occurrence]]:
        r"""Return a callable for the update occurrence method over gRPC.

        Updates the specified occurrence.

        Returns:
            Callable[[~.UpdateOccurrenceRequest],
                    Awaitable[~.Occurrence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_occurrence' not in self._stubs:
            self._stubs['update_occurrence'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/UpdateOccurrence',
                request_serializer=grafeas.UpdateOccurrenceRequest.serialize,
                response_deserializer=grafeas.Occurrence.deserialize,
            )
        return self._stubs['update_occurrence']

    @property
    def get_occurrence_note(self) -> Callable[
            [grafeas.GetOccurrenceNoteRequest],
            Awaitable[grafeas.Note]]:
        r"""Return a callable for the get occurrence note method over gRPC.

        Gets the note attached to the specified occurrence.
        Consumer projects can use this method to get a note that
        belongs to a provider project.

        Returns:
            Callable[[~.GetOccurrenceNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_occurrence_note' not in self._stubs:
            self._stubs['get_occurrence_note'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/GetOccurrenceNote',
                request_serializer=grafeas.GetOccurrenceNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs['get_occurrence_note']

    @property
    def get_note(self) -> Callable[
            [grafeas.GetNoteRequest],
            Awaitable[grafeas.Note]]:
        r"""Return a callable for the get note method over gRPC.

        Gets the specified note.

        Returns:
            Callable[[~.GetNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_note' not in self._stubs:
            self._stubs['get_note'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/GetNote',
                request_serializer=grafeas.GetNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs['get_note']

    @property
    def list_notes(self) -> Callable[
            [grafeas.ListNotesRequest],
            Awaitable[grafeas.ListNotesResponse]]:
        r"""Return a callable for the list notes method over gRPC.

        Lists notes for the specified project.

        Returns:
            Callable[[~.ListNotesRequest],
                    Awaitable[~.ListNotesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_notes' not in self._stubs:
            self._stubs['list_notes'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/ListNotes',
                request_serializer=grafeas.ListNotesRequest.serialize,
                response_deserializer=grafeas.ListNotesResponse.deserialize,
            )
        return self._stubs['list_notes']

    @property
    def delete_note(self) -> Callable[
            [grafeas.DeleteNoteRequest],
            Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete note method over gRPC.

        Deletes the specified note.

        Returns:
            Callable[[~.DeleteNoteRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_note' not in self._stubs:
            self._stubs['delete_note'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/DeleteNote',
                request_serializer=grafeas.DeleteNoteRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_note']

    @property
    def create_note(self) -> Callable[
            [grafeas.CreateNoteRequest],
            Awaitable[grafeas.Note]]:
        r"""Return a callable for the create note method over gRPC.

        Creates a new note.

        Returns:
            Callable[[~.CreateNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_note' not in self._stubs:
            self._stubs['create_note'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/CreateNote',
                request_serializer=grafeas.CreateNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs['create_note']

    @property
    def batch_create_notes(self) -> Callable[
            [grafeas.BatchCreateNotesRequest],
            Awaitable[grafeas.BatchCreateNotesResponse]]:
        r"""Return a callable for the batch create notes method over gRPC.

        Creates new notes in batch.

        Returns:
            Callable[[~.BatchCreateNotesRequest],
                    Awaitable[~.BatchCreateNotesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'batch_create_notes' not in self._stubs:
            self._stubs['batch_create_notes'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/BatchCreateNotes',
                request_serializer=grafeas.BatchCreateNotesRequest.serialize,
                response_deserializer=grafeas.BatchCreateNotesResponse.deserialize,
            )
        return self._stubs['batch_create_notes']

    @property
    def update_note(self) -> Callable[
            [grafeas.UpdateNoteRequest],
            Awaitable[grafeas.Note]]:
        r"""Return a callable for the update note method over gRPC.

        Updates the specified note.

        Returns:
            Callable[[~.UpdateNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_note' not in self._stubs:
            self._stubs['update_note'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/UpdateNote',
                request_serializer=grafeas.UpdateNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs['update_note']

    @property
    def list_note_occurrences(self) -> Callable[
            [grafeas.ListNoteOccurrencesRequest],
            Awaitable[grafeas.ListNoteOccurrencesResponse]]:
        r"""Return a callable for the list note occurrences method over gRPC.

        Lists occurrences referencing the specified note.
        Provider projects can use this method to get all
        occurrences across consumer projects referencing the
        specified note.

        Returns:
            Callable[[~.ListNoteOccurrencesRequest],
                    Awaitable[~.ListNoteOccurrencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_note_occurrences' not in self._stubs:
            self._stubs['list_note_occurrences'] = self.grpc_channel.unary_unary(
                '/grafeas.v1.Grafeas/ListNoteOccurrences',
                request_serializer=grafeas.ListNoteOccurrencesRequest.serialize,
                response_deserializer=grafeas.ListNoteOccurrencesResponse.deserialize,
            )
        return self._stubs['list_note_occurrences']

    def close(self):
        return self.grpc_channel.close()


__all__ = (
    'GrafeasGrpcAsyncIOTransport',
)