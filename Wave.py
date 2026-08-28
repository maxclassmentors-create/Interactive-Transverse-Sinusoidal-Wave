import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Interactive Transverse Wave",
    page_icon="〰️",
    layout="wide"
)

st.title("〰️ Interactive Transverse Sinusoidal Wave")

st.write(
    "Adjust the amplitude, wave speed, frequency, and wavelength "
    "to explore the relationship between wave properties."
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


/* ==================================================
   SLIDER PANEL
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


.control-label {

    width: 70px;

    font-size: 20px;

    font-weight: bold;

    text-align: center;

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
   PLOT
================================================== */

#plot {

    width: 100%;

    height: 600px;

}


/* ==================================================
   INFORMATION UNDER ANIMATION
================================================== */

.relationship {

    background-color: #202736;

    border-radius: 10px;

    padding: 20px;

    margin-top: 12px;

    text-align: center;

}


.formula {

    font-size: 30px;

    font-weight: bold;

    margin-bottom: 12px;

}


.live-values {

    font-size: 18px;

    margin-bottom: 18px;

}


.live-values span {

    font-weight: bold;

}


.info-title {

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 10px;

}


.info-text {

    font-size: 16px;

    line-height: 1.7;

}


.info-text strong {

    display: block;

}


/* ==================================================
   BUTTONS
================================================== */

.buttons {

    text-align: center;

    margin-top: 8px;

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
     SLIDERS
================================================== -->

<div class="control-panel">


    <!-- AMPLITUDE -->

    <div class="control-row">

        <div class="control-label">
            A
        </div>

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


    <!-- WAVE SPEED -->

    <div class="control-row">

        <div class="control-label">
            v
        </div>

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

        <div class="control-label">
            f
        </div>

        <input
            id="frequencySlider"
            type="range"
            min="0.5"
            max="4.0"
            value="1.0"
            step="0.01"
        >

        <div
            class="value"
            id="frequencyValue"
        >
            1.00 Hz
        </div>

    </div>


    <!-- WAVELENGTH -->

    <div class="control-row">

        <div class="control-label">
            λ
        </div>

        <input
            id="wavelengthSlider"
            type="range"
            min="1"
            max="8"
            value="4"
            step="0.01"
        >

        <div
            class="value"
            id="wavelengthValue"
        >
            4.00 m
        </div>

    </div>

</div>


<!-- ==================================================
     ANIMATION
================================================== -->

<div id="plot"></div>


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


<!-- ==================================================
     INFORMATION BELOW ANIMATION
================================================== -->

<div class="relationship">


    <div class="formula">

        v = f × λ

    </div>


    <div class="live-values">

        <span id="liveSpeed">
            4.00 m/s
        </span>

        &nbsp;&nbsp;=&nbsp;&nbsp;

        <span id="liveFrequency">
            1.00 Hz
        </span>

        ×

        <span id="liveWavelength">
            4.00 m
        </span>

    </div>


    <div class="info-title">

        Wave Speed, Frequency, and Wavelength

    </div>


    <div class="info-text">

        When wave speed is constant, frequency and wavelength
        are inversely proportional.

        <br>

        <strong>
            Increase frequency → wavelength decreases
        </strong>

        <strong>
            Decrease frequency → wavelength increases
        </strong>

        <br>

        Changing the wave speed adjusts the frequency and
        wavelength while maintaining:

        <strong>
            v = f × λ
        </strong>

    </div>

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
// FREQUENCY / WAVELENGTH RATIO
// ==================================================
//
// Initially:
//
// f = 1 Hz
// λ = 4 m
//
// λ / f = 4
//
// When the speed changes, this ratio is preserved.
// This causes BOTH f and λ to change while:
//
// v = fλ
//
// remains true.
//
// ==================================================

let wavelengthFrequencyRatio =
    wavelength / frequency;


// ==================================================
// FIXED GRAPH RANGES
// ==================================================

const xMin = 0;

const xMax = 12;


// IMPORTANT:
// Symmetric amplitude range:
//
// -2 m to +2 m
//

const yAxisMin = -2.0;

const yAxisMax = 2.0;


// ==================================================
// X VALUES
// ==================================================

const numberOfPoints = 700;

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
// WAVE EQUATION
// ==================================================
//
// y(x,t) = A sin(2πx/λ - 2πft)
//
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
// PARTICLES
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
// WAVELENGTH SCALE
// ==================================================
//
// Finds two neighboring crests and draws a scale
// between them.
//
// ==================================================

function getWavelengthScale(t) {

    let phaseDistance =

        (waveSpeed * t) % wavelength;


    // First crest position

    let firstCrest =

        wavelength / 4 +

        phaseDistance;


    // Move into visible graph range

    while (
        firstCrest < xMin
    ) {

        firstCrest += wavelength;

    }


    while (
        firstCrest > xMax
    ) {

        firstCrest -= wavelength;

    }


    let secondCrest =

        firstCrest + wavelength;


    // If the second crest is outside the graph,
    // move both one wavelength to the left.

    while (
        secondCrest > xMax
    ) {

        firstCrest -= wavelength;

        secondCrest -= wavelength;

    }


    return {

        x1: firstCrest,

        x2: secondCrest

    };

}


// ==================================================
// INITIAL WAVELENGTH SCALE
// ==================================================

const initialScale =
    getWavelengthScale(0);


// ==================================================
// WAVE TRACE
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

    y: calculateParticles(0),

    mode: "markers",

    marker: {
        size: 10
    },

    name: "Particles"

};


// ==================================================
// WAVELENGTH SCALE TRACE
// ==================================================

const wavelengthScaleTrace = {

    x: [
        initialScale.x1,
        initialScale.x2
    ],

    y: [
        1.72,
        1.72
    ],

    mode: "lines+markers",

    line: {
        width: 3
    },

    marker: {

        size: 9,

        symbol: [
            "triangle-left",
            "triangle-right"
        ]

    },

    name: "Wavelength"

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

        // ------------------------------------------
        // SYMMETRIC Y-AXIS
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

        l: 80,

        r: 30,

        t: 70,

        b: 60

    },


    showlegend: true,


    // ----------------------------------------------
    // WAVELENGTH LABEL
    // ----------------------------------------------

    annotations: [

        {

            x:
                (initialScale.x1 +
                initialScale.x2) / 2,

            y: 1.87,

            text:
                "λ = " +
                wavelength.toFixed(2) +
                " m",

            showarrow: false,

            font: {
                size: 16
            }

        }

    ]

};


// ==================================================
// CREATE PLOT
// ==================================================

Plotly.newPlot(

    "plot",

    [
        waveTrace,
        equilibriumTrace,
        particleTrace,
        wavelengthScaleTrace
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
// UPDATE LIVE DATA
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

        frequency.toFixed(2)
        + " Hz";


    document.getElementById(
        "liveWavelength"
    ).textContent =

        wavelength.toFixed(2)
        + " m";

}


// ==================================================
// UPDATE WAVELENGTH SCALE
// ==================================================

function updateWavelengthScale() {

    const scale =
        getWavelengthScale(elapsedTime);


    // Update horizontal scale

    Plotly.restyle(

        "plot",

        {

            x: [[
                scale.x1,
                scale.x2
            ]]

        },

        [3]

    );


    // Update wavelength label

    Plotly.relayout(

        "plot",

        {

            "annotations[0].x":

                (scale.x1 +
                scale.x2) / 2,

            "annotations[0].y":
                1.87,

            "annotations[0].text":

                "λ = " +
                wavelength.toFixed(2) +
                " m"

        }

    );

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


    updateWavelengthScale();

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


    // Time is measured in seconds.

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


        // ------------------------------------------
        // Constant speed relationship
        //
        // v = fλ
        //
        // λ = v/f
        // ------------------------------------------

        wavelength =

            waveSpeed /
            frequency;


        // Keep wavelength inside slider limits

        wavelength = Math.max(
            1,
            Math.min(
                8,
                wavelength
            )
        );


        wavelengthSlider.value =
            wavelength;


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
        // Constant speed relationship
        //
        // v = fλ
        //
        // f = v/λ
        // ------------------------------------------

        frequency =

            waveSpeed /
            wavelength;


        // Keep frequency inside slider limits

        frequency = Math.max(
            0.5,
            Math.min(
                4,
                frequency
            )
        );


        frequencySlider.value =
            frequency;


        document.getElementById(
            "wavelengthValue"
        ).textContent =

            wavelength.toFixed(2)
            + " m";


        document.getElementById(
            "frequencyValue"
        ).textContent =

            frequency.toFixed(2)
            + " Hz";


        updateWaveImmediately();

    }

);


// ==================================================
// WAVE SPEED SLIDER
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
        // CHANGE BOTH f AND λ
        // ------------------------------------------
        //
        // We preserve the current λ/f ratio.
        //
        // λ = Rf
        //
        // v = fλ
        //
        // v = Rf²
        //
        // f = √(v/R)
        //
        // λ = Rf
        //
        // Therefore BOTH values change while:
        //
        // v = fλ
        //
        // remains exactly consistent.
        // ------------------------------------------

        frequency =

            Math.sqrt(

                waveSpeed /
                wavelengthFrequencyRatio

            );


        wavelength =

            wavelengthFrequencyRatio *
            frequency;


        // ------------------------------------------
        // Keep values within slider limits
        // ------------------------------------------

        if (
            frequency > 4
        ) {

            frequency = 4;

            wavelength =
                waveSpeed /
                frequency;

        }


        if (
            frequency < 0.5
        ) {

            frequency = 0.5;

            wavelength =
                waveSpeed /
                frequency;

        }


        if (
            wavelength > 8
        ) {

            wavelength = 8;

            frequency =
                waveSpeed /
                wavelength;

        }


        if (
            wavelength < 1
        ) {

            wavelength = 1;

            frequency =
                waveSpeed /
                wavelength;

        }


        // ------------------------------------------
        // Update both sliders in real time
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

            waveSpeed.toFixed(2)
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
// INITIALIZE
// ==================================================

document.getElementById(
    "amplitudeValue"
).textContent =

    amplitude.toFixed(2)
    + " m";


document.getElementById(
    "speedValue"
).textContent =

    waveSpeed.toFixed(2)
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
    height=1050,
    scrolling=False
)