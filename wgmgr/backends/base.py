from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from wgmgr.config import Config


class Backend(ABC):
    @staticmethod
    @abstractmethod
    def from_options(options: Dict[str, str]) -> Backend:
        pass

    @abstractmethod
    def load(self) -> Config:
        pass

    @abstractmethod
    def save(self, config: Config):
        pass
