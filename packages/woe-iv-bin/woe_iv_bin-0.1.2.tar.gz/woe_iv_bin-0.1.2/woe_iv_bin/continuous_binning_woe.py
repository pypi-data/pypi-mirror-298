import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def calculate_woe_iv(grouped):
    """
    Calculate Weight of Evidence (WoE) and Information Value (IV) for grouped data.
    """
    grouped['dist_good'] = grouped['n_good'] / grouped['n_good'].sum()
    grouped['dist_bad'] = grouped['n_bad'] / grouped['n_bad'].sum()
    grouped['WoE'] = np.log((grouped['dist_good'] + 0.0001) / (grouped['dist_bad'] + 0.0001))
    grouped['IV'] = (grouped['dist_good'] - grouped['dist_bad']) * grouped['WoE']
    
    return grouped

def continuous_binning(df, feature, target, max_bins=20, min_samples_bin=0.05):
    """
    Enhances binning for a continuous feature based on Information Value (IV),
    also returns optimized bins with their respective IV values.
    
    Parameters:
    - df (DataFrame): The input dataframe.
    - feature (str): The name of the continuous feature to bin.
    - target (str): The name of the target variable.
    - max_bins (int): Maximum number of bins to consider; defaults to 20.
    - min_samples_bin (float or int): Minimum fraction or absolute number of samples required per bin.
    
    Returns:
    - DataFrame: Updated DataFrame with an additional column for the binned feature.
    - List of tuples: List of optimized bin ranges.
    - DataFrame: DataFrame containing 'optimized_bin', 'optimized_IV', 'total_optimized_IV' for each bin.
    """
    if min_samples_bin > 1:
        min_samples_bin = min_samples_bin / df.shape[0]
    
    # Initial binning to get starting bins
    df['binned'], bins = pd.qcut(df[feature], q=max_bins, duplicates='drop', retbins=True, labels=False)
    best_iv = 0
    best_bins = bins  # Use the initial bins as the starting best_bins

    for bin_count in range(2, max_bins + 1):
        df['binned'], temp_bins = pd.qcut(df[feature], q=bin_count, duplicates='drop', retbins=True, labels=False)
        grouped = df.groupby('binned')[target].agg(['count', 'sum']).rename(columns={'count': 'n_obs', 'sum': 'n_good'})
        grouped['n_bad'] = grouped['n_obs'] - grouped['n_good']

        if (grouped['n_obs'] < df.shape[0] * min_samples_bin).any():
            continue

        grouped = calculate_woe_iv(grouped)
        iv = grouped['IV'].sum()

        if iv > best_iv:
            best_iv = iv
            best_bins = temp_bins
    
    # Check if best_bins was determined
    if best_bins is None:
        raise ValueError("Binning did not result in any valid bins with the given parameters.")

    # Recalculate grouped with the best bins to ensure WoE and IV are accurate
    df['binned'] = pd.cut(df[feature], bins=best_bins, labels=False, include_lowest=True)
    grouped = df.groupby('binned')[target].agg(['count', 'sum']).rename(columns={'count': 'n_obs', 'sum': 'n_good'})
    grouped['n_bad'] = grouped['n_obs'] - grouped['n_good']
    grouped = calculate_woe_iv(grouped)

    # Combine bins with the same WoE and IV
    combined_bins = []
    combined_bins.append(best_bins[0])
    combined_iv = []
    combined_woe = []
    
    previous_woe = grouped['WoE'].values[0]
    previous_iv = grouped['IV'].values[0]

    combined_iv.append(previous_iv)
    combined_woe.append(previous_woe)

    for i in range(1, len(best_bins) - 1):
        current_woe = grouped['WoE'].values[i]
        current_iv = grouped['IV'].values[i]
        if current_woe != previous_woe or current_iv != previous_iv:
            combined_bins.append(best_bins[i])
            combined_iv.append(current_iv)
            combined_woe.append(current_woe)
            previous_woe = current_woe
            previous_iv = current_iv
    
    combined_bins.append(best_bins[-1])
    
    # Apply the optimized binning configuration
    df['optimized_binned_feature'] = pd.cut(df[feature], bins=combined_bins, labels=range(len(combined_bins)-1), include_lowest=True)
    final_grouped = df.groupby('optimized_binned_feature')[target].agg(['count', 'sum']).rename(columns={'count': 'n_obs', 'sum': 'n_good'})
    final_grouped['n_bad'] = final_grouped['n_obs'] - final_grouped['n_good']
    final_grouped = calculate_woe_iv(final_grouped)
    final_iv = final_grouped['IV'].sum()

    # Prepare bin range list
    optimized_bins = [(f"({combined_bins[i]}, {combined_bins[i+1]}]" if i < len(combined_bins)-1 else f"({combined_bins[i]}, {combined_bins[i+1]}]") for i in range(len(combined_bins)-1)]

    # Prepare the final DataFrame to return
    final_df = pd.DataFrame({
        'optimized_bin': optimized_bins,
        'optimized_WoE': combined_woe,
        'optimized_IV': combined_iv
    })
    final_df['total_optimized_IV'] = final_iv

    return df, optimized_bins, final_df
