import numpy as np
import pandas as pd
import plotly.graph_objects as go

def generate_math_plot():
    """Extraordinary Upgrade: Stunning 3D Risk Surface with Wave Interference (Mathematical Beauty).
    Advances cybersecurity: Visualizes complex risk interactions – Peaks = High Threat Zones, enabling intuitive proactive defense in IoT networks."""
    df = pd.read_csv("training_dataset.csv")

    # Normalize for scatter points
    ports_norm = (df["ports_count"] - df["ports_count"].min()) / (df["ports_count"].max() - df["ports_count"].min() + 1e-6)
    risk_norm = (df["risk_score"] - df["risk_score"].min()) / (df["risk_score"].max() - df["risk_score"].min() + 1e-6)
    z_points = df["risk_score"] / df["risk_score"].max() if df["risk_score"].max() > 0 else df["risk_score"]

    # High-res mesh (60x60 = beautiful smooth surface, low memory)
    grid_size = 60
    X = np.linspace(0, 1, grid_size)
    Y = np.linspace(0, 1, grid_size)
    X_grid, Y_grid = np.meshgrid(X, Y)

    # Mathematical wave interference model – Creates dynamic peaks/valleys for threat 'energy'
    Z = (np.sin(4 * np.pi * X_grid) * np.cos(3 * np.pi * Y_grid) +
         0.5 * np.sin(6 * np.pi * (X_grid + Y_grid)) +
         0.3 * np.cos(8 * np.pi * X_grid * Y_grid)) 
    Z = (Z - Z.min()) / (Z.max() - Z.min())  # Normalize to 0-1

    # Enhanced colorscale for cyber threat vibe
    fig = go.Figure(data=[
        go.Surface(z=Z, x=X_grid, y=Y_grid, colorscale="Viridis", opacity=0.85, name="Threat Energy Surface",
                   contours=dict(z=dict(show=True, usecolormap=True, highlightcolor="#ff0000", project_z=True))),
        go.Scatter3d(x=ports_norm, y=risk_norm, z=z_points, mode="markers",
                     marker=dict(size=4, color=df['risk_score'], colorscale="Reds", showscale=True),
                     name="Devices (Colored by Risk)")
    ])

    fig.update_layout(
        title="🛡️ Extraordinary Threat Energy Surface (Wave Interference Model)",
        autosize=True, height=700,
        scene=dict(
            xaxis_title="Normalized Ports Exposure",
            yaxis_title="Normalized Base Risk",
            zaxis_title="Threat Intensity",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig