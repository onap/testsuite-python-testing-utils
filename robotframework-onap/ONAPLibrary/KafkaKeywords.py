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
from pykafka import KafkaClient
from pykafka.common import OffsetType
from robot.api.deco import keyword
from robot import utils


class KafkaKeywords:
    """ Utilities useful for Kafka consuming and producing """

    def __init__(self):
        self._cache = utils.ConnectionCache('No Kafka Environments created')

    @keyword
    def connect(self, alias, kafka_host, kafka_version="1.0.0"):
        """connect to the specified kafka server"""
        client = KafkaClient(hosts=kafka_host, broker_version=kafka_version)
        self._cache.register(client, alias=alias)

    @keyword
    def produce(self, alias, topic, key, value):
        assert topic
        assert value

        producer = self._get_producer(alias, topic)
        return producer.produce(value, key)

    def _get_producer(self, alias, topic_name):
        topic = self._cache.switch(alias).topics[topic_name]
        prod = topic.get_sync_producer()
        return prod

    @keyword
    def consume(self, alias, topic_name, consumer_group=None):
        assert topic_name

        consumer = self._get_consumer(alias, topic_name, consumer_group)
        msg = consumer.consume()
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

        topic = self._cache.switch(alias).topics[topic_name]

        offset_type = OffsetType.LATEST
        if set_offset_to_earliest:
            offset_type = OffsetType.EARLIEST

        c = topic.get_simple_consumer(
                consumer_group=cgn, auto_offset_reset=offset_type, auto_commit_enable=True,
                reset_offset_on_start=True, consumer_timeout_ms=5000)

        return c
