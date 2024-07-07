#!usr/bin/python3
from abc import ABC, abstractmethod

class IPersistenceManager(ABC):
    """
    Abstract interface for managing the persistence of entities.

    This class defines abstract methods that must be implemented by any class 
    wishing to handle data persistence to a data source, such as a database, 
    files, etc.
    """

    @abstractmethod
    def save(self, entity):
        pass

