import pandas as pd
import plotly.express as px


class Visualizer:
    def __init__(self, X, text, labels) -> None:
        self.X = X
        self.text = text
        self.labels = labels

    def show(self, *args, labels_map=None, title="Title", autosize=False, width=1400, 
             height=800, xaxis_title="dimension 1", yaxis_title="dimension 2", **kwargs):
        df = pd.DataFrame(self.X, columns=['dim1', 'dim2'])
        df["text"] = self.text

        kwargs_fig = {"x": "dim1", "y": "dim2", "hover_name": "text", "opacity": 0.7}

        if self.labels is not None:
            df["labels"] = self.labels.astype(str)
            if labels_map is not None:
                df["labels_map"] = df["labels"].map(labels_map).fillna(df["labels"])
                kwargs_fig["color"] = "label_map"
            else:
                kwargs_fig["color"] = "labels"
            kwargs_fig["color_discrete_sequence"] = px.colors.qualitative.Alphabet

        fig = px.scatter(df, *args, **kwargs_fig)
        fig.update_traces(marker=dict(line=dict(width=0.2,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))
        fig.update_layout(
            title=title,
            autosize=autosize,
            width=width,
            height=height,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            **kwargs
        )
        return fig