import streamlit as st
import streamlit.components.v1 as components

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
    "Adjust the amplitude and frequency to see how they "
    "affect a transverse wave."
)

# --------------------------------------------------
# Streamlit Controls
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
# Fixed Wave Properties
# --------------------------------------------------

wavelength = 400

# --------------------------------------------------
# Calculate Properties
# --------------------------------------------------

wave_speed = frequency * wavelength
period = 1 / frequency

# --------------------------------------------------
# Plotly + JavaScript
# --------------------------------------------------

html_code = f"""
<!DOCTYPE html>

<html>

<head>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>

body {{
    margin: 0;
    background-color: #141923;
    font-family: Arial, sans-serif;
}}

#plot {{
    width: 100%;
    height: 550px;
}}

.controls {{
    text-align: center;
    margin-top: 5px;
}}

button {{
    font-size: 16px;
    padding: 8px 18px;
    margin: 4px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
}}

</style>

</head>

<body>

<div id="plot"></div>

<div class="controls">

<button onclick="playWave()">▶ Play</button>

<button onclick="pauseWave()">⏸ Pause</button>

<button onclick="resetWave()">↺ Reset</button>

</div>


<script>

// --------------------------------------------------
// Wave Parameters
// --------------------------------------------------

const amplitude = {amplitude};

const frequency = {frequency};

const wavelength = {wavelength};


// --------------------------------------------------
// Wave Configuration
// --------------------------------------------------

const numberOfPoints = 600;

const xMin = 0;

const xMax = 1200;


// --------------------------------------------------
// Create X Values
// --------------------------------------------------

const x = [];

for (let i = 0; i < numberOfPoints; i++) {{

    x.push(
        xMin +
        (xMax - xMin) *
        i / (numberOfPoints - 1)
    );

}}


// --------------------------------------------------
// Initial Wave
// --------------------------------------------------

let initialY = [];

for (let i = 0; i < x.length; i++) {{

    initialY.push(
        amplitude *
        Math.sin(
            2 * Math.PI * x[i] / wavelength
        )
    );

}}


// --------------------------------------------------
// Wave Trace
// --------------------------------------------------

const waveTrace = {{

    x: x,

    y: initialY,

    mode: "lines",

    line: {{

        width: 4

    }},

    name: "Wave"

}};


// --------------------------------------------------
// Equilibrium Line
// --------------------------------------------------

const equilibriumTrace = {{

    x: [xMin, xMax],

    y: [0, 0],

    mode: "lines",

    line: {{

        width: 2,

        dash: "dash"

    }},

    name: "Equilibrium"

}};


// --------------------------------------------------
// Particle Positions
// --------------------------------------------------

const particlePositions = [
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    1100
];


// --------------------------------------------------
// Particle Trace
// --------------------------------------------------

let particleY = [];

for (let i = 0; i < particlePositions.length; i++) {{

    particleY.push(

        amplitude *
        Math.sin(
            2 * Math.PI *
            particlePositions[i] /
            wavelength
        )

    );

}}


const particleTrace = {{

    x: particlePositions,

    y: particleY,

    mode: "markers",

    marker: {{

        size: 9

    }},

    name: "Particles"

}};


// --------------------------------------------------
// Plot Layout
// --------------------------------------------------

const layout = {{

    title: {{

        text: "Transverse Sinusoidal Wave",

        font: {{

            size: 22

        }}

    }},

    paper_bgcolor: "#141923",

    plot_bgcolor: "#141923",

    font: {{

        color: "#eeeeee"

    }},

    xaxis: {{

        title: "Position",

        range: [0, 1200],

        gridcolor: "#39404d",

        zeroline: false

    }},

    yaxis: {{

        title: "Displacement",

        range: [
            -amplitude * 1.3,
            amplitude * 1.3
        ],

        gridcolor: "#39404d",

        zeroline: false

    }},

    margin: {{

        l: 70,

        r: 30,

        t: 70,

        b: 60

    }},

    showlegend: true

}};


// --------------------------------------------------
// Create Plot
// --------------------------------------------------

Plotly.newPlot(

    "plot",

    [
        waveTrace,
        equilibriumTrace,
        particleTrace
    ],

    layout,

    {{

        responsive: true

    }}

);


// --------------------------------------------------
// Animation Variables
// --------------------------------------------------

let animationID = null;

let startTime = null;

let elapsedBeforePause = 0;

let isPlaying = true;


// --------------------------------------------------
// Animation Function
// --------------------------------------------------

function animateWave(timestamp) {{

    if (!isPlaying) {{

        return;

    }}


    if (startTime === null) {{

        startTime =
            timestamp -
            elapsedBeforePause * 1000;

    }}


    const elapsed =
        (timestamp - startTime) / 1000;


    // Phase

    const phase =
        2 *
        Math.PI *
        frequency *
        elapsed;


    // --------------------------------------------------
    // Calculate Wave
    // --------------------------------------------------

    const newY = [];

    for (let i = 0; i < x.length; i++) {{

        newY.push(

            amplitude *
            Math.sin(

                2 *
                Math.PI *
                x[i] /
                wavelength
                - phase

            )

        );

    }}


    // --------------------------------------------------
    // Calculate Particle Motion
    // --------------------------------------------------

    const newParticleY = [];

    for (
        let i = 0;
        i < particlePositions.length;
        i++
    ) {{

        newParticleY.push(

            amplitude *
            Math.sin(

                2 *
                Math.PI *
                particlePositions[i] /
                wavelength
                - phase

            )

        );

    }}


    // --------------------------------------------------
    // Update Plot
    // --------------------------------------------------

    Plotly.restyle(

        "plot",

        {{

            y: [newY]

        }},

        [0]

    );


    Plotly.restyle(

        "plot",

        {{

            y: [newParticleY]

        }},

        [2]

    );


    // --------------------------------------------------
    // Continue Forever
    // --------------------------------------------------

    animationID =
        requestAnimationFrame(animateWave);

}}


// --------------------------------------------------
// Play
// --------------------------------------------------

function playWave() {{

    if (isPlaying) {{

        return;

    }}


    isPlaying = true;

    startTime = null;

    animationID =
        requestAnimationFrame(animateWave);

}}


// --------------------------------------------------
// Pause
// --------------------------------------------------

function pauseWave() {{

    if (!isPlaying) {{

        return;

    }}


    isPlaying = false;

    cancelAnimationFrame(animationID);

    startTime =
        performance.now() -
        elapsedBeforePause * 1000;

}}


// --------------------------------------------------
// Reset
// --------------------------------------------------

function resetWave() {{

    cancelAnimationFrame(animationID);

    isPlaying = true;

    startTime = null;

    elapsedBeforePause = 0;

    const zeroY = [];

    for (let i = 0; i < x.length; i++) {{

        zeroY.push(

            amplitude *
            Math.sin(

                2 *
                Math.PI *
                x[i] /
                wavelength

            )

        );

    }}


    const zeroParticleY = [];

    for (
        let i = 0;
        i < particlePositions.length;
        i++
    ) {{

        zeroParticleY.push(

            amplitude *
            Math.sin(

                2 *
                Math.PI *
                particlePositions[i] /
                wavelength

            )

        );

    }}


    Plotly.restyle(

        "plot",

        {{ y: [zeroY] }},

        [0]

    );


    Plotly.restyle(

        "plot",

        {{ y: [zeroParticleY] }},

        [2]

    );


    animationID =
        requestAnimationFrame(animateWave);

}}


// --------------------------------------------------
// Start Automatically
// --------------------------------------------------

animationID =
    requestAnimationFrame(animateWave);

</script>

</body>

</html>
"""

# --------------------------------------------------
# Display Animation
# --------------------------------------------------

components.html(
    html_code,
    height=650,
    scrolling=False
)

# --------------------------------------------------
# Wave Properties
# --------------------------------------------------

st.subheader("Wave Properties")

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
# Additional Information
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.write("### Period")

    st.latex(
        r"T = \frac{1}{f}"
    )

    st.write(
        f"**T = {period:.2f} seconds**"
    )

with col2:

    st.write("### Wave Speed")

    st.latex(
        r"v = f\lambda"
    )

    st.write(
        f"**v = {wave_speed:.1f} px/s**"
    )

# --------------------------------------------------
# Wave Equation
# --------------------------------------------------

st.subheader("Wave Equation")

st.latex(
    r"""
    y(x,t)
    =
    A\sin
    \left(
    \frac{2\pi x}{\lambda}
    -
    2\pi ft
    \right)
    """
)