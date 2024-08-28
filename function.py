import pandas as pd
import matplotlib.pyplot as plt
import numpy
import os


def draw_plots(json_path):
    sigma = 0
    
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    df = pd.read_json(json_path)
    

    for i in range(len(df)):
        sigma += (df['gt_corners'][i] - df['rb_corners'][i]) * (df['gt_corners'][i] - df['rb_corners'][i])


    mse = 1/len(df) * sigma

    print("Mean squared error:", mse)

    plot_paths = []
    
    comparisons = [
        ('mean', 'floor_mean', 'ceiling_mean'),
        ('max', 'floor_max', 'ceiling_max'),
        ('min', 'floor_min', 'ceiling_min')
    ]
    
    for comp in comparisons:
        plot_path = os.path.join('plots', f'comparison_{comp[0]}.png')

        plt.figure(figsize=(10, 6))
        plt.plot(df['name'], df[comp[0]], marker='o', linestyle='-', label='Mean')
        plt.plot(df['name'], df[comp[1]], marker='o', linestyle='-', label='Floor Mean')
        plt.plot(df['name'], df[comp[2]], marker='o', linestyle='-', label='Ceiling Mean')
        plt.xlabel('Room Name')
        plt.ylabel('Degrees')
        plt.title(f'Comparison of {comp[0]} with Floor and Ceiling Mean')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        plot_paths.append(plot_path)
        
    return plot_paths