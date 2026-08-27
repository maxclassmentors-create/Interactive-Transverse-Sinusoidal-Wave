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
    "Adjust the amplitude, frequency, wavelength, and "
    "animation speed using the controls below."
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

/* ==================================================
   GENERAL
================================================== */

body {
    margin: 0;
    background-color: #141923;
    color: #eeeeee;
    font-family: Arial, sans-serif;
}


/* ==================================================
   CONTROL PANEL
================================================== */

.control-panel {

    background-color: #1d2330;

    padding: 18px 22px;

    border-radius: 10px;

    margin-bottom: 12px;

}


.control-row {

    display: flex;

    align-items: center;

    gap: 15px;

    margin-bottom: 14px;

}


.control-row:last-child {

    margin-bottom: 0;

}


label {

    width: 170px;

    font-size: 16px;

    flex-shrink: 0;

}


input[type="range"] {

    flex: 1;

    cursor: pointer;

}


.value {

    width: 100px;

    text-align: right;

    font-weight: bold;

}


/* ==================================================
   WAVE RELATIONSHIP
================================================== */

.relationship {

    background-color: #202736;

    border-radius: 10px;

    padding: 14px 20px;

    margin-bottom: 12px;

    text-align: center;

}


.relationship-title {

    font-size: 18px;

    font-weight: bold;

    margin-bottom: 8px;

}


.relationship-formula {

    font-size: 26px;

    font-weight: bold;

    margin-bottom: 8px;

}


.relationship-text {

    font-size: 15px;

    line-height: 1.5;

    color: #dddddd;

}


/* ==================================================
   LIVE VALUES
================================================== */

.live-values {

    text-align: center;

    font-size: 16px;

    margin-top: 8px;

}


.live-values span {

    font-weight: bold;

}


/* ==================================================
   PLOT
================================================== */

#plot {

    width: 100%;

    height: 550px;

}


/* ==================================================
   BUTTONS
================================================== */

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


    <!-- WAVELENGTH -->

    <div class="control-row">

        <label>
            Wavelength
        </label>

        <input
            id="wavelengthSlider"
            type="range"
            min="100"
            max="800"
            value="400"
            step="5"
        >

        <div
            class="value"
            id="wavelengthValue"
        >
            400 px
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
     SPEED / FREQUENCY / WAVELENGTH RELATIONSHIP
================================================== -->

<div class="relationship">

    <div class="relationship-title">
        Relationship Between Wave Speed, Frequency, and Wavelength
    </div>

    <div class="relationship-formula">
        v = f × λ
    </div>

    <div class="relationship-text">

        Wave speed is directly proportional to frequency
        when wavelength is constant, and directly proportional
        to wavelength when frequency is constant.

        <br>

        Increasing frequency or wavelength increases wave speed.

    </div>

    <div class="live-values">

        Current:
        <span id="liveFrequency">1.0 Hz</span>
        ×
        <span id="liveWavelength">400 px</span>
        =
        <span id="liveSpeed">400 px/s</span>

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
// WAVE PARAMETERS
// ==================================================

let amplitude = 100;

let frequency = 1.0;

let wavelength = 400;

let animationSpeed = 1.0;


// ==================================================
// FIXED Y-AXIS
// ==================================================

const yAxisMin = -220;

const yAxisMax = 220;


// ==================================================
// X AXIS
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
// CALCULATE WAVE
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
// CALCULATE PARTICLES
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


    const deltaTime =

        (timestamp - lastTimestamp) /

        1000;


    lastTimestamp = timestamp;


    // ----------------------------------------------
    // Animation speed
    // ----------------------------------------------

    elapsedTime +=

        deltaTime *

        animationSpeed;


    // ----------------------------------------------
    // Calculate wave
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
// UPDATE WAVE IMMEDIATELY
// ==================================================

function updateWaveImmediately() {

    const newWave =
        calculateWave(elapsedTime);

    const newParticles =
        calculateParticles(elapsedTime);


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


// ==================================================
// UPDATE LIVE SPEED DISPLAY
// ==================================================

function updateSpeedDisplay() {

    const speed =
        frequency *
        wavelength;


    document.getElementById(
        "liveFrequency"
    ).textContent =
        frequency.toFixed(1)
        + " Hz";


    document.getElementById(
        "liveWavelength"
    ).textContent =
        wavelength.toFixed(0)
        + " px";


    document.getElementById(
        "liveSpeed"
    ).textContent =
        speed.toFixed(1)
        + " px/s";

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

    updateWaveImmediately();

}


// ==================================================
// AMPLITUDE SLIDER
// ==================================================

const amplitudeSlider =

    document.getElementById(
        "amplitudeSlider"
    );


amplitudeSlider.addEventListener(
    "input",
    function() {

        amplitude =
            parseFloat(this.value);


        document.getElementById(
            "amplitudeValue"
        ).textContent =

            amplitude.toFixed(0)
            + " px";


        // Immediately update

        updateWaveImmediately();

    }
);


// ==================================================
// FREQUENCY SLIDER
// ==================================================

const frequencySlider =

    document.getElementById(
        "frequencySlider"
    );


frequencySlider.addEventListener(
    "input",
    function() {

        frequency =
            parseFloat(this.value);


        document.getElementById(
            "frequencyValue"
        ).textContent =

            frequency.toFixed(1)
            + " Hz";


        // Update speed relationship

        updateSpeedDisplay();

        // Immediately update wave

        updateWaveImmediately();

    }
);


// ==================================================
// WAVELENGTH SLIDER
// ==================================================

const wavelengthSlider =

    document.getElementById(
        "wavelengthSlider"
    );


wavelengthSlider.addEventListener(
    "input",
    function() {

        // ------------------------------------------
        // Update wavelength in REAL TIME
        // ------------------------------------------

        wavelength =
            parseFloat(this.value);


        document.getElementById(
            "wavelengthValue"
        ).textContent =

            wavelength.toFixed(0)
            + " px";


        // ------------------------------------------
        // Update speed immediately
        // ------------------------------------------

        updateSpeedDisplay();


        // ------------------------------------------
        // Redraw wave immediately
        // ------------------------------------------

        updateWaveImmediately();

    }
);


// ==================================================
// ANIMATION SPEED SLIDER
// ==================================================

const speedSlider =

    document.getElementById(
        "speedSlider"
    );


speedSlider.addEventListener(
    "input",
    function() {

        animationSpeed =
            parseFloat(this.value);


        document.getElementById(
            "speedValue"
        ).textContent =

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


// ==================================================
// INITIAL SPEED DISPLAY
// ==================================================

updateSpeedDisplay();

</script>

</body>

</html>
"""

# --------------------------------------------------
# Display App
# --------------------------------------------------

components.html(
    html_code,
    height=850,
    scrolling=False
)