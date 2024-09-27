from .reducer import Reducer


class SklearnReducer(Reducer):
    def __init__(self, model) -> None:
        super().__init__(model)

    def reduce(self, X):
        return self.model.fit_transform(X)