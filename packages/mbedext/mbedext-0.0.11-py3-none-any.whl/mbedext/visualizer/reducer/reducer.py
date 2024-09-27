class Reducer:
    def __init__(self, model) -> None:
        self.model = model
        self.embeddings_reduced = None

    def reduce(self):
        raise NotImplementedError