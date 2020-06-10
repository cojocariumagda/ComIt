
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        let page_url = tabs[0].url;
        const Http = new XMLHttpRequest();
        const url = "https://comittw.herokuapp.com/get_price_fluctuation?product_link=" + page_url;
        Http.open("GET", url);
        Http.send();

        Http.onreadystatechange = (e) => {
            let result = JSON.parse(Http.responseText);
            const ctx = document.getElementById('pretCanvas').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Pret vechi', 'Pret nou'],
                    datasets: [{
                        label: 'Fluctuatia pretului',
                        data: [parseInt(1899), 1999],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: false,
                                suggestedMax: 5000,
                                suggestedMin: 100
                            }
                        }]
                    }
                }
            });
        };
    });
