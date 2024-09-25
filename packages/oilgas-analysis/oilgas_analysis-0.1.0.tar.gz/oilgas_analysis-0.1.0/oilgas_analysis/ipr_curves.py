import numpy as np
import matplotlib.pyplot as plt

def generate_ipr_curve(reservoir_pressure, bubble_point_pressure, productivity_index, water_cut=0):
    """
    Generate Inflow Performance Relationship (IPR) curve.
    
    Parameters:
    reservoir_pressure (float): Reservoir pressure in psi
    bubble_point_pressure (float): Bubble point pressure in psi
    productivity_index (float): Productivity index in STB/day/psi
    water_cut (float): Water cut as a fraction (0 to 1)
    
    Returns:
    tuple: Arrays of bottomhole pressures and corresponding flow rates
    """
    pressures = np.linspace(0, reservoir_pressure, 100)
    rates = []
    
    for p in pressures:
        if p >= bubble_point_pressure:
            q = productivity_index * (reservoir_pressure - p)
        else:
            q = productivity_index * bubble_point_pressure * (1 - 0.2 * (p/bubble_point_pressure) - 0.8 * (p/bubble_point_pressure)**2)
        
        # Adjust for water cut
        q_oil = q * (1 - water_cut)
        rates.append(q_oil)
    
    return pressures, np.array(rates)

def plot_ipr_curve(pressures, rates, title="Inflow Performance Relationship"):
    """
    Plot the IPR curve.
    
    Parameters:
    pressures (array): Array of bottomhole pressures
    rates (array): Array of corresponding flow rates
    title (str): Title for the plot
    """
    plt.figure(figsize=(10, 6))
    plt.plot(rates, pressures)
    plt.title(title)
    plt.xlabel("Flow Rate (STB/day)")
    plt.ylabel("Bottomhole Pressure (psi)")
    plt.grid(True)
    plt.gca().invert_yaxis()
    plt.show()