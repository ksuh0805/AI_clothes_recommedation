
// document.addEventListener('readystatechange', function() {
//     if (document.readyState == "complete") {
//         const data = localStorage.getItem('name');
//         document.getElementById('tts_01').innerHTML = "몸무게를 알려주세요.";
//     }
// })
//몸무게 값을 로컬스토리지에 저장
function submitDiv() {
    const weight = document.getElementById('weight').value;
    
    document.getElementById('result').innerText = weight + "kg가 맞나요?"

    const show_btn = document.getElementById('btn_yes');
    show_btn.style.display = "block";

    localStorage.setItem('weight', weight)
}