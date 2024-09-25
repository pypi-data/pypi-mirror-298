import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datamapplot
from .utils import prepare_market_cap_data, format_market_cap, determine_representatives
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def create_color_map(n_colors):
    colors = plt.cm.viridis(np.linspace(0, 1, n_colors))
    cmap = LinearSegmentedColormap.from_list('custom_viridis', colors, N=n_colors)
    color_dict = {i: plt.cm.colors.rgb2hex(cmap(i / (n_colors - 1))) for i in range(n_colors)}
    return color_dict

def get_color(cluster, cluster_colors):
    return cluster_colors.get(cluster, '#808080')  # Default to gray if cluster not found

def prepare_plot_data_price(df, df_ratios):
    plot_data = df.merge(df_ratios, left_on='Ticker', right_index=True, how='left')
    plot_data['market_cap_display'] = plot_data['market_cap'].apply(format_market_cap)
    plot_data['market_cap_note'] = plot_data['market_cap'].apply(
        lambda x: '' if pd.notna(x) else '(Market Cap not available)'
    )
    return plot_data



def scale_coordinates(plot_data, feature_range=(-20, 20)):
    scaler = MinMaxScaler(feature_range=feature_range)
    return scaler.fit_transform(np.array(plot_data[['Dim1', 'Dim2']]))

def prepare_display_labels(plot_data, representative_column):
    display_labels = np.array(plot_data['Ticker'])
    representative_mask = plot_data['Ticker'] == plot_data[representative_column]
    display_labels[~representative_mask] = ''
    return display_labels

def prepare_color_array(plot_data, cluster_column):
    n_clusters = len(plot_data[cluster_column].unique())
    cluster_colors = create_color_map(n_clusters)
    color_array = np.array([get_color(cluster, cluster_colors) for cluster in plot_data[cluster_column]])
    return [mcolors.to_rgb(color) for color in color_array]




def assign_colors_by_cluster(plot_data):
    # Get unique clusters
    unique_clusters = plot_data['Cluster'].unique()
    n_clusters = len(unique_clusters)

    # Create a colormap
    cmap = plt.get_cmap('viridis')

    # Assign a color to each cluster
    cluster_colors = {cluster: cmap(i / (n_clusters - 1))[:3] for i, cluster in enumerate(unique_clusters)}

    # Assign colors to each point based on its cluster
    colors = np.array([cluster_colors[cluster] for cluster in plot_data['Cluster']])

    return colors

def prepare_color_array(plot_data):
    colors = assign_colors_by_cluster(plot_data)

    # Calculate mean distance matrix for saturation adjustment
    tsne_coords = plot_data[['Dim1', 'Dim2']].values
    distances = pdist(tsne_coords)
    dist_matrix = squareform(distances)
    mean_distances = np.mean(dist_matrix, axis=1)

    # Normalize mean distances to [0, 1] range
    normalized_distances = (mean_distances - mean_distances.min()) / (mean_distances.max() - mean_distances.min())

    # Adjust color saturation based on mean distance
    saturation_factor = (0.5 + 0.5 * normalized_distances)[:, np.newaxis]
    adjusted_colors = colors * saturation_factor + (1 - saturation_factor)

    return adjusted_colors



def prepare_data_and_create_plot(df, df_ratios, method, feature_range=(-20, 20)):
    # Join with df_ratios to get market cap data
    df = df.merge(df_ratios, left_on='Ticker', right_on='ticker', how='left')

    # Prepare market cap data
    df['market_cap_filled'], marker_sizes = prepare_market_cap_data(df['market_cap'], min_size=5, max_size=1235)

    # Determine representatives
    representative_tickers = determine_representatives(df, 'Cluster', 'market_cap', ['Dim1', 'Dim2'])
    df['Representative'] = df['Cluster'].map(representative_tickers)

    # Print summary
    print(df.groupby('Cluster').first()[['Representative', 'market_cap']])
    market_cap_count = sum(1 for v in representative_tickers.values() if pd.notna(v))
    centroid_count = len(representative_tickers) - market_cap_count
    print(f"Representatives assigned by market cap: {market_cap_count}")
    print(f"Representatives assigned by centroid: {centroid_count}")

    plot_data = df.copy()

    # Scale the coordinates
    scaled_coords = scale_coordinates(plot_data, feature_range=feature_range)

    # Prepare the labels array for display
    display_labels = prepare_display_labels(plot_data, 'Representative')

    # Prepare color array
    rgb_colors = prepare_color_array(plot_data)

    # Print debug information
    n_clusters = len(plot_data['Cluster'].unique())
    print("Unique clusters:", n_clusters)
    print("Shape of rgb_colors:", rgb_colors.shape)

    # Convert market_cap_filled to numeric, replacing any non-numeric values with NaN
    plot_data['market_cap_filled'] = pd.to_numeric(plot_data['market_cap_filled'], errors='coerce')

    # Replace NaN values with a placeholder string
    plot_data['market_cap_display'] = plot_data['market_cap_filled'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "N/A")

    # Update the hover text template
    hover_text_html_template = """
    <div style="font-family: Arial, sans-serif; padding: 10px; background-color: rgba(0,0,0,0.9); color: white; border-radius: 5px; max-width: 300px;">
        <h2 style="margin: 0 0 10px 0; color: #4CAF50;">{Ticker}</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 3px; border-bottom: 1px solid #555;">Market Cap:</td>
                <td style="padding: 3px; border-bottom: 1px solid #555; text-align: right;">{market_cap_display}</td>
            </tr>
        </table>
        <p style="margin: 10px 0 0 0; font-size: 0.9em; color: #888;">Cluster: {Cluster}</p>
    </div>
    """

    # Create the plot
    plot = datamapplot.create_interactive_plot(
        scaled_coords,
        display_labels,
        font_family="Playfair Display SC",
        title=f"Cluster Visualization of Stocks ({method.capitalize()} method)",
        hover_text=plot_data['Ticker'],
        text_collision_size_scale=3,
        enable_search=True,
        darkmode=True,
        custom_css="""
        #title-container span {
            font-size: 24px !important;
        }
        """,
        initial_zoom_fraction=0.9,
        text_outline_width=100,
        on_click="window.open(`https://finance.yahoo.com/quote/${Ticker}`)",
        extra_point_data=plot_data,
        marker_size_array=marker_sizes,
        hover_text_html_template=hover_text_html_template,
        noise_label='',
        marker_color_array=rgb_colors
    )

    return plot