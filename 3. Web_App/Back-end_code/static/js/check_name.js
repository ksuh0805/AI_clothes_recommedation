
//이름 값을 로컬스토리지에 저장
function submitDiv() {
    const element = document.getElementById('result');
    const name = document.getElementById('name').value;
    
    document.getElementById('result').innerText = name + "이 맞나요?"

    const show_btn = document.getElementById('btn_yes');
    show_btn.style.display = "block";

    localStorage.setItem('name', name)
    
}

