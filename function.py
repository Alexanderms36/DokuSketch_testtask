import pandas as pd
import matplotlib.pyplot as plt
import os


def save_plot(plot_path):
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()


def plot_bar_chart(df, x_col, y_col, colors, title, xlabel, ylabel, plot_path):
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col], df[y_col], color=colors)
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha='right')
    save_plot(plot_path)


def draw_anomalies(df, anomaly_threshold):
    df['mean_difference'] = (df['floor_mean'] - df['ceiling_mean']).abs()
    anomalies = df[df['mean_difference'] > anomaly_threshold]

    if not anomalies.empty:
        print("Rooms with anomalies:\n", anomalies[['name', 'floor_mean', 'ceiling_mean', 'mean_difference']])
    else:
        print("No anomalies detected.")

    colors = ['red' if diff > anomaly_threshold else 'blue' for diff in df['mean_difference']]
    plot_bar_chart(df, 'name', 'mean_difference', colors,
                   f'Difference between mean deviations for floor and ceiling (Total anomalies: {anomalies.shape[0]})',
                   'Room', 'Difference between mean deviations',
                   os.path.join('plots', 'comparison_anomaly.png'))

    return os.path.join('plots', 'comparison_anomaly.png')


def draw_comparison_plots(df):
    comparisons = [
        ('mean', 'floor_mean', 'ceiling_mean'),
        ('max', 'floor_max', 'ceiling_max'),
        ('min', 'floor_min', 'ceiling_min')
    ]

    plot_paths = []
    for label, floor_col, ceiling_col in comparisons:
        plt.figure(figsize=(10, 6))
        plt.plot(df['name'], df[label], marker='o', label='Mean')
        plt.plot(df['name'], df[floor_col], marker='o', label='Floor')
        plt.plot(df['name'], df[ceiling_col], marker='o', label='Ceiling')
        plt.xlabel('Room Name')
        plt.ylabel('Degrees')
        plt.title(f'Comparison of {label} with Floor and Ceiling')
        plt.xticks(rotation=45, ha='right')
        plt.legend()

        plot_path = os.path.join('plots', f'comparison_{label}.png')
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

    plot_bar_chart(df, 'name', 'floor_mean', 'blue', 'Average Mean Error per Room', 'Room', 'Average Error',
                   os.path.join('plots', 'average_mean_error_per_room.png'))

    plot_bar_chart(df, 'name', 'floor_max', 'lightcoral', 'Max and Min Errors per Room', 'Room', 'Error',
                   os.path.join('plots', 'max_min_errors_per_room.png'))

    return (os.path.join('plots', 'average_mean_error_per_room.png'),
            os.path.join('plots', 'max_min_errors_per_room.png'))


def draw_plots(json_path):
    try:
        df = pd.read_json(json_path)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

    threshold = 10

    os.makedirs('plots', exist_ok=True)

    plot_paths = draw_comparison_plots(df)
    plot_paths += generate_statistics(df)
    plot_paths.append(draw_anomalies(df, threshold))

    return plot_paths
