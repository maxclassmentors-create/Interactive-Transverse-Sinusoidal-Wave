import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Interactive Transverse Wave",
    page_icon="〰️",
    layout="wide"
)

st.title("〰️ Interactive Transverse Sinusoidal Wave")

st.write(
    "Explore the relationship between wave speed, frequency, "
    "wavelength, and amplitude."
)

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
    width: 120px;
    text-align: right;
    font-weight: bold;
}

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

#plot {
    width: 100%;
    height: 550px;
}

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
            min="0.1"
            max="2.0"
            value="1.0"
            step="0.01"
        >

        <div
            class="value"
            id="amplitudeValue"
        >
            1.00 m
        </div>

    </div>


    <!-- SPEED -->

    <div class="control-row">

        <label>
            Wave Speed
        </label>

        <input
            id="speedSlider"
            type="range"
            min="1"
            max="8"
            value="4"
            step="0.1"
        >

        <div
            class="value"
            id="speedValue"
        >
            4.0 m/s
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
            min="0.5"
            max="4.0"
            value="1.0"
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
            min="1"
            max="8"
            value="4"
            step="0.05"
        >

        <div
            class="value"
            id="wavelengthValue"
        >
            4.00 m
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

        Relationship Between Wave Speed, Frequency,
        and Wavelength

    </div>


    <div class="relationship-formula">

        v = f × λ

    </div>


    <div class="relationship-text">

        When wave speed is constant, frequency and wavelength
        are inversely proportional.

        <br><br>

        <strong>
        Increase frequency → wavelength decreases
        </strong>

        <br>

        <strong>
        Decrease frequency → wavelength increases
        </strong>

        <br><br>

        Changing wave speed changes the frequency and wavelength
        together while maintaining v = fλ.

    </div>


    <div class="live-values">

        Wave Speed:

        <span id="liveSpeed">
            4.00 m/s
        </span>

        &nbsp;&nbsp;|&nbsp;&nbsp;

        Frequency:

        <span id="liveFrequency">
            1.0 Hz
        </span>

        &nbsp;&nbsp;|&nbsp;&nbsp;

        Wavelength:

        <span id="liveWavelength">
            4.00 m
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
// PHYSICAL VARIABLES
// ==================================================

let amplitude = 1.0;

let frequency = 1.0;

let wavelength = 4.0;

let waveSpeed = 4.0;


// ==================================================
// CONSTANT SPEED MODE
// ==================================================

let constantWaveSpeed = true;


// ==================================================
// INITIAL FREQUENCY / WAVELENGTH RATIO
// ==================================================
//
// Initially:
//
// f = 1 Hz
// λ = 4 m
//
// Ratio:
//
// λ / f = 4
//
// This ratio is preserved when the speed slider
// changes so BOTH frequency and wavelength change.
//
// ==================================================

let wavelengthFrequencyRatio =

    wavelength / frequency;


// ==================================================
// FIXED Y AXIS
// ==================================================

const yAxisMin = -2.2;

const yAxisMax = 2.2;


// ==================================================
// X AXIS
// ==================================================

const numberOfPoints = 600;

const xMin = 0;

const xMax = 12;

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

    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11

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
// INITIAL TRACES
// ==================================================

const waveTrace = {

    x: x,

    y: calculateWave(0),

    mode: "lines",

    line: {
        width: 4
    },

    name: "Wave"

};


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


const particleTrace = {

    x: particlePositions,

    y: calculateParticles(0),

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

        title: "Position (m)",

        range: [
            xMin,
            xMax
        ],

        gridcolor: "#39404d",

        zeroline: false

    },

    yaxis: {

        title: "Displacement (m)",

        range: [
            yAxisMin,
            yAxisMax
        ],

        fixedrange: true,

        gridcolor: "#39404d",

        zeroline: false

    },

    margin: {

        l: 80,

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
// ANIMATION
// ==================================================

let animationID = null;

let lastTimestamp = null;

let elapsedTime = 0;

let isPlaying = true;


// ==================================================
// UPDATE DISPLAY
// ==================================================

function updateLiveValues() {

    document.getElementById(
        "liveSpeed"
    ).textContent =

        waveSpeed.toFixed(2)
        + " m/s";


    document.getElementById(
        "liveFrequency"
    ).textContent =

        frequency.toFixed(1)
        + " Hz";


    document.getElementById(
        "liveWavelength"
    ).textContent =

        wavelength.toFixed(2)
        + " m";

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


    // ----------------------------------------------
    // Time is measured in seconds
    // ----------------------------------------------

    elapsedTime += deltaTime;


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

            amplitude.toFixed(2)
            + " m";


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


        if (constantWaveSpeed) {

            // --------------------------------------
            // v = f × λ
            //
            // λ = v / f
            // --------------------------------------

            wavelength =

                waveSpeed /
                frequency;


            // Keep wavelength inside range

            wavelength = Math.max(
                1,
                Math.min(
                    8,
                    wavelength
                )
            );


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

            wavelength.toFixed(2)
            + " m";


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


        if (constantWaveSpeed) {

            // --------------------------------------
            // v = f × λ
            //
            // f = v / λ
            // --------------------------------------

            frequency =

                waveSpeed /
                wavelength;


            // Keep frequency inside range

            frequency = Math.max(
                0.5,
                Math.min(
                    4,
                    frequency
                )
            );


            frequencySlider.value =
                frequency;

        }


        document.getElementById(
            "wavelengthValue"
        ).textContent =

            wavelength.toFixed(2)
            + " m";


        document.getElementById(
            "frequencyValue"
        ).textContent =

            frequency.toFixed(1)
            + " Hz";


        updateWaveImmediately();

    }

);


// ==================================================
// SPEED SLIDER
// ==================================================

const speedSlider =

    document.getElementById(
        "speedSlider"
    );


speedSlider.addEventListener(

    "input",

    function() {

        waveSpeed =
            parseFloat(this.value);


        // ------------------------------------------
        // CHANGE BOTH FREQUENCY AND WAVELENGTH
        // ------------------------------------------
        //
        // We preserve their ratio while changing
        // the speed.
        //
        // v = f × λ
        //
        // Let:
        //
        // λ = R × f
        //
        // Therefore:
        //
        // v = R × f²
        //
        // so:
        //
        // f = √(v / R)
        //
        // λ = R × f
        //
        // ------------------------------------------

        const ratio =
            wavelengthFrequencyRatio;


        frequency =

            Math.sqrt(
                waveSpeed /
                ratio
            );


        wavelength =

            ratio *
            frequency;


        // ------------------------------------------
        // Update both sliders immediately
        // ------------------------------------------

        frequencySlider.value =
            frequency;


        wavelengthSlider.value =
            wavelength;


        // ------------------------------------------
        // Update displayed values
        // ------------------------------------------

        document.getElementById(
            "speedValue"
        ).textContent =

            waveSpeed.toFixed(1)
            + " m/s";


        document.getElementById(
            "frequencyValue"
        ).textContent =

            frequency.toFixed(2)
            + " Hz";


        document.getElementById(
            "wavelengthValue"
        ).textContent =

            wavelength.toFixed(2)
            + " m";


        updateWaveImmediately();

    }

);


// ==================================================
// CONSTANT SPEED CHECKBOX
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

            // --------------------------------------
            // Current speed is preserved.
            //
            // Adjust wavelength to match
            // current frequency.
            // --------------------------------------

            wavelength =

                waveSpeed /
                frequency;


            wavelength = Math.max(
                1,
                Math.min(
                    8,
                    wavelength
                );


            wavelengthSlider.value =
                wavelength;


            document.getElementById(
                "wavelengthValue"
            ).textContent =

                wavelength.toFixed(2)
                + " m";


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

components.html(
    html_code,
    height=850,
    scrolling=False
)