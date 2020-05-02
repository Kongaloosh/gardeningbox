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
                    var idx = 0;
                    for (idx =0; idx < data['time_stamp'].length; idx ++){
                        data['time_stamp'][idx] = new Date(data['time_stamp'][idx])
                        data['time_stamp'][idx] = data['time_stamp'][idx].toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
                    }

                    charts = ['temperature','moistness','humidity']
                    var idx = 0;
                    for (idx=0; idx < charts.length; idx ++) {
                    console.log(charts[idx] + "_chart")
                    var widget = document.getElementById(charts[idx] + "_chart");
                    var ticker_entry = document.createElement("div");
                    var title = charts[idx]
                    var chartCanvas = document.createElement("canvas");
                    chartCanvas.id = charts[idx] + "_chart_canvas"
                    ticker_entry.append(chartCanvas);
                    widget.innerHTML = ticker_entry.outerHTML

                    var ctx = document.getElementById(charts[idx] + "_chart_canvas").getContext('2d');
                    ctx.responsive = true;
                    console.log(Array.from(Array(data['temperature'].length).keys()))
                    var myChart = new Chart(ctx,
                    {
                        type: 'line',
                        data: {
                            labels: data['time_stamp'],
                            datasets: [{
                                label: 'Daily change',
                                data: data[charts[idx]],
                                borderWidth: 1,
                                // borderColor: 'rgb(235, 255, 236)',
                                // pointBackgroundColor: 'rgb(235, 255, 236)',
                            }]
                        },
                        options: {
                            title: {
                                display: true,
                                position: 'top',
                                text: charts[idx]
                            },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: false,
                                        // fontColor:'rgb(235, 255, 236)',
                                    },
                                    gridLines: {
                                        // color: 'rgb(235, 255, 236, 0.3)',
                                        display: true,
                                  },
                                }],
                                xAxes: [{
                                    ticks: {
                                        // fontColor:'rgb(235, 255, 236)',
                                    },
                                    gridLines: {
                                        // color: 'rgb(235, 255, 236, 0.3)',
                                        display: true,
                                  },
                                }]
                            },
                          pointLabels: {
                            // fontColor: 'white' // labels around the edge like 'Running'
                          },
                        }
                    }
                    );

                    }
                });
            }else {
                console.log('error')
            }
        })
}


garden_HUD()

window.setInterval(garden_HUD, 60000);