from typing import Union, Optional

from .embedder import Embedder

class STEmbedder(Embedder):
    def __init__(self, model, text, *args, **kwargs) -> None:
        super().__init__(model, text)

    def embed(self, batch: Union[list[str], str], *args, batch_size: Optional[int] = 256, to_cpu: Optional[bool] = False, **kwargs):
        embeddings = self.model.encode(batch, batch_size=batch_size, convert_to_tensor=True)
        self.empty_cache()
        if to_cpu:
            return embeddings.cpu().numpy()
        else:
            return embeddings