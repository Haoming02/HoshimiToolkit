# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: octodb.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="octodb.proto",
    package="",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x0coctodb.proto"}\n\x08\x44\x61tabase\x12\x10\n\x08revision\x18\x01 \x01(\x05\x12\x1e\n\x0f\x61ssetBundleList\x18\x02 \x03(\x0b\x32\x05.Data\x12\x0f\n\x07tagname\x18\x03 \x03(\t\x12\x1b\n\x0cresourceList\x18\x04 \x03(\x0b\x32\x05.Data\x12\x11\n\turlFormat\x18\x05 \x01(\t"\xad\x02\n\x04\x44\x61ta\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08\x66ilepath\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04size\x18\x04 \x01(\x05\x12\x0b\n\x03\x63rc\x18\x05 \x01(\r\x12\x10\n\x08priority\x18\x06 \x01(\x05\x12\r\n\x05tagid\x18\x07 \x03(\x05\x12\x13\n\x0b\x64\x65pendencie\x18\x08 \x03(\x05\x12\x1a\n\x05state\x18\t \x01(\x0e\x32\x0b.Data.State\x12\x0b\n\x03md5\x18\n \x01(\t\x12\x12\n\nobjectName\x18\x0b \x01(\t\x12\x12\n\ngeneration\x18\x0c \x01(\x04\x12\x17\n\x0fuploadVersionId\x18\r \x01(\x05">\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x41\x44\x44\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\n\n\x06LATEST\x10\x03\x12\n\n\x06\x44\x45LETE\x10\x04\x62\x06proto3',
)


_DATA_STATE = _descriptor.EnumDescriptor(
    name="State",
    full_name="Data.State",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="NONE",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="ADD",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="UPDATE",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="LATEST",
            index=3,
            number=3,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="DELETE",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=383,
    serialized_end=445,
)
_sym_db.RegisterEnumDescriptor(_DATA_STATE)


_DATABASE = _descriptor.Descriptor(
    name="Database",
    full_name="Database",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="revision",
            full_name="Database.revision",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
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
        _descriptor.FieldDescriptor(
            name="assetBundleList",
            full_name="Database.assetBundleList",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
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
            name="tagname",
            full_name="Database.tagname",
            index=2,
            number=3,
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
            name="resourceList",
            full_name="Database.resourceList",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
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
            name="urlFormat",
            full_name="Database.urlFormat",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=16,
    serialized_end=141,
)


_DATA = _descriptor.Descriptor(
    name="Data",
    full_name="Data",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="Data.id",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
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
        _descriptor.FieldDescriptor(
            name="filepath",
            full_name="Data.filepath",
            index=1,
            number=2,
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
            name="name",
            full_name="Data.name",
            index=2,
            number=3,
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
            name="size",
            full_name="Data.size",
            index=3,
            number=4,
            type=5,
            cpp_type=1,
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
        _descriptor.FieldDescriptor(
            name="crc",
            full_name="Data.crc",
            index=4,
            number=5,
            type=13,
            cpp_type=3,
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
        _descriptor.FieldDescriptor(
            name="priority",
            full_name="Data.priority",
            index=5,
            number=6,
            type=5,
            cpp_type=1,
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
        _descriptor.FieldDescriptor(
            name="tagid",
            full_name="Data.tagid",
            index=6,
            number=7,
            type=5,
            cpp_type=1,
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
            name="dependencie",
            full_name="Data.dependencie",
            index=7,
            number=8,
            type=5,
            cpp_type=1,
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
            name="state",
            full_name="Data.state",
            index=8,
            number=9,
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
        _descriptor.FieldDescriptor(
            name="md5",
            full_name="Data.md5",
            index=9,
            number=10,
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
            name="objectName",
            full_name="Data.objectName",
            index=10,
            number=11,
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
            name="generation",
            full_name="Data.generation",
            index=11,
            number=12,
            type=4,
            cpp_type=4,
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
        _descriptor.FieldDescriptor(
            name="uploadVersionId",
            full_name="Data.uploadVersionId",
            index=12,
            number=13,
            type=5,
            cpp_type=1,
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
        _DATA_STATE,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=144,
    serialized_end=445,
)

_DATABASE.fields_by_name["assetBundleList"].message_type = _DATA
_DATABASE.fields_by_name["resourceList"].message_type = _DATA
_DATA.fields_by_name["state"].enum_type = _DATA_STATE
_DATA_STATE.containing_type = _DATA
DESCRIPTOR.message_types_by_name["Database"] = _DATABASE
DESCRIPTOR.message_types_by_name["Data"] = _DATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Database = _reflection.GeneratedProtocolMessageType(
    "Database",
    (_message.Message,),
    {
        "DESCRIPTOR": _DATABASE,
        "__module__": "octodb_pb2",
        # @@protoc_insertion_point(class_scope:Database)
    },
)
_sym_db.RegisterMessage(Database)

Data = _reflection.GeneratedProtocolMessageType(
    "Data",
    (_message.Message,),
    {
        "DESCRIPTOR": _DATA,
        "__module__": "octodb_pb2",
        # @@protoc_insertion_point(class_scope:Data)
    },
)
_sym_db.RegisterMessage(Data)


# @@protoc_insertion_point(module_scope)
