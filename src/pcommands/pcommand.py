from abc import ABC, abstractmethod


class PCommand(ABC):
    @abstractmethod
    def run(self, context, input):
        pass

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_info() -> str:
        pass

    @staticmethod
    def get_role() -> None:
        return None
