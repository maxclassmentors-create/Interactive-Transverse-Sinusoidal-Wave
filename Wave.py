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

st.title("〰️ Interactive Transverse Sinusoidal Wave")

st.write(
    "Adjust the sliders in real time to change the amplitude, "
    "frequency, and animation speed."
)

# --------------------------------------------------
# HTML / JavaScript / Plotly
# --------------------------------------------------

html_code = """
<!DOCTYPE html>

<html>

<head>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>

body {
    margin: 0;
    background-color: #141923;
    color: #eeeeee;
    font-family: Arial, sans-serif;
}

/* -----------------------------------------------
   Controls
------------------------------------------------ */

.control-panel {
    background-color: #1d2330;
    padding: 15px 20px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.control-row {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 12px;
}

.control-row:last-child {
    margin-bottom: 0;
}

label {
    width: 170px;
    font-size: 16px;
}

input[type="range"] {
    flex: 1;
    cursor: pointer;
}

.value {
    width: 80px;
    text-align: right;
    font-weight: bold;
}

/* -----------------------------------------------
   Buttons
------------------------------------------------ */

.buttons {
    text-align: center;
    margin-top: 5px;
}

button {
    font-size: 16px;
    padding: 8px 18px;
    margin: 4px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
}

/* -----------------------------------------------
   Plot
------------------------------------------------ */

#plot {
    width: 100%;
    height: 550px;
}

</style>

</head>


<body>


<!-- ==================================================
     CONTROL PANEL
================================================== -->

<div class="control-panel">


    <!-- AMPLITUDE -->

    <div class="control-row">

        <label>
            Amplitude
        </label>

        <input
            id="amplitudeSlider"
            type="range"
            min="20"
            max="200"
            value="100"
            step="1"
        >

        <div
            class="value"
            id="amplitudeValue"
        >
            100 px
        </div>

    </div>


    <!-- FREQUENCY -->

    <div class="control-row">

        <label>
            Frequency
        </label>

        <input
            id="frequencySlider"
            type="range"
            min="0.1"
            max="5"
            value="1"
            step="0.1"
        >

        <div
            class="value"
            id="frequencyValue"
        >
            1.0 Hz
        </div>

    </div>


    <!-- ANIMATION SPEED -->

    <div class="control-row">

        <label>
            Animation Speed
        </label>

        <input
            id="speedSlider"
            type="range"
            min="0.1"
            max="3"
            value="1"
            step="0.1"
        >

        <div
            class="value"
            id="speedValue"
        >
            1.0×
        </div>

    </div>

</div>


<!-- ==================================================
     PLOT
================================================== -->

<div id="plot"></div>


<!-- ==================================================
     BUTTONS
================================================== -->

<div class="buttons">

    <button onclick="playWave()">
        ▶ Play
    </button>

    <button onclick="pauseWave()">
        ⏸ Pause
    </button>

    <button onclick="resetWave()">
        ↺ Reset
    </button>

</div>


<script>

// ==================================================
// INITIAL PARAMETERS
// ==================================================

let amplitude = 100;

let frequency = 1.0;

let animationSpeed = 1.0;

const wavelength = 400;


// ==================================================
// FIXED Y-AXIS RANGE
// ==================================================
//
// IMPORTANT:
//
// This does NOT change when amplitude changes.
//
// Therefore:
//
// A = 50  -> small wave
//
// A = 100 -> medium wave
//
// A = 200 -> large wave
//
// ==================================================

const yAxisMin = -220;

const yAxisMax = 220;


// ==================================================
// X VALUES
// ==================================================

const numberOfPoints = 600;

const xMin = 0;

const xMax = 1200;

const x = [];

for (
    let i = 0;
    i < numberOfPoints;
    i++
) {

    x.push(
        xMin +
        (xMax - xMin) *
        i /
        (numberOfPoints - 1)
    );

}


// ==================================================
// PARTICLE POSITIONS
// ==================================================
//
// These NEVER change horizontally.
//
// They only move vertically.
//

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


// ==================================================
// CREATE INITIAL WAVE
// ==================================================

function calculateWave(t) {

    const y = [];

    const phase =
        2 *
        Math.PI *
        frequency *
        t;

    for (
        let i = 0;
        i < x.length;
        i++
    ) {

        y.push(

            amplitude *
            Math.sin(

                2 *
                Math.PI *
                x[i] /
                wavelength
                -
                phase

            )

        );

    }

    return y;

}


// ==================================================
// CREATE PARTICLE POSITIONS
// ==================================================

function calculateParticles(t) {

    const y = [];

    const phase =
        2 *
        Math.PI *
        frequency *
        t;

    for (
        let i = 0;
        i < particlePositions.length;
        i++
    ) {

        y.push(

            amplitude *
            Math.sin(

                2 *
                Math.PI *
                particlePositions[i] /
                wavelength
                -
                phase

            )

        );

    }

    return y;

}


// ==================================================
// INITIAL DATA
// ==================================================

const initialWave =
    calculateWave(0);

const initialParticles =
    calculateParticles(0);


// ==================================================
// WAVE TRACE
// ==================================================

const waveTrace = {

    x: x,

    y: initialWave,

    mode: "lines",

    line: {
        width: 4
    },

    name: "Wave"

};


// ==================================================
// EQUILIBRIUM LINE
// ==================================================

const equilibriumTrace = {

    x: [xMin, xMax],

    y: [0, 0],

    mode: "lines",

    line: {
        width: 2,
        dash: "dash"
    },

    name: "Equilibrium"

};


// ==================================================
// PARTICLE TRACE
// ==================================================

const particleTrace = {

    x: particlePositions,

    y: initialParticles,

    mode: "markers",

    marker: {
        size: 10
    },

    name: "Particles"

};


// ==================================================
// PLOT LAYOUT
// ==================================================

const layout = {

    title: {

        text: "Transverse Sinusoidal Wave",

        font: {
            size: 22
        }

    },

    paper_bgcolor: "#141923",

    plot_bgcolor: "#141923",

    font: {
        color: "#eeeeee"
    },

    xaxis: {

        title: "Position",

        range: [
            xMin,
            xMax
        ],

        gridcolor: "#39404d",

        zeroline: false

    },

    yaxis: {

        title: "Displacement",

        // ------------------------------------------
        // FIXED RANGE
        // ------------------------------------------

        range: [
            yAxisMin,
            yAxisMax
        ],

        fixedrange: true,

        gridcolor: "#39404d",

        zeroline: false

    },

    margin: {

        l: 70,

        r: 30,

        t: 70,

        b: 60

    },

    showlegend: true

};


// ==================================================
// CREATE PLOT
// ==================================================

Plotly.newPlot(

    "plot",

    [
        waveTrace,
        equilibriumTrace,
        particleTrace
    ],

    layout,

    {
        responsive: true
    }

);


// ==================================================
// ANIMATION VARIABLES
// ==================================================

let animationID = null;

let lastTimestamp = null;

let elapsedTime = 0;

let isPlaying = true;


// ==================================================
// ANIMATION LOOP
// ==================================================

function animateWave(timestamp) {

    if (!isPlaying) {

        return;

    }


    if (lastTimestamp === null) {

        lastTimestamp = timestamp;

    }


    // ----------------------------------------------
    // Calculate elapsed real time
    // ----------------------------------------------

    const deltaTime =
        (timestamp - lastTimestamp) /
        1000;


    lastTimestamp = timestamp;


    // ----------------------------------------------
    // Apply animation-speed multiplier
    // ----------------------------------------------

    elapsedTime +=
        deltaTime *
        animationSpeed;


    // ----------------------------------------------
    // Calculate new wave
    // ----------------------------------------------

    const newWave =
        calculateWave(elapsedTime);


    const newParticles =
        calculateParticles(elapsedTime);


    // ----------------------------------------------
    // Update wave
    // ----------------------------------------------

    Plotly.restyle(

        "plot",

        {
            y: [newWave]
        },

        [0]

    );


    // ----------------------------------------------
    // Update particles
    // ----------------------------------------------

    Plotly.restyle(

        "plot",

        {
            y: [newParticles]
        },

        [2]

    );


    // ----------------------------------------------
    // Continue forever
    // ----------------------------------------------

    animationID =
        requestAnimationFrame(
            animateWave
        );

}


// ==================================================
// PLAY
// ==================================================

function playWave() {

    if (isPlaying) {

        return;

    }

    isPlaying = true;

    lastTimestamp = null;

    animationID =
        requestAnimationFrame(
            animateWave
        );

}


// ==================================================
// PAUSE
// ==================================================

function pauseWave() {

    if (!isPlaying) {

        return;

    }

    isPlaying = false;

    cancelAnimationFrame(
        animationID
    );

}


// ==================================================
// RESET
// ==================================================

function resetWave() {

    elapsedTime = 0;

    lastTimestamp = null;


    const resetWave =
        calculateWave(0);


    const resetParticles =
        calculateParticles(0);


    Plotly.restyle(

        "plot",

        {
            y: [resetWave]
        },

        [0]

    );


    Plotly.restyle(

        "plot",

        {
            y: [resetParticles]
        },

        [2]

    );

}


// ==================================================
// AMPLITUDE SLIDER
// ==================================================

const amplitudeSlider =
    document.getElementById(
        "amplitudeSlider"
    );

const amplitudeValue =
    document.getElementById(
        "amplitudeValue"
    );


amplitudeSlider.addEventListener(
    "input",
    function() {

        // ------------------------------------------
        // Update amplitude IMMEDIATELY
        // ------------------------------------------

        amplitude =
            parseFloat(
                this.value
            );


        amplitudeValue.textContent =
            amplitude.toFixed(0)
            + " px";


        // ------------------------------------------
        // Immediately redraw wave
        // ------------------------------------------

        const newWave =
            calculateWave(
                elapsedTime
            );


        const newParticles =
            calculateParticles(
                elapsedTime
            );


        Plotly.restyle(

            "plot",

            {
                y: [newWave]
            },

            [0]

        );


        Plotly.restyle(

            "plot",

            {
                y: [newParticles]
            },

            [2]

        );

    }

);


// ==================================================
// FREQUENCY SLIDER
// ==================================================

const frequencySlider =
    document.getElementById(
        "frequencySlider"
    );

const frequencyValue =
    document.getElementById(
        "frequencyValue"
    );


frequencySlider.addEventListener(
    "input",
    function() {

        // ------------------------------------------
        // Update frequency IMMEDIATELY
        // ------------------------------------------

        frequency =
            parseFloat(
                this.value
            );


        frequencyValue.textContent =
            frequency.toFixed(1)
            + " Hz";

    }

);


// ==================================================
// ANIMATION SPEED SLIDER
// ==================================================

const speedSlider =
    document.getElementById(
        "speedSlider"
    );

const speedValue =
    document.getElementById(
        "speedValue"
    );


speedSlider.addEventListener(
    "input",
    function() {

        // ------------------------------------------
        // Update animation speed IMMEDIATELY
        // ------------------------------------------

        animationSpeed =
            parseFloat(
                this.value
            );


        speedValue.textContent =
            animationSpeed.toFixed(1)
            + "×";

    }

);


// ==================================================
// START ANIMATION
// ==================================================

animationID =
    requestAnimationFrame(
        animateWave
    );

</script>

</body>

</html>
"""

# --------------------------------------------------
# Display Application
# --------------------------------------------------

components.html(
    html_code,
    height=750,
    scrolling=False
)