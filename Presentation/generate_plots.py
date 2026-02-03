"""
Marine Vessel Propulsion System - Plot Generator
Generates all analysis plots for the presentation.
Run this script to create all plots in the output folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import os

# Configuration
OUTPUT_FOLDER = "Generated_Plots"
DATA_FILE = "../DT-LLM-Vessel/cleaned_data.csv"

def setup_output_folder():
    """Create output folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    print(f"Output folder: {OUTPUT_FOLDER}")

def load_data():
    """Load the cleaned dataset."""
    df = pd.read_csv(DATA_FILE)
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    return df

def plot_correlation_heatmap(df):
    """Generate correlation heatmap of all gas turbine measures."""
    plt.figure(figsize=(14, 10))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of Gas Turbine Measures')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "correlation_heatmap.png"), dpi=300)
    plt.close()
    print("Created: correlation_heatmap.png")

def plot_speed_vs_fuel_decay(df):
    """Scatter plot of ship speed vs fuel flow colored by compressor decay."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Ship_Speed', y='Fuel_Flow',
                    hue='Compressor_Decay', palette='icefire', alpha=0.6)
    plt.title('Relationship between Ship Speed and Fuel Flow (colored by Compressor Decay)')
    plt.xlabel('Ship Speed (knots)')
    plt.ylabel('Fuel Flow (kg/s)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "speed_vs_fuel_decay.png"), dpi=300)
    plt.close()
    print("Created: speed_vs_fuel_decay.png")

def plot_speed_vs_fuel_lines(df):
    """Line plot of ship speed vs fuel flow - averaged across all turbine decay values."""
    plt.figure(figsize=(10, 6))

    # Select specific compressor decay values (include ALL turbine decay values)
    selected_decays = [0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    df_selected = df[df['Compressor_Decay'].isin(selected_decays)]

    # Average fuel flow across all turbine decay values for each (compressor_decay, speed)
    df_avg = df_selected.groupby(['Compressor_Decay', 'Ship_Speed'])['Fuel_Flow'].mean().reset_index()

    # Plot lines connecting averaged data points
    for decay in selected_decays:
        subset = df_avg[df_avg['Compressor_Decay'] == decay].sort_values('Ship_Speed')
        plt.plot(subset['Ship_Speed'], subset['Fuel_Flow'],
                 marker='o', markersize=4, linewidth=1.5, label=f'{decay}')

    plt.title('Ship Speed vs Fuel Flow (Averaged Across All Turbine Decay Values)')
    plt.xlabel('Ship Speed (knots)')
    plt.ylabel('Fuel Flow (kg/s)')
    plt.legend(title='Compressor Decay')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "speed_vs_fuel_lines.png"), dpi=300)
    plt.close()
    print("Created: speed_vs_fuel_lines.png")

def plot_speed_vs_fuel_decay_filtered(df):
    """Scatter plot of ship speed vs fuel flow - filtered to speed >= 9 knots."""
    plt.figure(figsize=(10, 6))
    df_filtered = df[df['Ship_Speed'] >= 9]
    sns.scatterplot(data=df_filtered, x='Ship_Speed', y='Fuel_Flow',
                    hue='Compressor_Decay', palette='icefire', alpha=0.6)
    plt.title('Ship Speed vs Fuel Flow (Speed >= 9 knots)')
    plt.xlabel('Ship Speed (knots)')
    plt.ylabel('Fuel Flow (kg/s)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "speed_vs_fuel_decay_filtered.png"), dpi=300)
    plt.close()
    print("Created: speed_vs_fuel_decay_filtered.png")

def plot_speed_vs_fuel_lines_filtered(df):
    """Line plot of ship speed vs fuel flow - filtered to speed >= 9 knots, averaged across turbine decay."""
    plt.figure(figsize=(10, 6))

    # Select specific compressor decay values, speed >= 9 (include ALL turbine decay values)
    selected_decays = [0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    df_selected = df[(df['Compressor_Decay'].isin(selected_decays)) &
                     (df['Ship_Speed'] >= 9)]

    # Average fuel flow across all turbine decay values for each (compressor_decay, speed)
    df_avg = df_selected.groupby(['Compressor_Decay', 'Ship_Speed'])['Fuel_Flow'].mean().reset_index()

    # Plot lines connecting averaged data points
    for decay in selected_decays:
        subset = df_avg[df_avg['Compressor_Decay'] == decay].sort_values('Ship_Speed')
        plt.plot(subset['Ship_Speed'], subset['Fuel_Flow'],
                 marker='o', markersize=4, linewidth=1.5, label=f'{decay}')

    plt.title('Ship Speed vs Fuel Flow (Averaged Across Turbine Decay, Speed >= 9 knots)')
    plt.xlabel('Ship Speed (knots)')
    plt.ylabel('Fuel Flow (kg/s)')
    plt.legend(title='Compressor Decay')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "speed_vs_fuel_lines_filtered.png"), dpi=300)
    plt.close()
    print("Created: speed_vs_fuel_lines_filtered.png")

def plot_sensor_boxplots(df):
    """Boxplots for outlier detection of key sensors."""
    sensors_to_plot = ['T48', 'T2', 'P48', 'P2', 'Fuel_Flow']
    fig, axes = plt.subplots(1, 5, figsize=(15, 6))
    for ax, sensor in zip(axes, sensors_to_plot):
        sns.boxplot(y=df[sensor], ax=ax, color='steelblue')
        ax.set_title(sensor)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "sensor_boxplots.png"), dpi=300)
    plt.close()
    print("Created: sensor_boxplots.png")

def plot_data_summary(df):
    """Data quality summary showing dataset statistics."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Missing values and data completeness
    missing = df.isnull().sum()
    completeness = ((len(df) - missing) / len(df) * 100).sort_values()
    axes[0].barh(completeness.index, completeness.values, color='steelblue')
    axes[0].set_xlim(95, 100.5)
    axes[0].set_xlabel('Completeness (%)')
    axes[0].set_title(f'Data Completeness (n={len(df):,} rows)')
    axes[0].axvline(x=100, color='green', linestyle='--', alpha=0.7)

    # Right: Distribution of ship speeds (operating conditions coverage)
    sns.histplot(df['Ship_Speed'], bins=20, kde=True, ax=axes[1], color='steelblue')
    axes[1].set_title('Distribution of Operating Conditions (Ship Speed)')
    axes[1].set_xlabel('Ship Speed (knots)')
    axes[1].set_ylabel('Count')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "data_summary.png"), dpi=300)
    plt.close()
    print("Created: data_summary.png")

def plot_decay_vs_p2(df):
    """Scatter plot showing compressor decay effect on outlet pressure at 15 knots."""
    speed_15 = df[df['Ship_Speed'] == 15]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=speed_15, x='Compressor_Decay', y='P2', alpha=0.7)
    plt.title('How Compressor Decay affects Outlet Pressure (P2) at 15 knots')
    plt.xlabel('Compressor Decay Coefficient (1.0 = New, 0.95 = Worn)')
    plt.ylabel('Compressor Outlet Pressure (P2) [bar]')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "decay_vs_p2_explanation.png"), dpi=300)
    plt.close()
    print("Created: decay_vs_p2_explanation.png")

def plot_decay_vs_t48(df):
    """Scatter plot showing turbine decay effect on exit temperature at 15 knots."""
    speed_15 = df[df['Ship_Speed'] == 15]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=speed_15, x='Turbine_Decay', y='T48', color='orange', alpha=0.7)
    plt.title('How Turbine Decay affects Exit Temperature (T48) at 15 knots')
    plt.xlabel('Turbine Decay Coefficient (1.0 = New, 0.975 = Worn)')
    plt.ylabel('HP Turbine Exit Temperature (T48) [C]')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "decay_vs_t48_explanation.png"), dpi=300)
    plt.close()
    print("Created: decay_vs_t48_explanation.png")

def plot_decay_distributions(df):
    """Histogram distributions of decay coefficients."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df['Compressor_Decay'], bins=20, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('Distribution of Compressor Decay')
    axes[0].set_xlabel('Compressor Decay Coefficient')
    sns.histplot(df['Turbine_Decay'], bins=20, kde=True, ax=axes[1], color='red')
    axes[1].set_title('Distribution of Turbine Decay')
    axes[1].set_xlabel('Turbine Decay Coefficient')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "decay_distributions.png"), dpi=300)
    plt.close()
    print("Created: decay_distributions.png")

def plot_operating_lines(df):
    """Operating lines: Fuel flow vs ship speed across decay states."""
    plt.figure(figsize=(12, 7))

    # Select representative compressor decay states (New, Mid, Worn)
    selected_decays = [0.95, 0.975, 1.0]
    df_selected = df[df['Compressor_Decay'].isin(selected_decays)]

    # Group by decay and speed, take mean fuel flow (same as scatter plot data)
    df_grouped = df_selected.groupby(['Compressor_Decay', 'Ship_Speed'])['Fuel_Flow'].mean().reset_index()

    sns.lineplot(
        data=df_grouped,
        x='Ship_Speed',
        y='Fuel_Flow',
        hue='Compressor_Decay',
        palette='viridis',
        style='Compressor_Decay',
        markers=True,
        dashes=False,
        linewidth=2.5,
        markersize=8
    )

    plt.title('Operating Lines: Fuel Flow vs. Ship Speed\n(Comparing Engine Health States)', fontsize=14)
    plt.xlabel('Ship Speed (knots)', fontsize=12)
    plt.ylabel('Fuel Flow (kg/s)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title='Compressor Decay State')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "operating_lines.png"), dpi=300)
    plt.close()
    print("Created: operating_lines.png")


def plot_3d_speed_fuel_decay(df):
    """3D surface plot of compressor decay, turbine decay, and fuel flow colored by exhaust temp."""
    import numpy as np
    from matplotlib import cm
    from matplotlib.colors import Normalize

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Fix ship speed to 15 knots for a clean surface
    df_speed = df[df['Ship_Speed'] == 15]

    # Create pivot tables for fuel flow and temperature
    fuel_pivot = df_speed.pivot_table(
        values='Fuel_Flow',
        index='Compressor_Decay',
        columns='Turbine_Decay',
        aggfunc='mean'
    )
    temp_pivot = df_speed.pivot_table(
        values='T48',
        index='Compressor_Decay',
        columns='Turbine_Decay',
        aggfunc='mean'
    )

    # Create meshgrid
    X = fuel_pivot.columns.values  # Turbine Decay
    Y = fuel_pivot.index.values    # Compressor Decay
    X, Y = np.meshgrid(X, Y)
    Z = fuel_pivot.values          # Fuel Flow

    # Normalize temperature for color mapping
    norm = Normalize(vmin=temp_pivot.values.min(), vmax=temp_pivot.values.max())
    colors = cm.hot_r(norm(temp_pivot.values))

    # Plot surface
    surf = ax.plot_surface(X, Y, Z, facecolors=colors, alpha=0.9, shade=True)

    ax.set_xlabel('Turbine Decay')
    ax.set_ylabel('Compressor Decay')
    ax.set_zlabel('Fuel Flow (kg/s)')
    ax.set_title('3D Surface: Decay States vs Fuel Flow at 15 knots\n(Color = Exhaust Temperature T48)')

    # Add colorbar
    mappable = cm.ScalarMappable(norm=norm, cmap='hot_r')
    mappable.set_array(temp_pivot.values)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label('Exhaust Temperature T48 (°C)')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "3d_speed_fuel_decay.png"), dpi=300)
    plt.close()
    print("Created: 3d_speed_fuel_decay.png")


def main():
    """Generate all plots."""
    print("=" * 50)
    print("Marine Vessel Propulsion System - Plot Generator")
    print("=" * 50)

    setup_output_folder()
    df = load_data()

    print("\nGenerating plots...")
    print("-" * 30)

    # Generate all plots
    plot_data_summary(df)
    plot_correlation_heatmap(df)
    plot_speed_vs_fuel_decay(df)
    plot_speed_vs_fuel_lines(df)
    plot_speed_vs_fuel_decay_filtered(df)
    plot_speed_vs_fuel_lines_filtered(df)
    plot_sensor_boxplots(df)
    plot_decay_vs_p2(df)
    plot_decay_vs_t48(df)
    plot_decay_distributions(df)
    plot_operating_lines(df)
    plot_3d_speed_fuel_decay(df)

    print("-" * 30)
    print(f"\nAll plots saved to '{OUTPUT_FOLDER}/' folder")
    print("=" * 50)


if __name__ == "__main__":
    main()
