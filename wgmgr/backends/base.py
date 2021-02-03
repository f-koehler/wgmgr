from abc import ABC, abstractmethod
from pathlib import Path

from wgmgr.config import Config


class Backend(ABC):
    @abstractmethod
    def load(self) -> Config:
        pass

    @abstractmethod
    def save(self, config: Config):
        pass