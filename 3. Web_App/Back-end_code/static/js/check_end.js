/* 
name, gender, weight, height를 여기로 모은뒤 Json 형식으로 묶어서 서버로 전송

서버에서 각각 보내서 일괄 취합가능하면 check_end.js 삭제
*/
//저장된 프로필 정보를 백엔드에 JSON형태로 변환하여 POST방식으로 전송
document.addEventListener('readystatechange', function() {
    if (document.readyState == "complete") {
        const name = localStorage.getItem('name');
        const gender = localStorage.getItem('gender');
        const weight = localStorage.getItem('weight');
        const height = localStorage.getItem('height');

        let jsonData = new Object();
        jsonData.name = name;
        jsonData.gender = gender;
        jsonData.weight = weight;
        jsonData.height = height;

        console.log(JSON.stringify(jsonData));
        // 이쪽부분부터 서버 보내는 작업 시작하시면 됩니다.

        $.ajax({
        type : 'POST',
        contentType:'application/json',
        url:'http://127.0.0.1:5000/closet',
        dataType:'json',
        data : JSON.stringify(jsonData)
        });

        setTimeout(function(){
            location.href = "http://127.0.0.1:5000/closet";
        }, 3000);
    }
})