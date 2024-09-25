import pandas as pd
from .clustering import process_spearman, process_hierarchical, fast_robust_clustering

def process_data(data_close_price, method='fast_robust', n_clusters=120, days=90, dim_reduction_method='tsne', metric='euclidean'):
    if method == 'spearman_correlation':
        return process_spearman(data_close_price, n_clusters, days, dim_reduction_method, metric=metric)
    elif method == 'spectral_method':
        return process_hierarchical(data_close_price, n_clusters, days, dim_reduction_method, metric=metric)
    elif method == 'moment_based':
        return fast_robust_clustering(data_close_price, n_clusters, days, dim_reduction_method=dim_reduction_method, metric=metric)
    else:
        raise ValueError("Method must be either 'spearman_correlation', 'spectral_method', or 'moment_based'")

