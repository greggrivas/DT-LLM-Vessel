# Marine Vessel Propulsion System - Presentation Dialog

## Slide 1: Introduction & Dataset Overview

**Dialog:**

"Today we present our analysis of a Marine Vessel Propulsion System using gas turbine sensor data. The dataset contains 18 features including ship operational parameters, gas turbine measurements, and component decay coefficients.

Key variables include:
- **Operational:** Lever position, ship speed (3-27 knots)
- **Turbine metrics:** GT torque, RPM, temperatures (T1, T2, T48), pressures (P1, P2, P48, Pexh)
- **Propulsion:** Starboard and port propeller torque
- **Health indicators:** Compressor decay (0.95-1.0) and turbine decay (0.975-1.0) coefficients

The decay coefficients represent component degradation, where 1.0 indicates a new component and lower values indicate wear."

---

## Slide 2: Data Cleaning & Preparation

**Dialog:**

"Before analysis, we performed data cleaning using pandas to ensure data quality.

**Duplicate Check:**
```python
df.duplicated().sum()  # Result: 0 duplicates found
```

**Missing Values:**
```python
df.isnull().sum()  # Result: No missing values across all 18 columns
```

**Data Consistency:**
- Verified all numerical columns have appropriate ranges
- Ship speed ranges from 3-27 knots as expected
- Decay coefficients stay within physical bounds (0.95-1.0 for compressor, 0.975-1.0 for turbine)

The dataset is clean with 11,934 complete records, ready for analysis. This is reflected in our data summary plot showing 100% completeness across all variables."

---

## Slide 3: Correlation Analysis

**Dialog:**

"Our correlation heatmap reveals strong relationships across most operational parameters. Ship speed, lever position, torque, RPM, temperatures, and pressures all show correlations above 0.90 - this is expected as they represent interconnected physical systems.

The critical finding: **decay coefficients show near-zero correlation with other variables** (values between -0.05 and 0.04). This means component degradation is independent of operating conditions and cannot be directly inferred from standard sensor readings alone.

This highlights the challenge in predictive maintenance - degradation occurs gradually regardless of how the vessel operates, making early detection crucial."

---

## Slide 4: Impact of Component Decay

**Dialog:**

"Despite low overall correlation, decay has measurable effects when we control for operating conditions. At a fixed speed of 15 knots:

- **Compressor decay** directly affects outlet pressure (P2): A worn compressor (0.95) produces lower pressure than a new one (1.0), dropping from ~11.27 bar to ~10.90 bar.

The operating lines plot shows the practical impact: **degraded components require more fuel to maintain the same speed**. At 27 knots, a worn engine (decay 0.95) consumes approximately 1.8 kg/s of fuel compared to 1.7 kg/s for a healthy engine - roughly 6% higher fuel consumption.

This fuel efficiency loss represents significant operational costs over time."

---

## Slide 5: Conclusions & Digital Twin Application

**Dialog:**

"Our analysis demonstrates the value of data-driven monitoring for marine propulsion systems:

**Key Findings:**
1. Component decay is independent of operating conditions but measurably impacts performance
2. Degraded components reduce pressure output and increase fuel consumption
3. Effects become more pronounced at higher speeds

**Digital Twin Potential:**
- Real-time monitoring of decay indicators
- Predictive maintenance scheduling before critical failures
- Fuel consumption optimization through condition-based operation
- Cost savings through proactive rather than reactive maintenance

By building a digital twin that monitors these parameters, we can predict maintenance needs and optimize vessel operations for both performance and economy."

---

## Suggested Visuals per Slide

| Slide | Recommended Plot |
|-------|------------------|
| 1 | Dataset statistics or sensor boxplots |
| 2 | Data summary plot (completeness + operating conditions) |
| 3 | Correlation heatmap |
| 4 | Operating lines + Decay vs P2 plot |
| 5 | Speed vs fuel decay scatter plot |
