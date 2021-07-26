/* function load() {
    var video = document.getElementById('myVideo');
    if (navigator.webkitGetUserMedia) {
        navigator.webkitGetUserMedia({audio:true, video:true},
            function(stream) { video.src = webkitURL.createObjectURL(stream); },
            function(error) { alert('ERROR: ' + error.toString()); } );
    } else {
        alert('webkitGetUserMedia not supported');
    }
}

*/


document.addEventListener('readystatechange', function() {
    if (document.readyState == "complete") {
        const data = localStorage.getItem('name');
        document.getElementById('tts_01').innerHTML = data + "님의 체형을 분석하겠습니다.";
    }
})

function submitDiv() {
    const element = document.getElementById('result');
    const camera = document.getElementById('camera').value;
    
    const show_btn = document.getElementById('btn_yes');
    show_btn.style.display = "block";
}