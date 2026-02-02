import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

folder_name = "Data Plots"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

df = pd.read_csv('cleaned_data.csv')
# Rename columns for easier use
# df.columns = df.columns.str.strip()

# rename_dict = {
#     'Lever position': 'Lever_Pos',
#     'Ship speed (v)': 'Ship_Speed',
#     'Gas Turbine (GT) shaft torque (GTT) [kN m]': 'GT_Torque',
#     'GT rate of revolutions (GTn) [rpm]': 'GT_RPM',
#     'Gas Generator rate of revolutions (GGn) [rpm]': 'GG_RPM',
#     'Starboard Propeller Torque (Ts) [kN]': 'Prop_Torque_S',
#     'Port Propeller Torque (Tp) [kN]': 'Prop_Torque_P',
#     'Hight Pressure (HP) Turbine exit temperature (T48) [C]': 'T48',
#     'GT Compressor inlet air temperature (T1) [C]': 'T1',
#     'GT Compressor outlet air temperature (T2) [C]': 'T2',
#     'HP Turbine exit pressure (P48) [bar]': 'P48',
#     'GT Compressor inlet air pressure (P1) [bar]': 'P1',
#     'GT Compressor outlet air pressure (P2) [bar]': 'P2',
#     'GT exhaust gas pressure (Pexh) [bar]': 'Pexh',
#     'Turbine Injecton Control (TIC) [%]': 'TIC',
#     'Fuel flow (mf) [kg/s]': 'Fuel_Flow',
#     'GT Compressor decay state coefficient': 'Compressor_Decay',
#     'GT Turbine decay state coefficient': 'Turbine_Decay'
# }
# df = df.rename(columns=rename_dict).drop(columns=['index'])

# =============================================================================
# Initial inspection graphs for visulization
# =============================================================================

print("Data Head:")
print(df.head())
print("\nData Description:")
print(df.info())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

# checks for variance so columns that dont change; 1 means all entries are the same
constant_cols = [col for col in df.columns if df[col].nunique() <= 1] 
print("Constant columns:", constant_cols)

# 1. Correlation Heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix of Gas Turbine Measures')
plt.tight_layout()
plt.savefig(os.path.join(folder_name,"correlation_heatmap.png"))

# 2. Scatter plot: Ship Speed vs Fuel Flow colored by Compressor Decay
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Ship_Speed', y='Fuel_Flow', hue='Compressor_Decay', palette='icefire', alpha=0.6)
plt.title('Relationship between Ship Speed and Fuel Flow (colored by Compressor Decay)')
plt.tight_layout()
plt.savefig(os.path.join(folder_name,"speed_vs_fuel_decay.png"))

# 3. Boxplots for Outlier Detection (subset of interesting sensors)
sensors_to_plot = ['T48', 'T2', 'P48', 'P2', 'Fuel_Flow']
plt.figure(figsize=(15, 8))
df[sensors_to_plot].plot(kind='box', subplots=True, layout=(1, 5), sharex=False, sharey=False, figsize=(15, 6))
plt.tight_layout()
plt.savefig(os.path.join(folder_name,"sensor_boxplots.png"))

# -----------------------------------------------------------------------------
# MORE DETAILED BOX PLOTS FOR BETTER UNIT CORRELATION
# -----------------------------------------------------------------------------

# Plot 1: Temperatures
plt.figure(figsize=(8, 6))
sns.boxplot(data=df[['T48', 'T2']], palette="Set2")
plt.title('Box Plot: Temperature Sensors (Celsius)')
plt.ylabel('Temperature')
plt.savefig(os.path.join(folder_name,"box_plot_temperatures.png"))

# Plot 2: Pressures
plt.figure(figsize=(8, 6))
sns.boxplot(data=df[['P2', 'P48']], palette="Set3")
plt.title('Box Plot: Pressure Sensors (bar)')
plt.ylabel('Pressure')
plt.savefig(os.path.join(folder_name,"box_plot_pressures.png"))

# Plot 3: Fuel Flow (Single variable example)
plt.figure(figsize=(6, 6))
sns.boxplot(y=df['Fuel_Flow'], color="skyblue")
plt.title('Box Plot: Fuel Flow Distribution')
plt.ylabel('kg/s')
plt.savefig(os.path.join(folder_name,"box_plot_fuel.png"))



# Descriptive stats for the clean data
print("\nDescriptive Statistics:")
print(df.describe().T)


# =============================================================================
# Picking a specific speed (e.g., 15 knots) to show how decay affects sensors
# =============================================================================
speed_15 = df[df['Ship_Speed'] == 15]

# Plot 1: Compressor Decay vs P2 (at 15 knots)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=speed_15, x='Compressor_Decay', y='P2', alpha=0.7)
plt.title('How Compressor Decay affects Outlet Pressure (P2) at 15 knots')
plt.xlabel('Compressor Decay Coefficient (1.0 = New, 0.95 = Worn)')
plt.ylabel('Compressor Outlet Pressure (P2) [bar]')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig(os.path.join(folder_name,"decay_vs_p2_explanation.png"))

# Plot 2: Turbine Decay vs T48 (at 15 knots)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=speed_15, x='Turbine_Decay', y='T48', color='orange', alpha=0.7)
plt.title('How Turbine Decay affects Exit Temperature (T48) at 15 knots')
plt.xlabel('Turbine Decay Coefficient (1.0 = New, 0.975 = Worn)')
plt.ylabel('HP Turbine Exit Temperature (T48) [C]')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig(os.path.join(folder_name,"decay_vs_t48_explanation.png"))

# Plot 3: Distribution of Decay Coefficients
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.histplot(df['Compressor_Decay'], bins=20, kde=True, ax=axes[0], color='blue')
axes[0].set_title('Distribution of Compressor Decay')
sns.histplot(df['Turbine_Decay'], bins=20, kde=True, ax=axes[1], color='red')
axes[1].set_title('Distribution of Turbine Decay')
plt.tight_layout()
plt.savefig(os.path.join(folder_name,"decay_distributions.png"))

# =============================================================================
# OPERATING LINES: Fuel Flow vs Ship Speed across Decay States
# =============================================================================
plt.figure(figsize=(12, 7))

# Identify unique decay states to pick representative samples (New, Mid, Worn)
available_decays = sorted(df['Compressor_Decay'].unique())
selected_decays = [available_decays[0], available_decays[len(available_decays)//2], available_decays[-1]]

# Filter for these specific decay states
df_lines = df[df['Compressor_Decay'].isin(selected_decays)]

# Plotting the continuous lines
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

# Save the plot inside your folder
plt.savefig(os.path.join(folder_name, "operating_lines.png"), dpi=300)