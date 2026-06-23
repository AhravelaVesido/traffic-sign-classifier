// Wait for the page to fully load before running any code
document.addEventListener('DOMContentLoaded', function() {
 // Get all the elemnts we need from HTML
 const viewfinder = document.getElementById('viewfinder')
 const cameraBtn = document.getElementById('camera-btn')
 const uploadBtn = document.getElementById('upload-btn')
 const fileInput = document.getElementById('file-input')
 const resultCard = document.getElementById('result-card')
 const resultLabel = document.getElementById('result-label')
 const resultConf = document.getElementById('result-conf')
 const barLabel = document.getElementById('bar-label')
 const barFill = document.getElementById('bar-fill')
 const barPercent = document.getElementById('bar-percent')
 const ledRow = document.getElementById('led-row')
 const ledR = document.getElementById('led-r')
 const ledG = document.getElementById('led-g')
 const ledB = document.getElementById('led-b')
 const ledText = document.getElementById('led-text')
 

 //When upload button is clicked it triggers file input
 uploadBtn.addEventListener('click', function() {
    fileInput.click()
 })

 // Opens the devcice's camera once camera button is clicked
 cameraBtn.addEventListener('click', function() {
    if (/Mobi|Android/i.test(navigator.userAgent)) {
        // If the user is on mobile, opens a camera
        fileInput.setAttribute('capture', 'environment')
        fileInput.click()
    } else {
        // If the user is on laptop, camera is unsupported. Opens a file picker instead.
        alert('Open camera is only available on mobile. Please use Upload a photo instead.')
    }
 })

// When a file is selected it appears in the viewfinder
fileInput.addEventListener('change', function() {
    const file = fileInput.files[0]  // Gets the first selected file
    if (file) {
        const reader = new FileReader()  // A tool that reads files
        reader.onload = function(e) {
            // Show the image inside the viewfinder
            viewfinder.style.backgroundImage = `url(${e.target.result})`
            viewfinder.style.backgroundSize = 'cover'
            viewfinder.style.backgroundPosition = 'center'

            //Hides the camera icon once found and  hints text inside the viewfinder
            viewfinder.querySelector('i').style.display = 'none'
            viewfinder.querySelector('p').style.display = 'none'

        }
        reader.readAsDataURL(file)  // Converts image to a URL

        // Once image is showed, send it to Flask to classify it
        classifyImage(file).then(function(result) {
            showResult(result)  //Updates page with the result
            updateLED(result.label)  //Lights up the correct LED
        })
    }
})

// Sends an image to Flask and gets the classification result
async function classifyImage(file) {
    const formData = new FormData()  // This creates a container to send the image
    formData.append('image', file)   // This adds the image to the container

    const response = await fetch('/classify', {
        method: 'POST',        // This sends data
        body: formData         // The image we are sending
    })

    const result = await response.json()  // Converts the response to JSON
    return result
}
// This will update the page with the classification result
function showResult(result) {
    if (result.recognized) {  //Sees if Flask returns True nor False
        // Show the sign name and confidence
        resultLabel.textContent = result.label
        resultConf.textContent = Math.round(result.confidence * 100) + '% confident'
        barLabel.textContent = result.label
        barFill.style.width = Math.round(result.confidence * 100) + '%'
        barPercent.textContent = Math.round(result.confidence * 100) + '%'
    } else {
        // Show unknown if confidence is too low
        resultLabel.textContent = 'Not a recognized sign'
        resultConf.textContent = 'Confidence too low'
        barLabel.textContent = '—'
        barFill.style.width = '0%'
        barPercent.textContent = '—'
    }

    // Show the result card and LED row
    resultCard.removeAttribute('hidden')
    ledRow.removeAttribute('hidden')
}

//Correct LED will light up according to the sign detected
function updateLED(label) {
    //Resets LEDs to off initially
    ledR.className = 'led'
    ledG.className = 'led'
    ledB.className = 'led'

    //Light up the right color based on the sign detected
    if (label === 'Stop') {
        ledR.className = 'led on-r'  // on-r makes red color appear
        ledText.textContent = 'Stop sign detected - Red LED has been activated'
    } else if (label === 'Pedestrian Crossing') {
        ledG.className = 'led on-g'
        ledText.textContent = 'Pedestrian Crossing sign detected - Green LED has been activated'
    } else if (label === 'No Entry') {
        ledB.className = 'led on-b'
        ledText.textContent = 'No Entry sign detected - Blue LED has been activated'
    } else if (label === 'Speed Limit') {
        ledR.className = 'led on-r'
        ledG.className = 'led on-g'
        ledText.textContent = 'Speed Limit sign detected - Yellow LED has been activated'
    } else {
        ledR.className = 'led on-r'  // mixes color to achieve a specific one
        ledG.className = 'led on-g'
        ledB.className = 'led on-b'
        ledText.textContent = 'Other sign detected — White LED active'
    }
}

})

