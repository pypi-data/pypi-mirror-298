import gc
from abc import ABC, abstractmethod
from typing import Optional

import torch


class Embedder(ABC):
    def __init__(self, model, text, dev = None) -> None:
        self.model = model
        self.text = text
        self.dev = self.set_device(dev)

    @abstractmethod
    def embed(self, batch):
        raise NotImplementedError

    @staticmethod
    def set_device(dev: Optional[str] = None):
        if dev is not None:
            return torch.device(dev)
        if torch.backends.mps.is_available():
            return torch.device("mps")
        elif torch.cuda.is_available():
            return torch.device("cuda")
        else:
            return torch.device("cpu")

    def empty_cache(self):
        gc.collect()
        if self.dev.type == "cuda":
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        elif self.dev.type == "mps":
            torch.mps.empty_cache()
        