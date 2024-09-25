
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, SpectralClustering, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from .utils import perform_tsne, perform_umap
from scipy.stats import rankdata
from scipy.stats import rankdata, skew, kurtosis


def process_it_price(data_close_price, days):
    # Load and preprocess data
    recent_date = data_close_price.index.get_level_values('date').max() - pd.Timedelta(days=days)
    close_prices = data_close_price.loc[data_close_price.index.get_level_values('date') >= recent_date]
    
    df_unstack = close_prices.loc[close_prices.index.get_level_values('ticker').notna(), "closeadj"].unstack(level='ticker')
    returns = df_unstack.pct_change()
    returns = returns.bfill()
    valid_tickers = returns.columns[returns.notna().all()]
    returns_final = returns[valid_tickers].fillna(0)
    return returns_final, valid_tickers



def spearman_correlation(data):
    ranks = np.apply_along_axis(rankdata, 0, data)
    corr_matrix = np.corrcoef(ranks, rowvar=False)
    return corr_matrix

def process_spearman(data_close_price, n_clusters, days, dim_reduction_method='tsne', metric='euclidean'):
    df_final, valid_tickers = process_it_price(data_close_price, days)
   
    data_array = df_final.values
    tail_matrix = spearman_correlation(data_array)

    dissimilarity_matrix = -np.log(np.abs(tail_matrix) + np.finfo(float).eps)
    np.fill_diagonal(dissimilarity_matrix, 0)

    imputer = SimpleImputer(strategy='mean')
    dissimilarity_matrix_imputed = imputer.fit_transform(dissimilarity_matrix)
    dissimilarity_matrix_imputed = (dissimilarity_matrix_imputed + dissimilarity_matrix_imputed.T) / 2
    np.fill_diagonal(dissimilarity_matrix_imputed, 0)

    n_components = min(50, dissimilarity_matrix_imputed.shape[0] - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    reduced_data = svd.fit_transform(dissimilarity_matrix_imputed)

    kmeans = KMeans(n_clusters=min(n_clusters, len(valid_tickers)), random_state=42)
    clusters = kmeans.fit_predict(reduced_data)

    if dim_reduction_method == 'tsne':
        coords = perform_tsne(reduced_data, perplexity=min(50, reduced_data.shape[0] - 1), n_iter=250, metric=metric)
    elif dim_reduction_method == 'umap':
        coords = perform_umap(reduced_data, n_neighbors=min(50, reduced_data.shape[0] - 1), metric=metric)
    else:
        raise ValueError("dim_reduction_method must be either 'tsne' or 'umap'")

    df_clusters = pd.DataFrame({
        'Ticker': valid_tickers,
        'Cluster': clusters,
        'Dim1': coords[:, 0],
        'Dim2': coords[:, 1]
    })

    return df_clusters



def ultra_fast_correlation_and_clustering(returns, n_clusters):
    # Standardize the returns
    scaler = StandardScaler(with_mean=False)  # Faster without centering
    returns_standardized = scaler.fit_transform(returns)
    
    # Compute similarity matrix (using dot product as a fast approximation of correlation)
    similarity = returns_standardized.T @ returns_standardized
    
    # Perform dimensionality reduction
    n_components = min(100, returns.shape[1] - 1)  # Adjust this value as needed
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    reduced_data = svd.fit_transform(similarity)
    
    # Perform spectral clustering on reduced data
    clustering = SpectralClustering(n_clusters=min(n_clusters, returns.shape[1]), 
                                    random_state=42, 
                                    n_jobs=-1,
                                    affinity='nearest_neighbors')  # Using nearest_neighbors for speed
    cluster_labels = clustering.fit_predict(reduced_data)
    
    return similarity, cluster_labels


def process_hierarchical(data_close_price, n_clusters, days, dim_reduction_method='tsne', metric='euclidean'):
    returns, valid_tickers = process_it_price(data_close_price, days)
    
    # Perform correlation and clustering
    corr, cluster_labels = ultra_fast_correlation_and_clustering(returns, n_clusters)
    
    # Dimensionality reduction
    n_components = min(50, corr.shape[0] - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    reduced_data = svd.fit_transform(corr)

    if dim_reduction_method == 'tsne':
        coords = perform_tsne(reduced_data, perplexity=min(50, reduced_data.shape[0] - 1), n_iter=250, metric=metric)
    elif dim_reduction_method == 'umap':
        coords = perform_umap(reduced_data, n_neighbors=min(50, reduced_data.shape[0] - 1), metric=metric)
    else:
        raise ValueError("dim_reduction_method must be either 'tsne' or 'umap'")

    result_df = pd.DataFrame({
        'Ticker': valid_tickers,
        'Cluster': cluster_labels,
        'Dim1': coords[:, 0],
        'Dim2': coords[:, 1]
    })

    return result_df

def fast_features(returns):
    if len(returns) == 0:
        return np.array([np.nan] * 5)  # Return NaNs if returns is empty
    cumsum_returns = np.cumsum(returns)
    return np.array([
        np.mean(returns),
        np.std(returns),
        skew(returns),
        kurtosis(returns),
        np.min(cumsum_returns - np.maximum.accumulate(cumsum_returns))
    ])



def fast_robust_clustering(data_close_price, n_clusters=120, days=90, batch_size=1000, dim_reduction_method='tsne', metric='euclidean'):
    returns_final, valid_tickers = process_it_price(data_close_price, days)

    print(f"Number of valid tickers: {len(valid_tickers)}")
    
    if len(valid_tickers) == 0:
        raise ValueError("No valid tickers found after preprocessing.")

    # Extract features
    features = np.array([fast_features(returns_final[ticker].values) for ticker in valid_tickers])
    
    print(f"Shape of features array: {features.shape}")

    # Ensure features is 2D
    if features.ndim == 1:
        features = features.reshape(1, -1)

    # Handle potential infinite values and impute NaN values
    features = np.where(np.isfinite(features), features, np.nan)
    imputer = SimpleImputer(strategy='mean')
    features_imputed = imputer.fit_transform(features)

    # Normalize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_imputed)

    # Apply MiniBatchKMeans for fast, robust clustering
    n_clusters = min(n_clusters, len(valid_tickers))  # Ensure n_clusters is not greater than number of samples
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=min(batch_size, len(valid_tickers)))
    clusters = kmeans.fit_predict(features_scaled)

    if dim_reduction_method == 'tsne':
        coords = perform_tsne(features_scaled, perplexity=min(50, features_scaled.shape[0] - 1), n_iter=250, metric=metric)
    elif dim_reduction_method == 'umap':
        coords = perform_umap(features_scaled, n_neighbors=min(50, features_scaled.shape[0] - 1), metric=metric)
    else:
        raise ValueError("dim_reduction_method must be either 'tsne' or 'umap'")

    # Create result DataFrame
    result_df = pd.DataFrame({
        'Ticker': valid_tickers,
        'Cluster': clusters,
        'Dim1': coords[:, 0],
        'Dim2': coords[:, 1]
    })

    return result_df