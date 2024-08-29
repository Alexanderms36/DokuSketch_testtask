import pandas as pd
import matplotlib.pyplot as plt
import os


def save_plot(plot_path):
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()


def draw_anomalies(df, anomaly_threshold):
    df['mean_difference'] = abs(df['floor_mean'] - df['ceiling_mean'])
    anomalies = df[df['mean_difference'] > anomaly_threshold]

    if not anomalies.empty:
        print("Rooms with anomalies:\n", anomalies[['name', 'floor_mean', 'ceiling_mean', 'mean_difference']])
    else:
        print("No anomalies detected.")

    plt.figure(figsize=(10, 6))
    colors = ['red' if diff > anomaly_threshold else 'blue' for diff in df['mean_difference']]
    plt.bar(df['name'], df['mean_difference'], color=colors)

    plt.title(f'Difference between mean deviations for floor and ceiling (Total anomalies: {anomalies.shape[0]})', fontsize=16)
    plt.xlabel('Room', fontsize=12)
    plt.ylabel('Difference between mean deviations', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    save_plot(plot_path := os.path.join('plots', 'comparison_anomaly.png'))
    return plot_path

def draw_comparison_plots(df):
    comparisons = [
        ('mean', 'floor_mean', 'ceiling_mean'),
        ('max', 'floor_max', 'ceiling_max'),
        ('min', 'floor_min', 'ceiling_min')
    ]

    plot_paths = []

    for comp in comparisons:
        plt.figure(figsize=(10, 6))
        plt.plot(df['name'], df[comp[0]], marker='o', linestyle='-', label='Mean')
        plt.plot(df['name'], df[comp[1]], marker='o', linestyle='-', label='Floor Mean')
        plt.plot(df['name'], df[comp[2]], marker='o', linestyle='-', label='Ceiling Mean')
        plt.xlabel('Room Name')
        plt.ylabel('Degrees')
        plt.title(f'Comparison of {comp[0]} with Floor and Ceiling Mean')
        plt.xticks(rotation=45, ha='right')
        plt.legend()

        plot_path = os.path.join('plots', f'comparison_{comp[0]}.png')
        save_plot(plot_path)
        plot_paths.append(plot_path)

    return plot_paths


def generate_statistics(df):
    stats = {
        'Mean Floor Error': df.groupby('name')['floor_mean'].mean(),
        'Mean Ceiling Error': df.groupby('name')['ceiling_mean'].mean(),
        'Max Floor Error': df.groupby('name')['floor_max'].max(),
        'Max Ceiling Error': df.groupby('name')['ceiling_max'].max(),
        'Min Floor Error': df.groupby('name')['floor_min'].min(),
        'Min Ceiling Error': df.groupby('name')['ceiling_min'].min(),
        'GT vs RB': df.groupby('name')[['gt_corners', 'rb_corners']].mean()
    }

    for key, value in stats.items():
        print(f"\n{key}:\n", value)

    plt.figure(figsize=(12, 6))
    stats['Mean Floor Error'].plot(kind='bar', color='blue', label='Mean Floor Error')
    stats['Mean Ceiling Error'].plot(kind='bar', color='green', label='Mean Ceiling Error', alpha=0.7)
    plt.title('Average Mean Error per Room')
    plt.xlabel('Room')
    plt.ylabel('Average Error')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    save_plot(plot_path1 := os.path.join('plots', 'average_mean_error_per_room.png'))

    plt.figure(figsize=(12, 6))
    stats['Max Floor Error'].plot(kind='bar', color='lightcoral', label='Max Floor Error')
    stats['Max Ceiling Error'].plot(kind='bar', color='green', label='Max Ceiling Error', alpha=0.7)
    stats['Min Floor Error'].plot(kind='bar', color='blue', label='Min Floor Error', alpha=0.7)
    stats['Min Ceiling Error'].plot(kind='bar', color='deepskyblue', label='Min Ceiling Error', alpha=0.7)
    plt.title('Max and Min Errors per Room')
    plt.xlabel('Room')
    plt.ylabel('Error')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    save_plot(plot_path2 := os.path.join('plots', 'max_min_errors_per_room.png'))
    
    return plot_path1, plot_path2

def draw_plots(json_path):
    try:
        df = pd.read_json(json_path)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

    if not os.path.exists('plots'):
        os.makedirs('plots')

    plot_paths = draw_comparison_plots(df)
    plot_paths += generate_statistics(df)
    plot_paths.append(draw_anomalies(df, 10))

    return plot_paths
