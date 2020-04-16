# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grafeas_v1/proto/build.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grafeas.grafeas_v1.proto import (
    provenance_pb2 as grafeas__v1_dot_proto_dot_provenance__pb2,
)


DESCRIPTOR = _descriptor.FileDescriptor(
    name="grafeas_v1/proto/build.proto",
    package="grafeas.v1",
    syntax="proto3",
    serialized_options=_b(
        "\n\rio.grafeas.v1P\001Z8google.golang.org/genproto/googleapis/grafeas/v1;grafeas\242\002\003GRA"
    ),
    serialized_pb=_b(
        '\n\x1cgrafeas_v1/proto/build.proto\x12\ngrafeas.v1\x1a!grafeas_v1/proto/provenance.proto"$\n\tBuildNote\x12\x17\n\x0f\x62uilder_version\x18\x01 \x01(\t"\\\n\x0f\x42uildOccurrence\x12/\n\nprovenance\x18\x01 \x01(\x0b\x32\x1b.grafeas.v1.BuildProvenance\x12\x18\n\x10provenance_bytes\x18\x02 \x01(\tBQ\n\rio.grafeas.v1P\x01Z8google.golang.org/genproto/googleapis/grafeas/v1;grafeas\xa2\x02\x03GRAb\x06proto3'
    ),
    dependencies=[grafeas__v1_dot_proto_dot_provenance__pb2.DESCRIPTOR,],
)


_BUILDNOTE = _descriptor.Descriptor(
    name="BuildNote",
    full_name="grafeas.v1.BuildNote",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="builder_version",
            full_name="grafeas.v1.BuildNote.builder_version",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=79,
    serialized_end=115,
)


_BUILDOCCURRENCE = _descriptor.Descriptor(
    name="BuildOccurrence",
    full_name="grafeas.v1.BuildOccurrence",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="provenance",
            full_name="grafeas.v1.BuildOccurrence.provenance",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="provenance_bytes",
            full_name="grafeas.v1.BuildOccurrence.provenance_bytes",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=117,
    serialized_end=209,
)

_BUILDOCCURRENCE.fields_by_name[
    "provenance"
].message_type = grafeas__v1_dot_proto_dot_provenance__pb2._BUILDPROVENANCE
DESCRIPTOR.message_types_by_name["BuildNote"] = _BUILDNOTE
DESCRIPTOR.message_types_by_name["BuildOccurrence"] = _BUILDOCCURRENCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BuildNote = _reflection.GeneratedProtocolMessageType(
    "BuildNote",
    (_message.Message,),
    dict(
        DESCRIPTOR=_BUILDNOTE,
        __module__="grafeas_v1.proto.build_pb2",
        __doc__="""Note holding the version of the provider's builder and the signature
  of the provenance message in the build details occurrence.
  Attributes:
      builder_version:
          Required. Immutable. Version of the builder which produced
          this build.
  """,
        # @@protoc_insertion_point(class_scope:grafeas.v1.BuildNote)
    ),
)
_sym_db.RegisterMessage(BuildNote)

BuildOccurrence = _reflection.GeneratedProtocolMessageType(
    "BuildOccurrence",
    (_message.Message,),
    dict(
        DESCRIPTOR=_BUILDOCCURRENCE,
        __module__="grafeas_v1.proto.build_pb2",
        __doc__="""Details of a build occurrence.
  Attributes:
      provenance:
          Required. The actual provenance for the build.
      provenance_bytes:
          Serialized JSON representation of the provenance, used in
          generating the build signature in the corresponding build
          note. After verifying the signature, ``provenance_bytes`` can
          be unmarshalled and compared to the provenance to confirm that
          it is unchanged. A base64-encoded string representation of the
          provenance bytes is used for the signature in order to
          interoperate with openssl which expects this format for
          signature verification.  The serialized form is captured both
          to avoid ambiguity in how the provenance is marshalled to json
          as well to prevent incompatibilities with future changes.
  """,
        # @@protoc_insertion_point(class_scope:grafeas.v1.BuildOccurrence)
    ),
)
_sym_db.RegisterMessage(BuildOccurrence)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
