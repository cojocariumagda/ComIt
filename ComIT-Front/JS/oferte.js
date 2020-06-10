chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let page_url = tabs[0].url;
    const Http = new XMLHttpRequest();
    const url = "https://comittw.herokuapp.com/get_offers?product_link=" + page_url;
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange= (e) => {
        let result;
        result = JSON.parse(Http.responseText);
        if(result != null) {
            let out = "";
            let i;
            for(i = 0; i < result.length; i++) {
                out += '<div class = "produs"><a target = "_blank" href="' + result[i].link_produs +
                    '"><img src ="' + result[i].imagine_produs + '" alt = "imagine produs"></a><span class = "nextToImage">Nume: ' +
                    result[i].nume_produs + '<br>Pret: ' + result[i].pret_produs + '</span></div>';
            }
            document.getElementById("oferte").innerHTML = out;
        }
    };
});