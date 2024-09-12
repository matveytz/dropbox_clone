from abc import ABC, abstractmethod
from typing import Dict, Callable, Any


class WebhookHandler(ABC):

    method_handle_mapping: Dict[Any, Callable]

    def webhook_handler_template(self, webhook_data):
        key = self.get_mapping_key(webhook_data)
        if key is None:
            return self.default_handler(webhook_data)
        try:
            return self.method_handle_mapping[key](self, webhook_data)
        except KeyError:
            raise NotImplementedError

    @abstractmethod
    def get_mapping_key(self, webhook_data) -> Any | None:
        raise NotImplementedError

    def default_handler(self, webhook_data):
        """
        Переопределите этот метод для обработки вебхуков по умолчанию
        """
        pass
