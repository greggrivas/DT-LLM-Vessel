"""
Marine Vessel Propulsion System - Plot Generator
Generates all analysis plots for the presentation.
Run this script to create all plots in the output folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
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

    # Select representative decay states (New, Mid, Worn)
    available_decays = sorted(df['Compressor_Decay'].unique())
    selected_decays = [available_decays[0], available_decays[len(available_decays)//2], available_decays[-1]]

    df_lines = df[df['Compressor_Decay'].isin(selected_decays)]

    sns.lineplot(
        data=df_lines,
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
    plot_sensor_boxplots(df)
    plot_decay_vs_p2(df)
    plot_decay_vs_t48(df)
    plot_decay_distributions(df)
    plot_operating_lines(df)

    print("-" * 30)
    print(f"\nAll plots saved to '{OUTPUT_FOLDER}/' folder")
    print("=" * 50)


if __name__ == "__main__":
    main()
