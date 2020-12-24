//submits the hidden form on index.ejs to increment the counter
function submitForm() {
    document.forms['/incrementCount'].submit();
}

//deactivates the button and starts the countdown timer 
function inactive() {
    //function receives the number of minutes for the counter as an argument, can be changed here
    min = 1
    countdown(min);
    document.getElementById('wrapper').onclick = '';
    document.getElementById('wait').innerHTML = 'Please wait before requesting again';
}

//countdown timer
function countdown(minutes) {
    var seconds = 60;
    var mins = minutes

    function tick() {
        var counter = document.getElementById("counter");
        var current_minutes = mins - 1
        seconds--;
        counter.innerHTML = current_minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        if (seconds > 0) {
            setTimeout(tick, 1000);
        } else {
            if (mins > 1) {
                countdown(mins - 1);
            }
        }
        if (seconds == 1) {
            document.forms['/back'].submit();
        }
    }
    tick();
}

//watches the number of clicks and alerts Prof. Gaskin when there is more than the specified mount
async function cutoff() {
    //document.forms['/admin'].submit();
    let count = parseInt(document.getElementById('clickCount').innerHTML);
    let cutoff = parseInt(document.getElementById('limit').innerHTML);
    //alert(count);
    //alert(cutoff);
    if (count >= cutoff) {
        playAlert();
        await new Promise((resolve, reject) => setTimeout(resolve, 3000));
        //alert('Slow down please!');
        document.forms['/delete'].submit();
    }
}


function thresh() {
    document.getElementById('thresh').submit()
}

function reset() {
    document.getElementById('/delete').submit()
}