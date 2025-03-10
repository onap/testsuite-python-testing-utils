# Copyright 2019 AT&T Intellectual Property. All rights reserved.
# Copyright (C) 2022 Nordix Foundation
# Copyright (C) 2022 Nokia
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

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
import ssl
from robot.api.deco import keyword
from robot import utils
import logging

logging.getLogger("kafka").setLevel(logging.CRITICAL)


class KafkaKeywords(object):
    """ Utilities useful for Kafka consuming and producing """

    def __init__(self):
        super(KafkaKeywords, self).__init__()
        self._cache = utils.ConnectionCache('No Kafka Environments created')

    @keyword
    def connect(self, alias, kafka_host, sasl_user, sasl_password, sasl_mechanism="PLAIN"):
        """connect to the specified kafka server"""
        client = {
            "bootstrap_servers": kafka_host,
            "sasl_username": sasl_user,
            "sasl_password": sasl_password,
            "security_protocol": 'SASL_PLAINTEXT',
            "ssl_context": ssl.create_default_context(),
            "sasl_mechanism": sasl_mechanism
        }
        self._cache.register(client, alias=alias)

    @keyword
    def produce(self, alias, topic, key, value):
        assert topic
        assert value

        producer = self._get_producer(alias)
        return producer.send(topic, value=value, key=key)

    def _get_producer(self, alias):
        cache = self._cache.switch(alias)
        prod = KafkaProducer(bootstrap_servers=cache['bootstrap_servers'],
                             sasl_plain_username=cache['sasl_username'],
                             sasl_plain_password=cache['sasl_password'],
                             security_protocol=cache['security_protocol'],
                             ssl_context=cache['ssl_context'],
                             sasl_mechanism=cache['sasl_mechanism'],
                             request_timeout_ms=5000)
        return prod

    @keyword
    def consume(self, alias, topic_name, consumer_group=None):
        assert topic_name

        consumer = self._get_consumer(alias, topic_name, consumer_group)
        msg = next(consumer)
        consumer.close(autocommit=True)
        if msg is None:
            return None
        else:
            return msg.value

    def _get_consumer(self, alias, topic_name, consumer_group=None, set_offset_to_earliest=False):
        assert topic_name

        # default to the topic as group name
        if consumer_group:
            cgn = consumer_group
        else:
            cgn = topic_name

        cache = self._cache.switch(alias)

        consumer = KafkaConsumer(bootstrap_servers=cache['bootstrap_servers'],
                                 sasl_plain_username=cache['sasl_username'],
                                 sasl_plain_password=cache['sasl_password'],
                                 security_protocol=cache['security_protocol'],
                                 ssl_context=cache['ssl_context'],
                                 sasl_mechanism=cache['sasl_mechanism'],
                                 group_id=cgn,
                                 request_timeout_ms=10000,
                                 api_version=(3,0,0))

        consumer.topics()
        partition_set = consumer.partitions_for_topic(str(topic_name))
        partitions = []
        for val in partition_set:
            partitions.append(TopicPartition(str(topic_name), val))
        consumer.assign(partitions)
        last = consumer.end_offsets(partitions)
        offset = max(last.values())

        if set_offset_to_earliest:
            consumer.seek_to_beginning()
        else:
            for tp in partitions:
                consumer.seek(tp, offset - 1)
        return consumer
