import abc

class GenericDAO(abc.ABC):

    @abc.abstractmethod
    def find_by_id(self, id: str | int): pass

    @abc.abstractmethod
    def find_by_cond(self, cond: str): pass

    @abc.abstractmethod
    def find_by_data(self, data: dict): pass

    @abc.abstractmethod
    def create(self, data: dict) -> str: pass

    @abc.abstractmethod
    def create_with_batch(self, lst_data: list[dict]) -> str: pass

    @abc.abstractmethod
    def update(self, primary_key_value, data: dict, primary_key_name='id'): pass

    @abc.abstractmethod
    def delete(self, id: str): pass