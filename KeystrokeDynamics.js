//onload = function () {

var element = $("#inputbox");

var handler = function (e) {
    var inputName = $(this).attr("name");
    if (inputName == "password") handler.data.flyTime.push(e);
}

handler.data = {};
handler.data.flyTime = [];

element.on("keyup", handler);


function getAvg(dataInput) {
    var sum = 0;
    $.each(dataInput, function (index, value) {
        if (typeof dataInput[index + 1] != 'undefined') {
            sum += (dataInput[index + 1].timeStamp - value.timeStamp);

        }
    });
    return sum / dataInput.length;
}

//----------------------------------------------------------------------------------------------------------------------
var dwellTimes = {};
var dwelTime = [];
element.keydown(function (e) {
    if (!dwellTimes[e.which])
        dwellTimes[e.which] = new Date().getTime();
});
element.keyup(function (e) {
    var dt = new Date().getTime() - dwellTimes[e.which];
    delete dwellTimes[e.which];
    dwelTime.push((dt / 1000));
    //  $('#output').prepend("<p>Pressed key " + e.which + " for " + dwellTime / 1000 + "</p>");
});

function getAvgDwel(dataInput) {
    var sum = 0;
    $.each(dataInput, function (index, value) {
        if (typeof dataInput[index + 1] != 'undefined') {
            sum += value;
        }
    });
    return sum / dataInput.length;
}

//----------------------------------------------------------------------------------------------------------------------
function duration(timestamps) {
    var last = timestamps.pop();
    var durations = [];
    while (timestamps.length) {
        durations.push(last - (last = timestamps.pop()));
    }
    return durations.reverse();
}

function display(mills) {
    if (mills > 1000)
        return (mills / 1000);
    return mills;
}

var durations = [];
var timeElapsedList = [];
var durationList = [];
element.keydown(function (e) {
    durations.push($.now());
}).keyup(function (e) {
    var current = durations;
    current.push($.now());
    durations = [];
    var timeElapsed = current[current.length - 1] - current[0];
    timeElapsedList.push(display(timeElapsed))
    durationList.push(duration(current).map(display));

});


//----------------------------------------------------------------------------------------------------------------------

/**
 * Run calculations
 */

$(".kbutton").on('click', function (e) {
     $("#subbtn").submit();
    e.preventDefault();
    let dataset = [];
    let pw1Avg = getAvg(handler.data.flyTime);
    let dwelAvg = getAvgDwel(dwelTime);
    dwelAvg = dwelAvg == null ? 0 : dwelAvg
    let avgTL = getAvgDwel(timeElapsedList);
    avgTL = (avgTL != null) ? avgTL : 0
    let avgDu = getAvgDwel(durationList);
    avgDu = (avgDu != null) ? avgDu : 0;
    let label = document.getElementById('username').value;
    pw1Avg = !pw1Avg ? 0 : pw1Avg;
    dwelAvg = !dwelAvg ? 0 : dwelAvg;
    avgTL = !avgTL ? 0 : avgTL;
    avgDu = !avgDu ? 0 : avgDu;
    alert([pw1Avg,dwelAvg,avgDu,avgTL])
    if (pw1Avg && dwelAvg && avgTL & label!='admin') {
        let row = [pw1Avg, dwelAvg, avgTL, avgDu, label]
        dataset.push(row);

        var url_k = window.location.origin + $(this).attr('url');
        var type = $(this).attr('url');
        if ($(this).attr('url') == '/kauth') {
            dataset = [];
            row = [pw1Avg, dwelAvg, avgTL, avgDu]
            dataset.push(row);
        }

        $.ajax({
            url: url_k,
            method: 'POST',
            data: {'data': JSON.stringify(dataset)},
            success: function (result) {

                if (result.data) {
                    if (result.data == label) {
                        $("#subbtn").submit();
                    }else if (type == '/kauth') {
                        alert("Keyboard  authentication rejected");
                    }
                }
            }
        });
        delete dataset;

        // Reset data

        handler.data = {};
        handler.data.flyTime = [];
        durations = [];
        timeElapsedList = [];
        durationList = [];
        dwellTimes = {};
        dwelTime = [];
        console.log(JSON.stringify(dataset));
    } else {
        alert("keyboard data corrupted please try again");
    }
    return false;
});


//}