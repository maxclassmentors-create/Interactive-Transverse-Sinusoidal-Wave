import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Interactive Transverse Wave",
    page_icon="〰️",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("〰️ Interactive Transverse Sinusoidal Wave")

st.write(
    "Adjust the amplitude and frequency sliders, "
    "then press Play to continuously animate the wave."
)

# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------

st.sidebar.header("Wave Controls")

amplitude = st.sidebar.slider(
    "Amplitude",
    min_value=20,
    max_value=200,
    value=100,
    step=5
)

frequency = st.sidebar.slider(
    "Frequency (Hz)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1
)

# --------------------------------------------------
# Wave Settings
# --------------------------------------------------

wavelength = 400

x = np.linspace(0, 1200, 600)

num_frames = 120

# One complete animation cycle
animation_period = 1 / frequency

times = np.linspace(
    0,
    animation_period,
    num_frames,
    endpoint=False
)

# --------------------------------------------------
# Initial Wave
# --------------------------------------------------

y = amplitude * np.sin(
    2 * np.pi * x / wavelength
)

# --------------------------------------------------
# Create Figure
# --------------------------------------------------

fig = go.Figure()

# Wave
fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(
            width=4
        ),
        name="Wave"
    )
)

# Equilibrium line
fig.add_trace(
    go.Scatter(
        x=[0, 1200],
        y=[0, 0],
        mode="lines",
        line=dict(
            width=2,
            dash="dash"
        ),
        name="Equilibrium"
    )
)

# --------------------------------------------------
# Animation Frames
# --------------------------------------------------

frames = []

for t in times:

    y_frame = amplitude * np.sin(
        2 * np.pi * x / wavelength
        - 2 * np.pi * frequency * t
    )

    frames.append(
        go.Frame(
            data=[
                go.Scatter(
                    x=x,
                    y=y_frame,
                    mode="lines",
                    line=dict(
                        width=4
                    )
                )
            ],
            name=str(t)
        )
    )

fig.frames = frames

# --------------------------------------------------
# Animation Buttons
# --------------------------------------------------

fig.update_layout(
    updatemenus=[
        {
            "type": "buttons",
            "direction": "left",
            "showactive": False,

            "x": 0.5,
            "y": -0.15,

            "xanchor": "center",
            "yanchor": "top",

            "buttons": [

                # PLAY
                {
                    "label": "▶ Play",
                    "method": "animate",

                    "args": [
                        None,

                        {
                            "frame": {
                                "duration": 30,
                                "redraw": True
                            },

                            "transition": {
                                "duration": 0
                            },

                            "fromcurrent": True,

                            # Continuously loop
                            "mode": "immediate"
                        }
                    ]
                },

                # PAUSE
                {
                    "label": "⏸ Pause",
                    "method": "animate",

                    "args": [
                        [None],

                        {
                            "frame": {
                                "duration": 0,
                                "redraw": False
                            },

                            "mode": "immediate"
                        }
                    ]
                }
            ]
        }
    ]
)

# --------------------------------------------------
# Graph Formatting
# --------------------------------------------------

fig.update_layout(

    title="Transverse Sinusoidal Wave",

    xaxis=dict(
        title="Position",
        range=[0, 1200],
        zeroline=False
    ),

    yaxis=dict(
        title="Displacement",
        range=[
            -amplitude * 1.3,
            amplitude * 1.3
        ],
        zeroline=False
    ),

    height=550,

    template="plotly_dark",

    hovermode="x unified",

    margin=dict(
        l=60,
        r=30,
        t=70,
        b=100
    )
)

# --------------------------------------------------
# Display
# --------------------------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Wave Properties
# --------------------------------------------------

st.subheader("Wave Properties")

wave_speed = frequency * wavelength
period = 1 / frequency

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Amplitude",
        f"{amplitude} px"
    )

with col2:
    st.metric(
        "Frequency",
        f"{frequency:.1f} Hz"
    )

with col3:
    st.metric(
        "Wavelength",
        f"{wavelength} px"
    )

with col4:
    st.metric(
        "Wave Speed",
        f"{wave_speed:.1f} px/s"
    )

# --------------------------------------------------
# Equation
# --------------------------------------------------

st.subheader("Wave Equation")

st.latex(
    r"""
    y(x,t) =
    A\sin\left(
    \frac{2\pi}{\lambda}x
    -2\pi ft
    \right)
    """
)