from typing import Optional

from tqdm import tqdm
import torch


def set_device(dev: Optional[str] = None):
    if dev is not None:
        return torch.device(dev)
    return torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")


def batch_embed(embedder, *args, dev=None, batch_size=256, **kwargs):
    embeddings = []
    for i in tqdm(range(0, len(embedder.text), batch_size), leave=False):
        batch = embedder.text[i:i+batch_size]
        embeddings.append(embedder.embed(batch, *args, **kwargs))

    # if isinstance(embeddings[0], torch.Tensor):
    # TODO MARCHE PAS POUR CPU pur l'instant (ah bon why?)
    embeddings = torch.cat(embeddings, dim=0)
    return embeddings