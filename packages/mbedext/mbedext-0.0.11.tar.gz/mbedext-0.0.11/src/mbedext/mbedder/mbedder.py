from typing import Optional

from sentence_transformers import SentenceTransformer
from transformers import PreTrainedModel

from ..utils import set_device, batch_embed
from ..embedder import STEmbedder, HFEmbedder
from ..visualizer import Visualizer, SklearnReducer


class Mbedder:
    def __init__(self, text: list[str], dev: Optional[str] = None, tqdm_disable: Optional[bool] = False) -> None:
        self.text = text
        self.embeddings = None
        self.embeddings_red = None
        self.labels = None
        self.clusters = None
        self.dev = set_device(dev)
        self.tqdm_disable = tqdm_disable


    def embed(self, model, *args, **kwargs):
        if isinstance(model, SentenceTransformer):
            embedder = STEmbedder(model, self.text)
        elif isinstance(model, PreTrainedModel):
            embedder = HFEmbedder(model, self.text)
        else:
            raise NotImplementedError
        
        self.embeddings = batch_embed(embedder, *args, dev=self.dev, **kwargs) # TODO convert to method of Embedder


    def reduce(self, model, *args, **kwargs):
        if "sklearn" in str(type(model)):
            reducer = SklearnReducer(model)
        else:
            raise NotImplementedError
        
        self.embeddings_red = reducer.reduce(self.embeddings.cpu())
    

    def cluster(self, model, *args, reduced=False, **kwargs):
        if "sklearn" in str(type(model)):
            clusterer = SklearnClusterer(model)
        else:
            raise NotImplementedError
        
        if reduced:
            self.clusters = clusterer.cluster(self.embeddings_red.cpu())
        else:
            self.clusters = clusterer.cluster(self.embeddings.cpu())
    

    def show(self, *args, reduce_model=None, cluster_model=None, **kwargs):
        if reduce_model is not None:
            self.reduce(reduce_model)
        if cluster_model is not None:
            self.cluster(cluster_model)

        if (self.embeddings_red is None) and (self.embeddings.shape[1] > 2):
            raise ValueError("Your embeddings have a dimensionality higher than 2 and can't be displayed on a plot. Please choose a dimensionality reduction method before.")
        if (self.embeddings_red.shape[1] > 2):
            raise ValueError("Your reduced embeddings have a dimensionality higher than 2 and can't be displayed on a plot. Please choose another dimensionality reduction method.")

        labels = self.clusters if self.clusters is not None else self.labels
        if self.embeddings_red is not None:
            visualizer = Visualizer(self.embeddings_red, self.text, labels, *args, **kwargs)
        else:
            visualizer = Visualizer(self.embeddings, self.text, labels, *args, **kwargs)
        return visualizer.show()
    