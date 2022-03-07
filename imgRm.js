
function importRmImage(){
    const url = `https://www.thecocktaildb.com/api/json/v1/1/random.php`
    //JS로 서버 데이터 받기, promise 개념 사용
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const imgage = document.querySelector("#img-form img")
            imgage.src = `${data['drinks'][0]['strDrinkThumb']}`;
            const name = document.querySelector("#img-form span")
            name.innerText = `${data['drinks'][0]['strDrink']}`
s        })
 }
