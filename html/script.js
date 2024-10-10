

// Function that turns off all border colors of the corners of a square`
function turnOfallBorder(elementId, rowNum) {
    const element = document.getElementById(elementId);
    const leftCorners = element.querySelector(`#left${rowNum}`);
    const rightCorners = element.querySelector(`#right${rowNum}`);
    const allCorners = ['left', 'right', 'top', 'bottom'];
    allCorners.forEach(corner => {
        if (leftCorners.style[`border-${corner}-color`] === 'red') {
            leftCorners.style[`border-${corner}-color`] = 'rgba(255,0,0,0.15)';
        }
        if (rightCorners.style[`border-${corner}-color`] === 'red') {
            rightCorners.style[`border-${corner}-color`] = 'rgba(255,0,0,0.15)';
        }
    });
    if (rowNum < 3) {
        turnOfallBorder(elementId, rowNum + 1);
    }

}

// Change the border color of the left square
function changeBorder(placement, rowNum, left, top, mirrorVertical) {
    // Get the left or right square on a certain row
    const digitsPlace = document.getElementById(placement);
    // make a ? to get the left or right square
    const element = digitsPlace.querySelector(`#${left ? 'left' : 'right'}${rowNum}`);
    if (top) {
        element.style['border-right-color'] = 'red';
        const mirrorElement = digitsPlace.querySelector(`#${left ? 'right' : 'left'}${rowNum}`);
        mirrorElement.style['border-left-color'] = 'red';
    }
    else {
        element.style['border-bottom-color'] = 'red';
    }
    if (mirrorVertical) {
        const mirrorHorizontalElement = digitsPlace.querySelector(`#${left ? 'left' : 'right'}${rowNum+1}`);
        if (top) {
            mirrorHorizontalElement.style['border-bottom-color'] = 'red';
        }
        else {
            mirrorHorizontalElement.style['border-top-color'] = 'red';
        }
    }
}

// A reset function that turns off all segments and corner-borders in a given elementId (first or second digit of hour or minutes)
function resetSeg(elementId) {
    // Get segment div
    const element = document.getElementById(elementId);
    // Go through each segment and turn it on
    for (let i = 1; i <= 7; i++) {
        const seg = element.querySelector(`#seg${i}`);
        seg.style.backgroundColor = 'rgba(255,0,0,0.15)';
    }
}
// Similar to setNumber function, this one turns on the borders of the segments of the clock
function turnOnBorder(placement, segment) {
    if (segment === 1) {
        changeBorder(placement, 1, left = true, top = true, mirrorVertical = false);
    }
    if (segment === 2) {
        changeBorder(placement, 1, left = true, top = false, mirrorVertical = true);
    }
    if (segment === 3) {
        changeBorder(placement, 1, left = false, top = false, mirrorVertical = true);
    }
    if (segment === 4) {
        changeBorder(placement, 2, left = true, top = true, mirrorVertical = false);
    }
    if (segment === 5) {
        changeBorder(placement, 2, left = true, top = false, mirrorVertical = true);
    }
    if (segment === 6) {
        changeBorder(placement, 2, left = false, top = false, mirrorVertical = true);
    }
    if (segment === 7) {
        changeBorder(placement, 3, left = true, top = true, mirrorVertical = false);
    }
}


// Function that colors an item red after recieving elementId (first or second digit of hour or minutes) and a segment number (number between 1 and 7)
function turnOnSeg(elementId, segNum) {
    // Make the elementId into a constant so that we can later style it
    const element = document.getElementById(elementId);
    // Go through each number given in segNum (1-7), and turn on the item by coloring it red
    segNum.forEach(segNum => {
        // Turn on the borders of the segment
        turnOnBorder(elementId, segNum);
        const seg = element.querySelector(`#seg${segNum}`);
        seg.style.backgroundColor = 'red';
    })
}

// Function that sets a number in the clock after recieving elementId (first or second digit of hour or minutes) and the number it is supposed to set it to
function setNumber(elementId, number) {
    // Reset the number
    resetSeg(elementId);
    turnOfallBorder(elementId, 1);
    if (number === 0) { 
        turnOnSeg(elementId, [1, 2, 3, 5, 6, 7]);
    }
    if (number === 1) { 
        turnOnSeg(elementId, [3, 6]);
    }
    if (number === 2) { 
        turnOnSeg(elementId, [1, 3, 4, 5, 7]);
    }
    if (number === 3) { 
        turnOnSeg(elementId, [1, 3, 4, 6, 7]);
    }
    if (number === 4) { 
        turnOnSeg(elementId, [2, 3, 4, 6]);
    }
    if (number === 5) { 
        turnOnSeg(elementId, [1, 2, 4, 6, 7]);
    }
    if (number === 6) { 
        turnOnSeg(elementId, [1, 2, 4, 5, 6, 7]);
    }
    if (number === 7) { 
        turnOnSeg(elementId, [1, 3, 6]);
    }
    if (number === 8) { 
       turnOnSeg(elementId, [1, 2, 4, 5, 6, 7]);
   }
    if (number === 9) { 
        turnOnSeg(elementId, [1, 2, 3, 4, 6, 7]);
    }
        
}







// Now we will create a function that gets the time and updates the clock accordingly
function updateClock() {
    // Get the current time
    const now = new Date();
    // Get the hours and minutes
    const hour = now.getHours();
    const minutes = now.getMinutes();
    
    // Get the first and second digit of the hours
    const firstDigitHour = Math.floor(hour/10);
    const secondDigitHour = hour%10;
    // Get the first and second digit of minute
    const firstDigitMinutes = Math.floor(minutes/10);
    const secondDigitMinutes = minutes%10;

    // Run our function to update the clock accordingly
    // Update first and second digit of hour
    setNumber('hour-first-digit', firstDigitHour);
    setNumber('hour-second-digit', secondDigitHour);
    // Update the first and second digit of minute
    setNumber('minutes-first-digit', firstDigitMinutes);
    setNumber('minutes-second-digit', secondDigitMinutes);
}

let isDotOn = true;
function updateColon() {
    // only run if secondCount passes three
    const colon = document.getElementsByClassName('colon-dot');
    colon[0].style.backgroundColor = isDotOn ? 'rgba(255,0,0,0.15)' : 'red';
    colon[1].style.backgroundColor = isDotOn ? 'rgba(255,0,0,0.15)' : 'red';
    isDotOn = !isDotOn;
}

updateClock();
setInterval(updateClock, 1000);
setInterval(updateColon, 1000);

