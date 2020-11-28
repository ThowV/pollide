from abc import ABC, abstractmethod


class PCommand(ABC):
    @abstractmethod
    def run(self, context, input):
        pass

    @staticmethod
    def get_role() -> None:
        return None
