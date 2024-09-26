from finalsa.common.models import SqsMessage
from typing import Union, Dict, List, Optional
from datetime import datetime, timezone
from uuid import uuid4
from abc import ABC, abstractmethod
try:
    from orjson import dumps
    ORJSON = True
except ImportError:
    from json import dumps
    ORJSON = False
from finalsa.traceability import (
    get_correlation_id, get_trace_id, get_span_id
)


class SnsClient(ABC):

    @abstractmethod
    def create_topic(self, name: str):
        pass

    @abstractmethod
    def subscription_exists(self, topic_name: str, arn: str) -> bool:
        pass

    @abstractmethod
    def get_all_topics(self) -> List:
        pass

    @abstractmethod
    def get_or_create_topic(self, name: str):
        pass

    @abstractmethod
    def get_topic(self, topic_name: str):
        pass

    @abstractmethod
    def list_subscriptions(self, topic: str) -> List:
        pass

    @abstractmethod
    def subscribe(self, topic_name: str, protocol: str, endpoint: str) -> Dict:
        pass

    @abstractmethod
    def publish_message(
        self,
        topic_name: str,
        payload: Union[Dict, SqsMessage],
        correlation_id: Optional[Union[str, uuid4]] = None
    ) -> Dict:
        pass

    @abstractmethod
    def publish(
        self,
        topic_name: str,
        payload: Union[Dict, str],
        att_dict: Optional[Dict] = {}
    ) -> Dict:
        pass

    @staticmethod
    def __dump_payload__(payload: Union[Dict, SqsMessage]) -> str:
        body = None
        if isinstance(payload, dict):
            body = dumps(payload)
            if ORJSON:
                body = body.decode()
            return body
        body = payload.model_dump_json()
        return body

    @staticmethod
    def __parse_to_message__(
        topic_name: str,
        payload: Union[Dict, SqsMessage],
        correlation_id: str,
    ) -> Dict:
        if isinstance(payload, SqsMessage):
            return payload.model_dump()
        message = SqsMessage(
            id=str(uuid4()),
            topic=topic_name,
            payload=payload,
            correlation_id=correlation_id,
            timestamp=datetime.now(timezone.utc)
        )
        return message.model_dump()

    def get_default_attrs(
        self,
    ) -> Dict:
        result = {
            'correlation_id': get_correlation_id(),
            "span_id": get_span_id(),
            'trace_id': get_trace_id()
        }
        return result

    def publish_message(
        self,
        topic_name: str,
        payload: Union[Dict, SqsMessage],
    ) -> Dict:
        correlation_id = str(get_correlation_id())
        message_attrs = self.get_default_attrs()
        message = self.__parse_to_message__(topic_name, payload, correlation_id)
        return self.publish(topic_name, message, message_attrs)
