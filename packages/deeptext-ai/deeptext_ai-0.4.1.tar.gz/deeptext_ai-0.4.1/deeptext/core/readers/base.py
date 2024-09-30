from typing import List, Optional
from abc import ABC, abstractmethod

from deeptext.core.document import Document


class BaseReader(ABC):
    """An interface for readers."""

    @classmethod
    def class_name(cls) -> str:
        return "BaseReader"

    @abstractmethod
    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data."""

    def load(self) -> List[Document]:
        return self.load_data()

    def lazy_load(self) -> List[Document]:
        return self.load_data()
