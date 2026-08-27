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
    "Explore the relationship between amplitude, frequency, "
    "wavelength, and wave speed."
)

# --------------------------------------------------
# Plotly + JavaScript Application
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

    width: 180px;

    font-size: 16px;

    flex-shrink: 0;

}


input[type="range"] {

    flex: 1;

    cursor: pointer;

}


.value {

    width: 110px;

    text-align: right;

    font-weight: bold;

}


/* ==================================================
   TOGGLE
================================================== */

.toggle-row {

    display: flex;

    align-items: center;

    gap: 10px;

    margin-top: 10px;

}


.toggle-row label {

    width: auto;

}


.toggle-row input {

    width: 18px;

    height: 18px;

    cursor: pointer;

}


/* ==================================================
   RELATIONSHIP BOX
================================================== */

.relationship {

    background-color: #202736;

    border-radius: 10px;

    padding: 15px 20px;

    margin-bottom: 12px;

    text-align: center;

}


.relationship-title {

    font-size: 19px;

    font-weight: bold;

    margin-bottom: 8px;

}


.relationship-formula {

    font-size: 28px;

    font-weight: bold;

    margin-bottom: 8px;

}


.relationship-text {

    font-size: 15px;

    line-height: 1.6;

    color: #dddddd;

}


.live-values {

    margin-top: 10px;

    font-size: 17px;

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
     CONTROLS
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


    <!-- CONSTANT SPEED -->

    <div class="toggle-row">

        <input
            id="constantSpeed"
            type="checkbox"
            checked
        >

        <label>
            Keep Wave Speed Constant
        </label>

    </div>

</div>


<!-- ==================================================
     RELATIONSHIP
================================================== -->

<div class="relationship">

    <div class="relationship-title">

        Wave Speed, Frequency, and Wavelength

    </div>


    <div class="relationship-formula">

        v = f × λ

    </div>


    <div class="relationship-text">

        When wave speed is constant, frequency and wavelength
        are inversely proportional.

        <br>

        <strong>
        Increase frequency → wavelength decreases
        </strong>

        <br>

        <strong>
        Decrease frequency → wavelength increases
        </strong>

    </div>


    <div class="live-values">

        Wave Speed:

        <span id="liveSpeed">
            400 px/s
        </span>

        &nbsp;&nbsp;|&nbsp;&nbsp;

        Frequency:

        <span id="liveFrequency">
            1.0 Hz
        </span>

        &nbsp;&nbsp;|&nbsp;&nbsp;

        Wavelength:

        <span id="liveWavelength">
            400 px
        </span>

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
// PARAMETERS
// ==================================================

let amplitude = 100;

let frequency = 1.0;

let wavelength = 400;

let animationSpeed = 1.0;


// ==================================================
// CONSTANT WAVE SPEED
// ==================================================

let constantWaveSpeed = true;

// Initial speed:
//
// v = f × λ
//
// v = 1 × 400
//
// v = 400 px/s

const fixedWaveSpeed = 400;


// ==================================================
// FIXED Y-AXIS
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
// PARTICLES
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
// INITIAL VALUES
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
// EQUILIBRIUM
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
// PARTICLES
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
// LAYOUT
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

        // IMPORTANT:
        // Fixed so amplitude changes are visible.

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
// UPDATE LIVE VALUES
// ==================================================

function updateLiveValues() {

    const speed =
        frequency *
        wavelength;


    document.getElementById(
        "liveSpeed"
    ).textContent =

        speed.toFixed(1)
        + " px/s";


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

}


// ==================================================
// UPDATE WAVE
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


    updateLiveValues();

}


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


    elapsedTime +=

        deltaTime *

        animationSpeed;


    updateWaveImmediately();


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


        // ------------------------------------------
        // CONSTANT SPEED MODE
        // ------------------------------------------

        if (constantWaveSpeed) {

            wavelength =

                fixedWaveSpeed /
                frequency;


            // Keep wavelength inside slider range

            wavelength = Math.max(
                100,
                Math.min(
                    800,
                    wavelength
                )
            );


            // Update wavelength slider

            wavelengthSlider.value =
                wavelength;

        }


        document.getElementById(
            "frequencyValue"
        ).textContent =

            frequency.toFixed(1)
            + " Hz";


        document.getElementById(
            "wavelengthValue"
        ).textContent =

            wavelength.toFixed(0)
            + " px";


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

        wavelength =
            parseFloat(this.value);


        // ------------------------------------------
        // CONSTANT SPEED MODE
        // ------------------------------------------

        if (constantWaveSpeed) {

            frequency =

                fixedWaveSpeed /
                wavelength;


            // Keep frequency inside slider range

            frequency = Math.max(
                0.1,
                Math.min(
                    5,
                    frequency
                )
            );


            // Update frequency slider

            frequencySlider.value =
                frequency;

        }


        document.getElementById(
            "wavelengthValue"
        ).textContent =

            wavelength.toFixed(0)
            + " px";


        document.getElementById(
            "frequencyValue"
        ).textContent =

            frequency.toFixed(1)
            + " Hz";


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
// CONSTANT SPEED TOGGLE
// ==================================================

const constantSpeedCheckbox =

    document.getElementById(
        "constantSpeed"
    );


constantSpeedCheckbox.addEventListener(

    "change",

    function() {

        constantWaveSpeed =
            this.checked;


        if (constantWaveSpeed) {

            // Recalculate wavelength
            // from the current frequency

            wavelength =

                fixedWaveSpeed /
                frequency;


            wavelength = Math.max(
                100,
                Math.min(
                    800,
                    wavelength
                )
            );


            wavelengthSlider.value =
                wavelength;


            document.getElementById(
                "wavelengthValue"
            ).textContent =

                wavelength.toFixed(0)
                + " px";


            updateWaveImmediately();

        }

    }

);


// ==================================================
// INITIALIZE
// ==================================================

updateLiveValues();

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
    height=850,
    scrolling=False
)