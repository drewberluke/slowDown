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

function studentWaitTime() {
    var newTime = parseFloat(document.getElementById('newStudentWaitTime').value);
    if (Number.isInteger(newTime)) {
        document.getElementById('studentWaitTime').submit();
    } else {
        alert("Please enter a whole number");
        newTime = Math.floor(newTime);
        document.getElementById('newStudentWaitTime').value = newTime;
        document.getElementById('newStudentWaitTime').focus();
    }    
}

function resetSetting() {
    var setting = parseFloat(document.getElementById('setting').value);
    if (Number.isInteger(setting)) {
        document.getElementById('resetSetting').submit();
    } else {
        alert("Please enter a whole number");
        setting = Math.floor(setting);
        document.getElementById('setting').value = setting;
        document.getElementById('setting').focus();
    }
    
}

function reset() {
    document.getElementById('/delete').submit()
}

function resetTimer() {
    document.getElementById('resetTimer').submit()
}

function alertInput() {
    var input = document.getElementById('alertCheckbox');

    if (input.checked == true) {
        document.cookie = "playAlert=true";
        //alert(document.cookie);
    } else {
        document.cookie = "playAlert=false";
        //alert(document.cookie);
    }
}

function alertStatus() {
    var name = "playAlert";
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        if (match[2] == "true") {
            document.getElementById('alertCheckbox').checked = true;
        } else {
            document.getElementById('alertCheckbox').checked = false;
        }
    } else {
        document.getElementById('alertCheckbox').checked = true;
        document.cookie = "playAlert=true";
    }
}

function timerStatus() {
    var name = "timerStatus";
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        if (match[2] == "on") {
            //alert('timer On');
            document.getElementById('requestResetCheckbox').checked = true;
        } else {
            //alert('timer off');
            document.getElementById('requestResetCheckbox').checked = false;
        }
    } else {
        document.getElementById('requestResetCheckbox').checked = true;
        document.cookie = 'timerStatus=on';
    }
}

function timerInput() {
    var input = document.getElementById('requestResetCheckbox');

    if (input.checked == true) {
        document.cookie = "timerStatus=on";
        //alert(document.cookie);
    } else {
        document.cookie = "timerStatus=off";
        //alert(document.cookie);
    }
}

function onPageLoad() {
    cutoff();
    alertStatus();
    timerStatus();
}

function refresh() {
    window.location.href = '/';
}