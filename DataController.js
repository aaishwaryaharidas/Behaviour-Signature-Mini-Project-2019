var tdna = new TypingDNA();
TypingDNA.addTarget(document.getElementById("inputbox"));
var data = []
var dataset  = "";
$(".kbutton").on('click', function (e) {
    e.preventDefault();
    let label = document.getElementById('username').value;
    if(label=='admin'){

        $("#subbtn").submit();
        return true;
    }
    var url_k = window.location.origin + $(this).attr('url');
    var type = $(this).attr('url');
    var typingPattern = tdna.getTypingPattern({type: 0, length: 2}) ;

    if ($(this).attr('url') == '/create') {
        typingPattern = tdna.getTypingPattern({type: 0, length: 2}) + "," + label;
        alert(typingPattern.split(",").length)
    }
    if(data.length>5){
        dataset = typingPattern;
    }

    tdna.reset()

    $.ajax({
        url: url_k,
        method: 'POST',
        data: {'data': dataset.toString()},
        success: function (result) {
            console.log('result' + JSON.stringify(result.data))
            data = [];
            if (result.data) {
                if (result.data == label) {
                    $("#subbtn").submit();
                } else if (type == '/kauth') {
                    alert("Keyboard  authentication rejected");
                }
            }
        }
    } ) ;

    return false;
})
$("#inputbox").keydown(function (e) {
    var code = (e.keyCode ? e.keyCode : e.which);
   data.push(code)
})
;


//}