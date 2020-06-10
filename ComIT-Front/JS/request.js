document.getElementById("buttonA").addEventListener("click", get);

function get() {
    const Http = new XMLHttpRequest();
    const url = 'https://comittw.herokuapp.com/search_product?content_search=' + document.getElementById('searchBar').value;
    Http.open("GET", url);
    Http.send();

    document.getElementById('searchBar').innerHTML.value = '';

    Http.onreadystatechange= (e) => {
        document.getElementById('computere').innerHTML = Http.responseText;
    };
}
