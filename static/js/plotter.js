function garden_HUD(){
    // Open a new connection, using the GET request on the URL endpoint
    fetch('/', {
              headers: {
               'Accept':'application/json'
              }
        }).then(
        function(request){
            console.log(request)
            if(request.status >= 200 && request.status < 400){
                request.json().then(function(data) {
                    console.log(data)
                    document.getElementById("garden_temperature").innerText = "Temperature: " + data['temperature'][0].toString() + '\u2103';
                    document.getElementById("garden_moisture").innerText = "Soil Mositure: " + ((1 - data['moistness'][0])*100).toPrecision(2).toString() + '\u0025';
                    document.getElementById("garden_humidity").innerText = "Humidity: " + data['humidity'][0].toString() + '\u0025';
                    document.getElementById("garden_pic").src = "http://192.168.1.12/" + data['image'][0]

                    var widget = document.getElementById("temp_chart");
                    var ticker_entry = document.createElement("div");
                    ticker_entry.className = "d-block col-sm-6";
                    var title = "Temperature"
                    var change = data['temperature']

                    var chartCanvas = document.createElement("canvas");
                    chartCanvas.id = "myChart" + String(idx);
                    ticker_entry.append(chartCanvas);
                    widget.innerHTML = ticker_entry.outerHTML

                    }else {
                        console.log('error')
                    }
                });
        })
}


garden_HUD()

window.setInterval(garden_HUD, 60000);