
// document.addEventListener('readystatechange', function() {
//     if (document.readyState == "complete") {
//         const data = localStorage.getItem('name');
//         document.getElementById('tts_01').innerHTML =  + "성별을 알려주세요.";
//     }
// })
//성별 값을 로컬스토리지에 저장
function submitDiv() {
    const element = document.getElementById('result');
    const gender = document.getElementById('gender').value;
    
    document.getElementById('result').innerText = gender + "가 맞나요?"

    const show_btn = document.getElementById('btn_yes');
    show_btn.style.display = "block";

    localStorage.setItem('gender', gender)
}