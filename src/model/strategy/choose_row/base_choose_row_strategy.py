import abc


class BaseChooseRowStrategy(abc.ABC):
    @abc.abstractmethod
    def choose_row(self) -> int:
        pass
