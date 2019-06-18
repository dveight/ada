# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ada.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ada.proto',
  package='ada',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\tada.proto\x12\x03\x61\x64\x61\x1a\x1cgoogle/protobuf/struct.proto\"5\n\x05Input\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x1a\n\x05range\x18\x02 \x01(\x0b\x32\x0b.ada.Frames\"6\n\x06Output\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x1a\n\x05range\x18\x02 \x01(\x0b\x32\x0b.ada.Frames\"\x1c\n\x08Template\x12\x10\n\x08location\x18\x01 \x01(\t\"#\n\x06Script\x12\x0b\n\x03\x64ir\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"$\n\x06\x46rames\x12\r\n\x05start\x18\x01 \x01(\x05\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x05\"\x8c\x03\n\x07\x43ontext\x12\x1a\n\x06inputs\x18\x01 \x03(\x0b\x32\n.ada.Input\x12\x1c\n\x07outputs\x18\x02 \x03(\x0b\x32\x0b.ada.Output\x12\x1f\n\x08template\x18\x03 \x01(\x0b\x32\r.ada.Template\x12\"\n\routput_script\x18\x04 \x01(\x0b\x32\x0b.ada.Script\x12(\n\x07\x61liases\x18\x64 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04host\x18\x06 \x01(\x0e\x32\x17.ada.Context.HostsTypes\x12\x0b\n\x03job\x18\x07 \x01(\t\x12\x0c\n\x04shot\x18\x08 \x01(\t\x12\x0e\n\x06\x66ormat\x18\t \x01(\t\x12\'\n\x12script_frame_range\x18\n \x01(\x0b\x32\x0b.ada.Frames\"]\n\nHostsTypes\x12\x08\n\x04NUKE\x10\x00\x12\x08\n\x04MAYA\x10\x01\x12\x0b\n\x07HOUDINI\x10\x02\x12\n\n\x06NATRON\x10\x03\x12\x0c\n\x08\x43LARISSE\x10\x04\x12\n\n\x06KATANA\x10\x05\x12\x08\n\x04MARI\x10\x06\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])



_CONTEXT_HOSTSTYPES = _descriptor.EnumDescriptor(
  name='HostsTypes',
  full_name='ada.Context.HostsTypes',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NUKE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MAYA', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOUDINI', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NATRON', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLARISSE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KATANA', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MARI', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=568,
  serialized_end=661,
)
_sym_db.RegisterEnumDescriptor(_CONTEXT_HOSTSTYPES)


_INPUT = _descriptor.Descriptor(
  name='Input',
  full_name='ada.Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='ada.Input.location', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='range', full_name='ada.Input.range', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=101,
)


_OUTPUT = _descriptor.Descriptor(
  name='Output',
  full_name='ada.Output',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='ada.Output.location', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='range', full_name='ada.Output.range', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=157,
)


_TEMPLATE = _descriptor.Descriptor(
  name='Template',
  full_name='ada.Template',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='ada.Template.location', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=187,
)


_SCRIPT = _descriptor.Descriptor(
  name='Script',
  full_name='ada.Script',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dir', full_name='ada.Script.dir', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='ada.Script.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=224,
)


_FRAMES = _descriptor.Descriptor(
  name='Frames',
  full_name='ada.Frames',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='ada.Frames.start', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='ada.Frames.end', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=226,
  serialized_end=262,
)


_CONTEXT = _descriptor.Descriptor(
  name='Context',
  full_name='ada.Context',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='inputs', full_name='ada.Context.inputs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outputs', full_name='ada.Context.outputs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='template', full_name='ada.Context.template', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_script', full_name='ada.Context.output_script', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aliases', full_name='ada.Context.aliases', index=4,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='ada.Context.host', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='job', full_name='ada.Context.job', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shot', full_name='ada.Context.shot', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='format', full_name='ada.Context.format', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='script_frame_range', full_name='ada.Context.script_frame_range', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONTEXT_HOSTSTYPES,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=265,
  serialized_end=661,
)

_INPUT.fields_by_name['range'].message_type = _FRAMES
_OUTPUT.fields_by_name['range'].message_type = _FRAMES
_CONTEXT.fields_by_name['inputs'].message_type = _INPUT
_CONTEXT.fields_by_name['outputs'].message_type = _OUTPUT
_CONTEXT.fields_by_name['template'].message_type = _TEMPLATE
_CONTEXT.fields_by_name['output_script'].message_type = _SCRIPT
_CONTEXT.fields_by_name['aliases'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_CONTEXT.fields_by_name['host'].enum_type = _CONTEXT_HOSTSTYPES
_CONTEXT.fields_by_name['script_frame_range'].message_type = _FRAMES
_CONTEXT_HOSTSTYPES.containing_type = _CONTEXT
DESCRIPTOR.message_types_by_name['Input'] = _INPUT
DESCRIPTOR.message_types_by_name['Output'] = _OUTPUT
DESCRIPTOR.message_types_by_name['Template'] = _TEMPLATE
DESCRIPTOR.message_types_by_name['Script'] = _SCRIPT
DESCRIPTOR.message_types_by_name['Frames'] = _FRAMES
DESCRIPTOR.message_types_by_name['Context'] = _CONTEXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), dict(
  DESCRIPTOR = _INPUT,
  __module__ = 'ada_pb2'
  # @@protoc_insertion_point(class_scope:ada.Input)
  ))
_sym_db.RegisterMessage(Input)

Output = _reflection.GeneratedProtocolMessageType('Output', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUT,
  __module__ = 'ada_pb2'
  # @@protoc_insertion_point(class_scope:ada.Output)
  ))
_sym_db.RegisterMessage(Output)

Template = _reflection.GeneratedProtocolMessageType('Template', (_message.Message,), dict(
  DESCRIPTOR = _TEMPLATE,
  __module__ = 'ada_pb2'
  # @@protoc_insertion_point(class_scope:ada.Template)
  ))
_sym_db.RegisterMessage(Template)

Script = _reflection.GeneratedProtocolMessageType('Script', (_message.Message,), dict(
  DESCRIPTOR = _SCRIPT,
  __module__ = 'ada_pb2'
  # @@protoc_insertion_point(class_scope:ada.Script)
  ))
_sym_db.RegisterMessage(Script)

Frames = _reflection.GeneratedProtocolMessageType('Frames', (_message.Message,), dict(
  DESCRIPTOR = _FRAMES,
  __module__ = 'ada_pb2'
  # @@protoc_insertion_point(class_scope:ada.Frames)
  ))
_sym_db.RegisterMessage(Frames)

Context = _reflection.GeneratedProtocolMessageType('Context', (_message.Message,), dict(
  DESCRIPTOR = _CONTEXT,
  __module__ = 'ada_pb2'
  # @@protoc_insertion_point(class_scope:ada.Context)
  ))
_sym_db.RegisterMessage(Context)


# @@protoc_insertion_point(module_scope)
