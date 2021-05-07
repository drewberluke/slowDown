//submits the hidden form on index.ejs to increment the counter
function submitForm() {
    var match = document.cookie.match(new RegExp('(^| )' + "allowReload" + '=([^;]+)'));
    if (match)
    {
        // var now = Date.now();
        // var expire = match[2];
        // console.log(Math.floor(Date.now() / 1000));
        // console.log(match[2]);
        // var remaining = match[2] - Math.floor(Date.now() / 1000);
        // alert('Wait ' + remaining + ' more seconds to request again');
        window.location.href = '/';
    }
    else{
        document.forms['/incrementCount'].submit();
    }

}

//deactivates the button and starts the countdown timer 
function inactive() {
    //function receives the number of minutes for the counter as an argument, can be changed here
    // var seconds = 10
    // timer(seconds);
    document.getElementById('wrapper').onclick = '';
    document.getElementById('wait').innerHTML = 'Please wait before requesting again';
}

// var counter = setInterval(timer, 1000);

// function timer(seconds) {
//     seconds = seconds - 1;
//     if (seconds <= -1) {
//         clearInterval(counter);
//         return;
//     }
//     document.getElementById('counter').innerHTML = seconds;

//     if (seconds == 0) {
//         document.forms['/back'].submit();
//     }
// }

// //countdown timer
// function countdown(minutes) {
//     var seconds = 60;
//     var mins = minutes

//     function tick() {
//         var counter = document.getElementById("counter");
//         var current_minutes = mins - 1
//         seconds--;
//         counter.innerHTML = current_minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
//         if (seconds > 0) {
//             setTimeout(tick, 1000);
//         } else {
//             if (mins > 1) {
//                 countdown(mins - 1);
//             }
//         }
//         if (seconds == 1) {
//             document.forms['/back'].submit();
//         }
//     }
//     tick();
// }

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
    var limit = parseFloat(document.getElementById('newLimit').value);
    if (Number.isInteger(limit)) {
        document.getElementById('thresh').submit();
    } else {
        alert("Please enter a whole number");
        limit = Math.floor(limit);
        document.getElementById('newLimit').value = limit;
        document.getElementById('newLimit').focus();
    }    
}

function reset() {
    document.getElementById('/delete').submit()
}