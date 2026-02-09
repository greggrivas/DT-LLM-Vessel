import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================================================
# 1. INITIAL SETTING - CHANGE THIS VALUE TO SWITCH TARGET
# =========================================================
# Options: 'Compressor_Decay' or 'Turbine_Decay'
TARGET = 'Turbine_Decay' 

# Automatic Folder Management
FOLDER = 'Compressor decay' if TARGET == 'Compressor_Decay' else 'Turbine decay'
os.makedirs(FOLDER, exist_ok=True)

# 2. Data Preparation
df = pd.read_csv('cleaned_data.csv')

# Features: Drop targets and constant sensors
X = df.drop(columns=['Compressor_Decay', 'Turbine_Decay', 'T1', 'P1'])
y = df[TARGET]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling (Required for Ridge and SVR)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Model Definition
models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Ridge Regression': Ridge(alpha=1.0),
    'SVR': SVR(kernel='rbf', epsilon=0.001, C=10)
}

# 4. Training, Prediction, and Metric Collection
perf_metrics = []
trained_models = {}

for name, model in models.items():
    if name in ['SVR', 'Ridge Regression']:
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
    
    trained_models[name] = model
    
    # Store Metrics
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    perf_metrics.append({'Model': name, 'MAE': mae, 'MSE': mse, 'R2': r2})
    
    # Generate Scatter Plot
    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, preds, alpha=0.3, s=10)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.title(f'{TARGET} - {name}\nActual vs Predicted')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.tight_layout()
    # Save inside specific folder
    plt.savefig(os.path.join(FOLDER, f"{TARGET}_{name.lower().replace(' ', '_')}_scatter.png"))
    plt.close()

# 5. Output Summary Table
perf_df = pd.DataFrame(perf_metrics)
print(f"--- Analysis Complete for: {TARGET} ---")
print(perf_df)

# 6. Error Comparison Plot (Log Scale)
plt.figure(figsize=(10, 6))
perf_df.set_index('Model')[['MAE', 'MSE']].plot(kind='bar', figsize=(10, 6))
plt.yscale('log')
plt.title(f'Error Magnitude Comparison ({TARGET})')
plt.ylabel('Value (Log Scale)')
plt.xticks(rotation=45)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(FOLDER, f"{TARGET}_error_comparison.png"))
plt.close()

# 7. R2 Comparison Plot
plt.figure(figsize=(10, 6))
plt.bar(perf_df['Model'], perf_df['R2'], color='skyblue', edgecolor='navy')
plt.title(f'R2 Comparison ({TARGET})')
plt.ylabel('Score')
plt.ylim(0, 1.1)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(FOLDER, f"{TARGET}_r2_comparison.png"))
plt.close()

# 8. Feature Importance Plot (Random Forest)
rf_model = trained_models['Random Forest']
importances = rf_model.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title(f'Random Forest Feature Importance ({TARGET})')
plt.barh(range(len(indices)), importances[indices], align='center', color='forestgreen')
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel('Relative Importance')
plt.tight_layout()
plt.savefig(os.path.join(FOLDER, f"{TARGET}_rf_feature_importance.png"))
plt.close()