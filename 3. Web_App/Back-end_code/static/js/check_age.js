// document.addEventListener('readystatechange', function() {
//     if (document.readyState == "complete") {
//         const data = localStorage.getItem('name');
//         document.getElementById('tts_01').innerHTML = "나이를 알려주세요.";
//     }
// })

//나이 값을 로컬스토리지에 저장
function submitDiv() {
    const age = document.getElementById('age').value;
    
    document.getElementById('result').innerText = age + "가 맞나요?"

    const show_btn = document.getElementById('btn_yes');
    show_btn.style.display = "block";

    localStorage.setItem('height', height)
}