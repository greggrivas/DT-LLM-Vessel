import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# Load your data
df = pd.read_csv('cleaned_data.csv') 

# 1. Select a high-speed operating point (e.g., 27 knots)
# This is where the engine is under high load and health differences are most visible
speed_val = 15
df_3d = df[df['Ship_Speed'] == speed_val]

# 2. Prepare the Grid (Pivot the data)
# X = Turbine Decay, Y = Compressor Decay, Z = Fuel Flow
pivot = df_3d.pivot_table(values='Fuel_Flow', index='Compressor_Decay', columns='Turbine_Decay')

X_vals = pivot.columns.values
Y_vals = pivot.index.values
X, Y = np.meshgrid(X_vals, Y_vals)
Z = pivot.values

# 3. Create the Advanced 3D Plot
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot a smooth surface with the 'coolwarm' colormap
# Blue = Healthy/Low Fuel | Red = Worn/High Fuel
surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8, edgecolor='none', antialiased=True)

# Add a subtle wireframe to give it a "digital grid" look
ax.plot_wireframe(X, Y, Z, color='black', alpha=0.1, linewidth=0.5)

# 4. AXIS LOGIC: We invert the axes so '1.0' (New) is at the back 
# and '0.95' (Worn) is at the front. 
# This makes the "climb" in fuel consumption look like a mountain we are rising up.
ax.set_xlim(1.0, 0.975)
ax.set_ylim(1.0, 0.95)

# Labels with LaTeX for a professional look
ax.set_xlabel('Turbine Decay ($k_{mt}$)', fontsize=12, labelpad=10)
ax.set_ylabel('Compressor Decay ($k_{mc}$)', fontsize=12, labelpad=10)
ax.set_zlabel('Fuel Flow (kg/s)', fontsize=12, labelpad=10)
ax.set_title(f'Digital Twin: Fuel Consumption Surface at {speed_val} Knots\n(Visualizing Combined Component Degradation)', fontsize=15, pad=20)

# Add a color bar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Fuel Flow Rate (kg/s)', rotation=270, labelpad=20)

# Set the perspective (Elev = height angle, Azim = rotation)
ax.view_init(elev=30, azim=135)

plt.tight_layout()
plt.savefig("advanced_engine_surface_3d.png", dpi=300)

# 1. Create the Height Grid (Fuel Flow)
pivot_z = df_3d.pivot_table(values='Fuel_Flow', index='Compressor_Decay', columns='Turbine_Decay')
Z = pivot_z.values

# 2. Create the Color Grid (Exhaust Gas Temperature)
# Replace 'GT_exhaust_gas_temperature' with the exact name from your columns
pivot_temp = df_3d.pivot_table(values='T48', index='Compressor_Decay', columns='Turbine_Decay')
Temp = pivot_temp.values

# Normalize Temperature values to a 0-1 range for the colormap
min_temp, max_temp = Temp.min(), Temp.max()
Temp_norm = (Temp - min_temp) / (max_temp - min_temp)

# 3. Plotting
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# We apply the 'magma' or 'hot' colormap specifically to the Temperature data
surf = ax.plot_surface(X, Y, Z, facecolors=cm.magma(Temp_norm), shade=False, antialiased=True)

ax.set_zlabel('Fuel Flow (kg/s) [Height]')
ax.set_title('Digital Twin: Fuel Consumption (Height) vs. Exhaust Temp (Color)')

# Add a colorbar that specifically explains the Temperature
sm = cm.ScalarMappable(cmap=cm.magma)
sm.set_array(Temp)
cbar = fig.colorbar(sm, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Exhaust Gas Temperature (C)', rotation=270, labelpad=20)

plt.show()