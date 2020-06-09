chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let page_url = tabs[0].url;
    const Http = new XMLHttpRequest();
    const url = "https://comittw.herokuapp.com/get_offers?product_link=" + page_url;
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange= (e) => {
        let result;
        console.log(Http.responseText);
        if(Http.responseText != null) {
            result = JSON.parse(Http.responseText);
        }
        if(result != null) {
            let out = "";
            let i;
            for(i = 0; i < result.length; i++) {
                out += 'oferte';
            }
            document.getElementById("pret").innerHTML = out;
        }
    };
});