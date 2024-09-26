from finalsa.common.models import (SqsReponse, SqsMessage)
from typing import Dict, List, Union, Optional
from uuid import uuid4
from datetime import datetime, timezone
from abc import ABC, abstractmethod
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


class SqsService(ABC):

    @staticmethod
    def default_correlation_id():
        return str(uuid4())

    @abstractmethod
    def receive_messages(
            self,
            queue_url: str,
            max_number_of_messages: int = 1,
            wait_time_seconds: int = 1
    ) -> List[SqsReponse]:
        pass

    def send_message(
            self,
            queue_url: str,
            data: Dict,
            topic: str = "default",
    ) -> None:
        message = self.__parse_to_message__(
            topic,
            data,
            get_correlation_id(),
        )
        self.send_raw_message(queue_url, message)

    def get_default_attrs(
        self,
    ) -> Dict:
        result = {
            'correlation_id': {'Type': 'String', 'Value': get_correlation_id()},
            'span_id': {'Type': 'String', 'Value': get_span_id()},
            'trace_id': {'Type': 'String', 'Value': get_trace_id()},
        }
        return result

    @abstractmethod
    def send_raw_message(
            self,
            queue_url: str,
            data: Union[Dict, str],
            attributes: Optional[Dict] = {}
    ) -> None:
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

    @abstractmethod
    def delete_message(self, queue_url: str, receipt_handle: str) -> None:
        pass

    @abstractmethod
    def get_queue_arn(self, queue_url: str) -> str:
        pass

    @abstractmethod
    def get_queue_attributes(self, queue_url: str, ) -> Dict:
        pass

    @abstractmethod
    def get_queue_url(self, queue_name: str) -> str:
        pass
