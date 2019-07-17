# Copyright 2019 AT&T Intellectual Property. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# noinspection PyPackageRequirements
from google.protobuf import descriptor
# noinspection PyPackageRequirements
from google.protobuf import descriptor_pb2
# noinspection PyPackageRequirements
from google.protobuf import message_factory
# noinspection PyPackageRequirements
from google.protobuf.json_format import MessageToJson


class VESProtobuf(object):
    """ non keywords methods related to VES """

    def __init__(self):
        super(VESProtobuf, self).__init__()
        self.message_descriptors = VESProtobuf.get_message_definitions()

    @staticmethod
    def create_ves_event():
        file_descriptor_proto = descriptor_pb2.FileDescriptorProto()
        file_descriptor_proto.name = 'VesEvent'
        VESProtobuf.create_commoneventheader(file_descriptor_proto)
        VESProtobuf.create_vesevent(file_descriptor_proto)
        return file_descriptor_proto

    @staticmethod
    def create_vesevent(file_descriptor_proto):
        message_type = file_descriptor_proto.message_type.add()
        message_type.name = "VesEvent"
        VESProtobuf.create_message_field(message_type, 1, "commonEventHeader", "CommonEventHeader")
        VESProtobuf.create_field(message_type, 2, "eventFields", descriptor.FieldDescriptor.TYPE_BYTES)
        return message_type

    @staticmethod
    def create_commoneventheader(file_descriptor_proto):
        message_type = file_descriptor_proto.message_type.add()
        message_type.name = "CommonEventHeader"
        enum_type = VESProtobuf.create_enum_type(message_type, 'Priority')
        VESProtobuf.create_enum_type_value(enum_type, ["PRIORITY_NOT_PROVIDED", "HIGH", "MEDIUM", "NORMAL", "LOW"])
        VESProtobuf.create_field(message_type, 1, "version", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 2, "domain", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 3, "sequence", descriptor.FieldDescriptor.TYPE_UINT32)
        VESProtobuf.create_enum_field(message_type, 4, "priority", "Priority")
        VESProtobuf.create_field(message_type, 5, "eventId", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 6, "eventName", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 7, "eventType", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 8, "lastEpochMicrosec", descriptor.FieldDescriptor.TYPE_UINT64)
        VESProtobuf.create_field(message_type, 9, "startEpochMicrosec", descriptor.FieldDescriptor.TYPE_UINT64)
        VESProtobuf.create_field(message_type, 10, "nfNamingCode", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 11, "nfcNamingCode", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 12, "nfVendorName", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 13, "reportingEntityId", descriptor.FieldDescriptor.TYPE_BYTES)
        VESProtobuf.create_field(message_type, 14, "reportingEntityName", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 15, "sourceId", descriptor.FieldDescriptor.TYPE_BYTES)
        VESProtobuf.create_field(message_type, 16, "sourceName", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 17, "timeZoneOffset", descriptor.FieldDescriptor.TYPE_STRING)
        VESProtobuf.create_field(message_type, 18, "vesEventListenerVersion",
                                 descriptor.FieldDescriptor.TYPE_STRING)
        return message_type

    @staticmethod
    def create_enum_type(desc_proto, name):
        enum_type = desc_proto.enum_type.add()
        enum_type.name = name
        return enum_type

    @staticmethod
    def create_enum_type_value(enum_type, value_list):
        for i in range(len(value_list)):
            enum_type_val = enum_type.value.add()
            enum_type_val.name = value_list[i]
            enum_type_val.number = i

    @staticmethod
    def create_field(desc_proto, number, name, field_type):
        field = desc_proto.field.add()
        field.number = number
        field.name = name
        field.type = field_type

    @staticmethod
    def create_enum_field(desc_proto, number, name, type_name):
        field = desc_proto.field.add()
        field.number = number
        field.name = name
        field.type = descriptor.FieldDescriptor.TYPE_ENUM
        field.type_name = type_name

    @staticmethod
    def create_message_field(desc_proto, number, name, type_name):
        field = desc_proto.field.add()
        field.number = number
        field.name = name
        field.type = descriptor.FieldDescriptor.TYPE_MESSAGE
        field.type_name = type_name

    @staticmethod
    def get_message_definitions():
        messages = message_factory.GetMessages((VESProtobuf.create_ves_event(),))
        message_factory._FACTORY = message_factory.MessageFactory()
        return messages

    def binary_to_json(self, binary_message):
        ves = self.message_descriptors['VesEvent']()
        ves.MergeFromString(binary_message)
        json = MessageToJson(ves)
        return json
