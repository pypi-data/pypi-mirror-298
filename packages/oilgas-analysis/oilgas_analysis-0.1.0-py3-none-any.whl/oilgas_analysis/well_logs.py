import numpy as np
import pandas as pd
from scipy.stats import mode

def load_well_log_data(file_path):
    """
    Load well log data from CSV or Excel file.
    
    Parameters:
    file_path (str): Path to the input file (CSV or Excel)
    
    Returns:
    pd.DataFrame: Well log data
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or Excel.")

def analyze_well_log(log_data):
    """
    Analyze well log data.
    
    Parameters:
    log_data (pd.DataFrame): Well log data with depth and various log curves.
    
    Returns:
    dict: Analysis results including porosity, permeability, lithology, and net pay.
    """
    # Calculate average porosity
    porosity = np.mean(log_data['NPHI'])
    
    # Estimate permeability using a more complex relationship
    k_coeff = 0.136 * (1000 * porosity)**4.4 / (1 - porosity)**2
    permeability = k_coeff * (log_data['NPHI'] / log_data['SW'])**2
    avg_permeability = np.mean(permeability)
    
    # Determine lithology
    gr_cutoff = 65  # Shale cutoff
    lithology = np.where(log_data['GR'] < gr_cutoff, 'sandstone', 'shale')
    unique_lithology, counts = np.unique(lithology, return_counts=True)
    dominant_lithology = unique_lithology[np.argmax(counts)]
    
    # Calculate net pay
    payzone_cutoff = 0.1  # Example cutoff for pay zone
    net_pay = np.sum((log_data['NPHI'] > payzone_cutoff) & (log_data['GR'] < gr_cutoff)) * log_data['DEPTH'].diff().mean()
    
    return {
        'average_porosity': porosity,
        'estimated_permeability': avg_permeability,
        'dominant_lithology': dominant_lithology,
        'net_pay': net_pay,
        'porosity_profile': log_data['NPHI'].tolist(),
        'permeability_profile': permeability.tolist(),
        'lithology_profile': lithology.tolist()
    }
