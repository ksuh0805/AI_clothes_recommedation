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

function submitDiv() {
    const element = document.getElementById('result');
    const camera = document.getElementById('camera').value;
    
    const show_btn = document.getElementById('btn_yes');
    show_btn.style.display = "block";
}

//0704
const video = document.querySelector("#videoElement");

if (navigator.mediaDevices.getUserMedia) {
	navigator.mediaDevices.getUserMedia({ video: true })
        .then( (stream) => {
          video.srcObject = stream;
    	})
  		.catch(function (error) {
          console.log("Something went wrong!");
          console.log(error);
          return;
        });
};