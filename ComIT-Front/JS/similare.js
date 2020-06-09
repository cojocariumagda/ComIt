chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let page_url = tabs[0].url;
    const Http = new XMLHttpRequest();
    const url = "https://comittw.herokuapp.com/get_similar?product_link=" + page_url;
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange= (e) => {
        let result;
        if(Http.responseText != null) {
            result = JSON.parse(Http.responseText);
        }
        if(result != null) {
            let out = "";
            let i;
            for(i = 0; i < result.length; i++) {
                out += '<div class ="produs"><a href ="' + result[i].link_produs + '"> <img src = "' + result[i].imagine_produs + '" alt = "imagine produs"></a>' +
                    'Nume produs: ' + result[i].nume_produs + '<br> Pret: ' + convert(result[i].pret_produs) + '</div>';
                ;
            }
            document.getElementById("similare").innerHTML = out;
        }
    };
});

function convert(arr) {
    let x = JSON.parse(arr);
    for(var i = x.length - 1; i >= 0; i--) {
        if(x[i] != null) {
            return x[i][1];
        }
    }
    return null;
}