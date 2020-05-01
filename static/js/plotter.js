function garden_HUD(){
    // Open a new connection, using the GET request on the URL endpoint
    fetch('/')
        .then(
        function(request){
            console.log(request)
            if(request.status >= 200 && request.status < 400){
                request.json().then(function(data) {
                    document.getElementById("garden_temperature").innerText = "Temperature: " + data['temperature'][0].toString() + '\u2103';
                    document.getElementById("garden_moisture").innerText = "Soil Mositure: " + ((1 - data['moistness'][0])*100).toPrecision(2).toString() + '\u0025';
                    document.getElementById("garden_humidity").innerText = "Humidity: " + data['humidity'][0].toString() + '\u0025';
                    document.getElementById("garden_pic").src = "http://192.168.1.12/" + data['image'][0]
                });
            }else {
                console.log('error')
            }
        })
}


garden_HUD()

window.setInterval(garden_HUD, 60000);