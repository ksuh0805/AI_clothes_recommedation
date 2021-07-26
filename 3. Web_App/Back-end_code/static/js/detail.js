/**
 * 비가 오는경우 rain.png
 * 맑은 경우 sunny.png
 * 흐린 경우 cloudy.png 배경화면에 적용
 */

const image = {
  rain : "../static/src/images/rain.png",
  sunny : "../static/src/images/sunny.png",
  cloud : "../static/src/images/cloud.png"
}

const value = key_weather;
// 백에서 날씨 값을 들어오게 해서 value에 저장
if (value == "맑은") {
  document.body.style.backgroundImage = "url('"+image.sunny+"')";
  console.log(value + "맑은");
} else if (value == "구름 많은") {
  document.body.style.backgroundImage = "url('"+image.cloud+"')";
  console.log(value + "구름 많은");
} else {
  document.body.style.backgroundImage = "url('"+image.rain+"')";
  console.log(value + "나머지")
}

let data = "";


//케쥬얼을 선택한 경우
function casual(){
    const value = "casual"
    let jsonData = new Object();
    jsonData.style = value;
    data = JSON.stringify(jsonData)


$.ajax({
        type : 'POST',
        contentType:'application/json',
        url:'http://127.0.0.1:5000/result',
        dataType:'json',
        data : JSON.stringify(jsonData)
        });
}

//비즈니스를 선택한 경우
function business(){
    const value = "business"
    let jsonData = new Object();
    jsonData.style = value;
    data = JSON.stringify(jsonData)


$.ajax({
        type : 'POST',
        contentType:'application/json',
        url:'http://127.0.0.1:5000/result',
        dataType:'json',
        data : JSON.stringify(jsonData)
        });
}

//스포츠를 선택한 경우
function sports(){
    const value = "sports"
    let jsonData = new Object();
    jsonData.style = value;
    data = JSON.stringify(jsonData)


$.ajax({
        type : 'POST',
        contentType:'application/json',
        url:'http://127.0.0.1:5000/result',
        dataType:'json',
        data : JSON.stringify(jsonData)
        });
}
