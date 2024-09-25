import numpy as np
import pandas as pd
from openTSNE import TSNE as OpenTSNE
from openTSNE import initialization
import umap
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def perform_tsne(data, n_components=2, perplexity=30, n_iter=250, random_state=42,metric="euclidean"):
    init = initialization.pca(data, n_components=n_components)

    metric = 'euclidean' if metric == 'correlation' else metric

    tsne = OpenTSNE(
        n_components=n_components,
        perplexity=perplexity,
        initialization=init,
        metric='euclidean',
        n_jobs=-1,
        neighbors="annoy",
        negative_gradient_method="fft",
        n_iter=n_iter,
        early_exaggeration_iter=50,
        random_state=random_state
    )
    return tsne.fit(data)


# New UMAP function
def perform_umap(data, n_components=2, n_neighbors=15, min_dist=0.1, random_state=42,metric="euclidean"):
    reducer = umap.UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metric,
        random_state=random_state
    )
    return reducer.fit_transform(data)

# Add other utility functions from the original code


def prepare_market_cap_data(market_caps, min_size=1, max_size=12035):
    median_market_cap = market_caps.median()
    market_caps_filled = market_caps.fillna(median_market_cap)
    min_positive = max(market_caps_filled.min(), 1e-6)
    market_caps_filled = np.maximum(market_caps_filled, min_positive)
    log_market_caps = np.log1p(market_caps_filled)

    scaler = RobustScaler()
    scaled_market_caps = scaler.fit_transform(log_market_caps.values.reshape(-1, 1)).flatten()

    marker_sizes = min_size + (max_size - min_size) * (scaled_market_caps - scaled_market_caps.min()) / (scaled_market_caps.max() - scaled_market_caps.min())

    return market_caps_filled, marker_sizes


def format_market_cap(value):
    if pd.isna(value):
        return "Not Available"
    try:
        return f"${float(value):,.0f} million"
    except ValueError:
        return str(value)


def determine_representatives(df, cluster_column, market_cap_column, coordinate_columns):
    market_cap_representatives = df.groupby(cluster_column).apply(
        lambda x: x.loc[x[market_cap_column].idxmax(), 'Ticker'] if x[market_cap_column].notna().any() else pd.NA
    ).to_dict()

    centroids = df.groupby(cluster_column)[coordinate_columns].mean()
    centroid_representatives = {}

    for cluster in centroids.index:
        if pd.isna(market_cap_representatives.get(cluster)):
            cluster_data = df[df[cluster_column] == cluster]
            distances = np.sqrt(
                sum((cluster_data[col] - centroids.loc[cluster, col]) ** 2 for col in coordinate_columns)
            )
            centroid_representatives[cluster] = cluster_data.loc[distances.idxmin(), 'Ticker']

    return {**market_cap_representatives, **centroid_representatives}
