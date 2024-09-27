from typing import Union, Optional, Callable, Any

import torch
from transformers import AutoTokenizer

from .embedder import Embedder


class HFEmbedder(Embedder):
    def __init__(self, model, text, *args, **kwargs) -> None:
        super().__init__(model, text)
        self.model = self.model.to(self.dev)

    def embed(self, batch: Union[list[str], str], *args, pooling_method: Optional[Union[str, int, Callable[..., Any]]], 
              padding: bool = True, truncation: bool = True, max_length: Optional[int] = None, 
              to_cpu: Optional[bool] = False, **kwargs):
        tokenizer = AutoTokenizer.from_pretrained(self.model.name_or_path)
        tokenized_batch = tokenizer(batch, return_tensors='pt', padding=padding, 
                                   truncation=truncation, max_length=max_length).to(self.dev)
        
        with torch.no_grad():
            outputs = self.model(**tokenized_batch)
            if isinstance(pooling_method, int):
                embeddings = outputs.last_hidden_state[:, pooling_method, :]
            elif isinstance(pooling_method, str):
                if pooling_method == "mean":
                    embeddings = outputs.last_hidden_state.mean(dim=1)
            else:
                embeddings = pooling_method(outputs.last_hidden_state, tokenized_batch, *args, **kwargs)
        
        self.empty_cache()
        if to_cpu:
            return embeddings.cpu().numpy()
        else:
            return embeddings
