# oilgas_analysis/artificial_lift.py
import numpy as np

def select_artificial_lift_candidates(wells_data):
    """
    Select candidate wells for artificial lift.
    
    Parameters:
    wells_data (list of dict): List of dictionaries containing well data
    
    Returns:
    list: List of well names that are candidates for artificial lift
    """
    candidates = []
    
    for well in wells_data:
        if (well['production_rate'] < well['economic_limit'] and 
            well['reservoir_pressure'] > well['bottomhole_pressure'] * 1.5 and
            well['water_cut'] < 0.9):
            candidates.append(well['name'])
    
    return candidates

def analyze_lift_performance(initial_rate, time, lifted_rates, lift_type):
    """
    Analyze the performance of an artificial lift installation.
    
    Parameters:
    initial_rate (float): Production rate before lift installation
    time (array): Time points after lift installation
    lifted_rates (array): Production rates after lift installation
    lift_type (str): Type of artificial lift (e.g., 'ESP', 'Gas Lift')
    
    Returns:
    dict: Analysis of lift performance
    """
    average_lift_rate = np.mean(lifted_rates)
    lift_efficiency = (average_lift_rate - initial_rate) / initial_rate
    decline_rate = (lifted_rates[-1] - lifted_rates[0]) / (time[-1] - time[0]) / lifted_rates[0]
    
    return {
        'lift_type': lift_type,
        'initial_rate': initial_rate,
        'average_lift_rate': average_lift_rate,
        'lift_efficiency': lift_efficiency,
        'decline_rate': decline_rate
    }