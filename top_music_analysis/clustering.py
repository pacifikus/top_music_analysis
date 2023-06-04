import pickle

import click
import pandas as pd
from pyclustertend import hopkins
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import top_music_analysis.config as config


def check_clustering_tendency(data):
    return hopkins(data, data.shape[0])


def silhouette(data, max_k):
    silhouette_values = []
    feature_cols = data.drop(["name", "artist"], axis=1).columns

    for k in range(2, max_k):
        kmeans = KMeans(
            n_clusters=k,
            random_state=config.SEED,
        ).fit(data[feature_cols])
        silhouette_value = silhouette_score(data[feature_cols], kmeans.labels_)
        silhouette_values.append(silhouette_value)
    max_metric_value = max(silhouette_values)
    return silhouette_values.index(max_metric_value) + 1


def get_labels(data, k):
    feature_cols = data.drop(["name", "artist"], axis=1).columns
    kmeans = KMeans(
        n_clusters=k,
        random_state=config.SEED,
    ).fit(data[feature_cols])
    with open("../models/k_means.pkl", "wb") as f:
        pickle.dump(kmeans, f)
    return kmeans.labels_


@click.command()
@click.option("--data", default="spotify_res.csv", help="Input data path")
@click.option("--out", default="clustering_res.csv", help="Output data path")
def start(data, out):
    df = pd.read_csv(data, index_col="Unnamed: 0")
    optimal_k = silhouette(df, 10)
    df["label"] = get_labels(df, optimal_k)
    df.to_csv(out)


if __name__ == "__main__":
    start()
