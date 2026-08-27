import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
    "Adjust the amplitude, frequency, wavelength, and time "
    "to see how they affect a transverse wave."
)

# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------

st.sidebar.header("Wave Controls")

amplitude = st.sidebar.slider(
    "Amplitude (m)",
    min_value=0.1,
    max_value=5.0,
    value=2.0,
    step=0.1
)

frequency = st.sidebar.slider(
    "Frequency (Hz)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1
)

wavelength = st.sidebar.slider(
    "Wavelength (m)",
    min_value=1.0,
    max_value=20.0,
    value=10.0,
    step=0.5
)

time = st.sidebar.slider(
    "Time (s)",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.1
)

# --------------------------------------------------
# Calculate Wave Properties
# --------------------------------------------------

wave_number = 2 * np.pi / wavelength

angular_frequency = 2 * np.pi * frequency

wave_speed = frequency * wavelength

period = 1 / frequency

# --------------------------------------------------
# Create x values
# --------------------------------------------------

x = np.linspace(
    0,
    2 * wavelength,
    1000
)

# --------------------------------------------------
# Sinusoidal Wave Equation
# --------------------------------------------------

y = amplitude * np.sin(
    wave_number * x - angular_frequency * time
)

# --------------------------------------------------
# Create Matplotlib Figure
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    x,
    y,
    linewidth=3
)

# Equilibrium line
ax.axhline(
    0,
    linestyle="--",
    linewidth=1.5
)

# --------------------------------------------------
# Labels
# --------------------------------------------------

ax.set_title(
    "Transverse Sinusoidal Wave",
    fontsize=18
)

ax.set_xlabel(
    "Position (m)",
    fontsize=13
)

ax.set_ylabel(
    "Displacement (m)",
    fontsize=13
)

ax.set_ylim(
    -amplitude * 1.3,
    amplitude * 1.3
)

ax.grid(True, alpha=0.3)

# --------------------------------------------------
# Display Graph
# --------------------------------------------------

st.pyplot(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Wave Information
# --------------------------------------------------

st.subheader("Wave Properties")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Amplitude",
        f"{amplitude:.2f} m"
    )

with col2:
    st.metric(
        "Frequency",
        f"{frequency:.2f} Hz"
    )

with col3:
    st.metric(
        "Wavelength",
        f"{wavelength:.2f} m"
    )

with col4:
    st.metric(
        "Wave Speed",
        f"{wave_speed:.2f} m/s"
    )

# --------------------------------------------------
# Additional Information
# --------------------------------------------------

st.subheader("Other Wave Quantities")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Wave Number**")
    st.write(f"k = {wave_number:.3f} rad/m")

with col2:
    st.write("**Angular Frequency**")
    st.write(f"ω = {angular_frequency:.3f} rad/s")

with col3:
    st.write("**Period**")
    st.write(f"T = {period:.3f} s")

# --------------------------------------------------
# Equation
# --------------------------------------------------

st.subheader("Wave Equation")

st.latex(
    r"y(x,t) = A\sin(kx-\omega t)"
)

st.write(
    f"With the current values:"
)

st.latex(
    rf"""
    y(x,t) =
    {amplitude:.2f}
    \sin\left(
    {wave_number:.3f}x -
    {angular_frequency:.3f}t
    \right)
    """
)

# --------------------------------------------------
# Physics Relationships
# --------------------------------------------------

st.subheader("Important Relationships")

st.latex(
    r"v = f\lambda"
)

st.latex(
    r"T = \frac{1}{f}"
)

st.latex(
    r"k = \frac{2\pi}{\lambda}"
)

st.latex(
    r"\omega = 2\pi f"
)