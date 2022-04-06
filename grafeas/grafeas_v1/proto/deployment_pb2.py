# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grafeas/grafeas_v1/proto/deployment.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="grafeas/grafeas_v1/proto/deployment.proto",
    package="grafeas.v1",
    syntax="proto3",
<<<<<<< HEAD
    serialized_options=b"\n\rio.grafeas.v1P\001ZFgoogle.golang.org/genproto/googleapis/grafeas/grafeas_v1/proto;grafeas\242\002\003GRA",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n)grafeas/grafeas_v1/proto/deployment.proto\x12\ngrafeas.v1\x1a\x1fgoogle/protobuf/timestamp.proto"&\n\x0e\x44\x65ploymentNote\x12\x14\n\x0cresource_uri\x18\x01 \x03(\t"\xc7\x02\n\x14\x44\x65ploymentOccurrence\x12\x12\n\nuser_email\x18\x01 \x01(\t\x12/\n\x0b\x64\x65ploy_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rundeploy_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06\x63onfig\x18\x04 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x05 \x01(\t\x12\x14\n\x0cresource_uri\x18\x06 \x03(\t\x12;\n\x08platform\x18\x07 \x01(\x0e\x32).grafeas.v1.DeploymentOccurrence.Platform"C\n\x08Platform\x12\x18\n\x14PLATFORM_UNSPECIFIED\x10\x00\x12\x07\n\x03GKE\x10\x01\x12\x08\n\x04\x46LEX\x10\x02\x12\n\n\x06\x43USTOM\x10\x03\x42_\n\rio.grafeas.v1P\x01ZFgoogle.golang.org/genproto/googleapis/grafeas/grafeas_v1/proto;grafeas\xa2\x02\x03GRAb\x06proto3',
    dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,],
=======
    serialized_options=_b(
        "\n\rio.grafeas.v1P\001Z8google.golang.org/genproto/googleapis/grafeas/v1;grafeas\242\002\003GRA"
    ),
    serialized_pb=_b(
        '\n!grafeas_v1/proto/deployment.proto\x12\ngrafeas.v1\x1a\x1fgoogle/protobuf/timestamp.proto"&\n\x0e\x44\x65ploymentNote\x12\x14\n\x0cresource_uri\x18\x01 \x03(\t"\xc7\x02\n\x14\x44\x65ploymentOccurrence\x12\x12\n\nuser_email\x18\x01 \x01(\t\x12/\n\x0b\x64\x65ploy_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rundeploy_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06\x63onfig\x18\x04 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x05 \x01(\t\x12\x14\n\x0cresource_uri\x18\x06 \x03(\t\x12;\n\x08platform\x18\x07 \x01(\x0e\x32).grafeas.v1.DeploymentOccurrence.Platform"C\n\x08Platform\x12\x18\n\x14PLATFORM_UNSPECIFIED\x10\x00\x12\x07\n\x03GKE\x10\x01\x12\x08\n\x04\x46LEX\x10\x02\x12\n\n\x06\x43USTOM\x10\x03\x42Q\n\rio.grafeas.v1P\x01Z8google.golang.org/genproto/googleapis/grafeas/v1;grafeas\xa2\x02\x03GRAb\x06proto3'
    ),
    dependencies=[
        google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,
    ],
>>>>>>> v0-old
)


_DEPLOYMENTOCCURRENCE_PLATFORM = _descriptor.EnumDescriptor(
    name="Platform",
    full_name="grafeas.v1.DeploymentOccurrence.Platform",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PLATFORM_UNSPECIFIED",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="GKE",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="FLEX",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="CUSTOM",
            index=3,
            number=3,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=391,
    serialized_end=458,
)
_sym_db.RegisterEnumDescriptor(_DEPLOYMENTOCCURRENCE_PLATFORM)


_DEPLOYMENTNOTE = _descriptor.Descriptor(
    name="DeploymentNote",
    full_name="grafeas.v1.DeploymentNote",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="resource_uri",
            full_name="grafeas.v1.DeploymentNote.resource_uri",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
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
    serialized_start=90,
    serialized_end=128,
)


_DEPLOYMENTOCCURRENCE = _descriptor.Descriptor(
    name="DeploymentOccurrence",
    full_name="grafeas.v1.DeploymentOccurrence",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="user_email",
            full_name="grafeas.v1.DeploymentOccurrence.user_email",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="deploy_time",
            full_name="grafeas.v1.DeploymentOccurrence.deploy_time",
            index=1,
            number=2,
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
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="undeploy_time",
            full_name="grafeas.v1.DeploymentOccurrence.undeploy_time",
            index=2,
            number=3,
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
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="config",
            full_name="grafeas.v1.DeploymentOccurrence.config",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="grafeas.v1.DeploymentOccurrence.address",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="resource_uri",
            full_name="grafeas.v1.DeploymentOccurrence.resource_uri",
            index=5,
            number=6,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="platform",
            full_name="grafeas.v1.DeploymentOccurrence.platform",
            index=6,
            number=7,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[
        _DEPLOYMENTOCCURRENCE_PLATFORM,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=131,
    serialized_end=458,
)

_DEPLOYMENTOCCURRENCE.fields_by_name[
    "deploy_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_DEPLOYMENTOCCURRENCE.fields_by_name[
    "undeploy_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_DEPLOYMENTOCCURRENCE.fields_by_name[
    "platform"
].enum_type = _DEPLOYMENTOCCURRENCE_PLATFORM
_DEPLOYMENTOCCURRENCE_PLATFORM.containing_type = _DEPLOYMENTOCCURRENCE
DESCRIPTOR.message_types_by_name["DeploymentNote"] = _DEPLOYMENTNOTE
DESCRIPTOR.message_types_by_name["DeploymentOccurrence"] = _DEPLOYMENTOCCURRENCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DeploymentNote = _reflection.GeneratedProtocolMessageType(
    "DeploymentNote",
    (_message.Message,),
    {
        "DESCRIPTOR": _DEPLOYMENTNOTE,
        "__module__": "grafeas.grafeas_v1.proto.deployment_pb2",
        "__doc__": """An artifact that can be deployed in some runtime.
  
  Attributes:
      resource_uri:
          Required. Resource URI for the artifact being deployed.
  """,
        # @@protoc_insertion_point(class_scope:grafeas.v1.DeploymentNote)
    },
)
_sym_db.RegisterMessage(DeploymentNote)

DeploymentOccurrence = _reflection.GeneratedProtocolMessageType(
    "DeploymentOccurrence",
    (_message.Message,),
    {
        "DESCRIPTOR": _DEPLOYMENTOCCURRENCE,
        "__module__": "grafeas.grafeas_v1.proto.deployment_pb2",
        "__doc__": """The period during which some deployable was active in a runtime.
  
  Attributes:
      user_email:
          Identity of the user that triggered this deployment.
      deploy_time:
          Required. Beginning of the lifetime of this deployment.
      undeploy_time:
          End of the lifetime of this deployment.
      config:
          Configuration used to create this deployment.
      address:
          Address of the runtime element hosting this deployment.
      resource_uri:
          Output only. Resource URI for the artifact being deployed
          taken from the deployable field with the same name.
      platform:
          Platform hosting this deployment.
  """,
        # @@protoc_insertion_point(class_scope:grafeas.v1.DeploymentOccurrence)
    },
)
_sym_db.RegisterMessage(DeploymentOccurrence)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
