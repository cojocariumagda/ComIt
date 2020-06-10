import os
import time
import datetime
import socket
import ssl
import string
import pymongo
import atexit

MONGODB_URI = "mongodb://heroku_xzc0r78w:iipvtiu45d221kjg9fjjtqi7r9@ds243812.mlab.com:43812/heroku_xzc0r78w?retryWrites=false"

dict_principal_field = {
    "Laptop, Tablete & Telefoane": {
        "Laptopuri si accesorii": "/laptopuri-accesorii/sd?ref=hp_menu_quick-nav_1_0&type=subdepartment",
        "Telefoane mobile si accesorii": "/telefoane-mobile-accesorii/sd?ref=hp_menu_quick-nav_1_15&type=subdepartment",
        "Tablete si accesorii": "/tablete-accesorii/sd?ref=hp_menu_quick-nav_1_31&type=subdepartment",
        "Wearables & Gadgeturi": "/wearables-gadgeturi/sd?ref=hp_menu_quick-nav_1_38&type=subdepartment"},
    "PC, Periferice & Software": {
        "Desktop PC & Monitoare": "/desktop-pc-monitoare/sd?ref=hp_menu_quick-nav_23_0&type=subdepartment",
        "Componente PC": "/componente/sd?ref=hp_menu_quick-nav_23_6&type=subdepartment",
        "Software": "/software/sd?ref=hp_menu_quick-nav_23_17&type=subdepartment",
        "Periferice PC": "/periferice-accesorii/sd?ref=hp_menu_quick-nav_23_21&type=subdepartment",
        "Imprimante, scanere & consumabile": "/imprimante-scanere-consumabile/sd?ref=hp_menu_quick-nav_23_32&type=subdepartment",
        "Servere, Componente & UPS": "/servere-componente-ups/sd?ref=hp_menu_quick-nav_23_36&type=subdepartment",
        "Retelistica & supraveghere": "/retelistica-si-supraveghere/sd?ref=hp_menu_quick-nav_23_38&type=subdepartment"},
    "TV, Audio-Video & Foto": {
        "Televizoare & accesorii": "/televizoare-accesorii/sd?ref=hp_menu_quick-nav_190_0&type=subdepartment",
        "Videoproiectoare & accesorii": "/videoproiectoare-si-ecrane/sd?ref=hp_menu_quick-nav_190_14&type=subdepartment",
        "Audio HI-FI & Profesionale": "/audio-hi-fi/sd?ref=hp_menu_quick-nav_190_15&type=subdepartment",
        "Home Cinema & Audio": "/home-cinema-blu-ray/sd?ref=hp_menu_quick-nav_190_18&type=subdepartment",
        "Portabile audio": "/ipod-mp3-mp4-casti-audio/sd?ref=hp_menu_quick-nav_190_22&type=subdepartment",
        "Drone si accesorii": "/drone-accesorii/sd?ref=hp_menu_quick-nav_190_27&type=subdepartment",
        "Camere video sport & accesorii": "/camere-video-si-sport/sd?ref=hp_menu_quick-nav_190_28&type=link",
        "Aparate foto & accesorii": "/aparate-foto-accesorii/sd?ref=hp_menu_quick-nav_190_29&type=subdepartment"},
    "Electrocasnice & Climatizare": {
        "Aparate frigorifice": "/aparate-frigorifice/sd?ref=hp_menu_quick-nav_267_0&type=subdepartment",
        "Masini de spalat rufe": "/masini-spalat-rufe/sd?ref=hp_menu_quick-nav_267_5&type=subdepartment",
        "Incorporabile": "/incorporabile/sd?ref=hp_menu_quick-nav_267_10&type=subdepartment",
        "Masini de spalat vase": "/masini-spalat-vase/sd?ref=hp_menu_quick-nav_267_15&type=subdepartment",
        "Aragazuri, hote si cuptoare": "/aragazuri-cuptoare-microunde/sd?ref=hp_menu_quick-nav_267_16&type=subdepartment",
        "Electrocasnice bucatarie": "/electrocasnice-bucatarie/sd?ref=hp_menu_quick-nav_267_19&type=subdepartment",
        "Aspiratoare & fiare de calcat": "/aspiratoare-fiare-de-calcat/sd?ref=hp_menu_quick-nav_267_24&type=subdepartment",
        "Aparate de aer conditionat": "/aparate_aer_conditionat/stoc/c?ref=hp_menu_quick-nav_267_27&type=link",
        "Climatizare": "/climatizare-sisteme-incalzire/sd?ref=hp_menu_quick-nav_267_31&type=subdepartment"},
    "Bacanie": {"Bacanie": "/bacanie/sd?ref=hp_menu_quick-nav_1308_0&type=subdepartment",
                "Bauturi alcoolice": "/bauturi-alcoolice/sd?ref=hp_menu_quick-nav_1308_15&type=subdepartment",
                "Cosmetice": "/cosmetice/sd?ref=hp_menu_quick-nav_1308_35&type=subdepartment",
                "Spalare & intretinere rufe": "/spalare-intretinere-rufe/sd?ref=hp_menu_quick-nav_1308_46&type=subdepartment",
                "Produse dezinfectante": "/produse-dezinfectante/sd?ref=hp_menu_quick-nav_1308_127&type=subdepartment"},
    "Fashion": {"Imbracaminte femei": "/imbracaminte-femei/sd?ref=hp_menu_quick-nav_1696_1&type=subdepartment",
                "Incaltaminte femei": "/incaltaminte-femei/sd?ref=hp_menu_quick-nav_1696_6&type=subdepartment",
                "Genti si accesorii femei": "/genti-accesorii-femei/sd?ref=hp_menu_quick-nav_1696_10&type=subdepartment",
                "Imbracaminte barbati": "/imbracaminte-barbati/sd?ref=hp_menu_quick-nav_1696_15&type=subdepartment",
                "Incaltaminte barbati": "incaltaminte-barbati/sd?ref=hp_menu_quick-nav_1696_20&type=subdepartment",
                "Genti si accesorii barbati": "/accesorii-barbati/sd?ref=hp_menu_quick-nav_1696_24&type=subdepartment"},
    "Ingrijire personala & Cosmetice": {
        "Cosmetice & Ingrijire personala": "/cosmetice-produse-ingrijire-personala/sd?ref=hp_menu_quick-nav_368_4&type=subdepartment"},
    "Casa, Gradina & Bricolaj": {
        "Mobilier de gradina": "/mobilier-gradina/sd?ref=hp_menu_quick-nav_477_0&type=subdepartment",
        "Gradinarit": "/gradinarit/sd?ref=hp_menu_quick-nav_477_6&type=subdepartment",
        "Textile & covoare": "/textile-casa-covoare/sd?ref=hp_menu_quick-nav_477_35&type=subdepartment"},
    "Sport & Activitati in aer liber": {
        "Imbracaminte sport": "/imbracaminte-sport/sd?ref=hp_menu_quick-nav_651_16&type=subdepartment",
        "Incaltaminte sport": "/imbracaminte-incaltaminte-sport/sd?ref=hp_menu_quick-nav_651_27&type=subdepartment",
        "Fitness si nutritie": "/fitness-si-nutritie/sd?ref=hp_menu_quick-nav_651_31&type=subdepartment"},
    "Auto, Moto  & RCA": {"Anvelope & Jante": "/anvelope-jante/sd?ref=hp_menu_quick-nav_689_0&type=subdepartment",
                          "Accesorii auto": "/accesorii-auto-exterioare-interioare/sd?ref=hp_menu_quick-nav_689_23&type=subdepartment",
                          "Eletronice Auto": "/electronice-auto/sd?ref=hp_menu_quick-nav_689_17&type=subdepartment"},
    "Jucarii, Copii & Bebe": {"Bebelusi": "/toate-produsele-bebelusi/sd?ref=hp_menu_quick-nav_768_0&type=subdepartment"}
}


def receive_all(sock, chunk_size=1024):
    chunks = []
    while True:
        chunk = sock.recv(int(chunk_size))
        if chunk:
            chunks.append(chunk)
        else:
            break
    return ''.join(chunks)


def http_data(url, resursa, encoding='utf-8'):
    port = 443
    crlf = '\r\n\r\n'

    def handshake(sock):
        new_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1)
        return new_sock

    def make_header():
        headers = [
            'GET %s HTTP/1.1' % resursa,
            'Host: %s' % url,
            'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            # 'User-Agent: Chrome/83.0.4103.61',
            'Charset: %s' % encoding
        ]
        header = '\n'.join(headers)
        header += crlf
        return header

    def request(header):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((url, port))
        try:
            sock = handshake(sock)
            sock.sendall(header)
            str_ = receive_all(sock)
        finally:
            sock.shutdown(1)
            sock.close()
        return str_

    str_final = request(make_header())
    return str_final


def check_contains_digit(line):
    digits = string.digits
    for char in line:
        if char in digits:
            return int(char, 10)
    return 1


def count_still_open_xpath(line, xpath_current, count_current):
    # words = line.split()
    print "count intial", count_current
    count_current += line.count('<' + xpath_current)
    count_current -= line.count('</' + xpath_current)
    """for word in words:
        if '<' + xpath_current in word:
            count_current += 1
        if '</' + xpath_current in word:
            count_current -= 1"""
    print "count final", count_current
    return count_current


def get_content_menubar(data_http):
    lines = data_http.split('\n')
    found_body = 0
    found_menubar = 0
    str_menu = ""
    """xpath_list = xpath.split('/')
    total_xpath = len(xpath_list) - 1
    count_xpath = 0
    count_max_current_xpath = check_contains_digit(xpath_list[0])
    count_current_xpath = 0
    ok_count = 0"""
    for line in lines:
        new_line = line.strip()
        # print new_line
        if '<body' in new_line and '>' in new_line:
            found_body = 1
        if found_body == 1:
            if '<aside class="emg-menu-wrapper emg-box-sizing"' in new_line:
                found_menubar = 1
            if found_menubar == 1:
                str_menu += new_line
                str_menu += '\n'
            if '</aside' in new_line:
                found_menubar = 0
            """print xpath_list[count_xpath], ' spliter ', new_line
            if '<' + xpath_list[count_xpath].split('[')[0] in new_line or '</' + xpath_list[count_xpath].split('[')[0] \
                    in new_line:
                count_current_xpath = count_still_open_xpath(new_line, xpath_list[count_xpath].split('[')[0],
                                                             count_current_xpath)
                ok_count = 1
                print "count", xpath_list[count_xpath], "count_xpath", count_max_current_xpath
            if count_current_xpath == 0 and ok_count == 1:
                count_max_current_xpath -= 1
                ok_count = 0
            if count_max_current_xpath == 1 and ok_count == 1 and count_current_xpath == 1:
                ok_count = 0
                count_xpath += 1
            if count_xpath == total_xpath:
                str_menu += new_line
                str_menu += '\n'"""

        if "</body" in new_line:
            found_body = 0
    return str_menu


def parse_subcategorie_title(line):  # <li class="emg-aside-links-title">Accesorii Telefoane </li>
    string_title = line.split('>', 1)[1]
    string_title = string_title.split('<', 1)[0]
    return string_title


def parse_subcategorie_item(
        line):  # li><a  href="/huse-telefoane/c?tree_ref=0&amp;ref=cat_tree_2417">Huse telefoane</a></li>
    string_item_resursa = line.split('"', 2)[1]
    string_title_item = line.split('"', 2)[2]
    string_title_item = string_title_item.split('>', 1)[1]
    string_title_item = string_title_item.split('<', 1)[0]
    return string_title_item, string_item_resursa


def get_dict_categories(str_menu_current, base="Base"):
    dict_categories = {}
    lines = str_menu_current.split('\n')
    found_ul = 0
    current_base = base
    for line in lines:
        new_line = line.strip()
        if '<ul' in new_line:
            found_ul = 1
        if found_ul == 1:
            if current_base not in dict_categories:
                dict_categories[current_base] = {}
            if '<li' in new_line and 'href' in new_line:
                title_item, item_resursa = parse_subcategorie_item(new_line)
                dict_categories[current_base].update({title_item: item_resursa})
            if '<li' in new_line and 'class' in new_line:
                current_base = parse_subcategorie_title(new_line)
        if '</ul' in new_line:
            break
    return dict_categories


def get_content_items(data_items):
    lines = data_items.split('\n')
    found_body = 0
    found_div = 0
    str_items = ""
    list_items = []
    found_current_item = 0
    for line in lines:
        new_line = line.strip()
        # print new_line
        if '<body' in new_line and '>' in new_line:
            found_body = 1
        if found_body == 1:
            if "<div" in new_line and "id" in new_line and '"card_grid"' in new_line:
                found_div = 1
            if found_div == 1:
                if found_current_item == 1:
                    if 'class="card-item js-product-data"' not in new_line:
                        str_items += new_line
                        str_items += '\n'
                    else:
                        found_current_item = 0
                        str_items += new_line.split('<div class="card-item js-product-data"')[0]
                        str_items += '\n'
                        list_items.append(str_items)
                        str_items = ""
                if '<div class="card-item js-product-data"' in new_line:
                    str_items += new_line.split('<div class="card-item js-product-data"')[1]
                    str_items += '\n'
                    found_current_item = 1
        if "</body" in new_line:
            found_body = 0
    return list_items


def get_dict_item(item):
    # data-name="Telefon mobil Samsung Galaxy A30s, Dual SIM, 64GB, 4G, Black"
    # <img data-src="https://s12emagst.akamaized.net/products/25122/25121026/images/res_36f3651190f18e1fe9cfc03c81de260b_200x200_arrn.jpg"
    # <div class="card-heading"><a href="https://www.emag.ro/telefon-mobil-samsung-galaxy-a30s-dual-sim-64gb-4g-black-sm-a307fzkvrom/pd/DLFTD6BBM/"
    # <a href="https://www.emag.ro/telefon-mobil-samsung-galaxy-a30s-dual-sim-64gb-4g-black-sm-a307fzkvrom/pd/DLFTD6BBM/#reviews-section"
    # <div class="star-rating-inner " style="width: 92%"                   - cat % din stelute e plina la rating
    # <span class="hidden-xs ">288 de review-uri </span>
    # <p class="product-stock-status text-availability-in_stock">\xc3\xaen stoc</p> - valabilitate
    # <p class="product-new-price">849<sup>99</sup> <span>Lei
    """#for item in list_items:
    lines = item.split('\n')
    dict_item = {}
    for line in lines:
        new_line = line.strip()
        try:
            if 'data-name="' in new_line:
                nume_produs = new_line.split('data-name="')[1]
                nume_produs = nume_produs.split('"', 1)[0]
                dict_item.update({"nume_produs": nume_produs})
            if '<img data-src="' in new_line:
                imagine_produs = new_line.split('<img data-src="')[1]
                imagine_produs = imagine_produs.split('"', 1)[0]
                dict_item.update({"imagine_produs": imagine_produs})
            if '<div class="card-heading"><a href="' in new_line:
                link_produs = new_line.split('<div class="card-heading"><a href="')[1]
                link_produs = link_produs.split('"', 1)[0]
                dict_item.update({"link_produs": link_produs})
            if 'class="star-rating-container js-product-url' in new_line:
                link_reviews = new_line.split('class="star-rating-container js-product-url')[0]
                link_reviews = link_reviews.split('<a href="')[1]
                link_reviews = link_reviews.split('"')[0]
                dict_item.update({"link_reviews": link_reviews})
            if '<div class="star-rating-inner " style="width:' in new_line:
                rating_produs = new_line.split('<div class="star-rating-inner " style="width: ')[1]
                rating_produs = rating_produs.split('"')[0]
                dict_item.update({"rating_produs": rating_produs})
            if '<span class="hidden-xs ">' in new_line:
                reviews_produs = new_line.split('<span class="hidden-xs ">')[1]
                reviews_produs = reviews_produs.split('</span')[0]
                dict_item.update({"reviews_produs": reviews_produs})
            if '<p class="product-stock-status text-availability-in_stock">' in new_line:
                valabilitate_produs = new_line.split('<p class="product-stock-status text-availability-in_stock">')[1]
                valabilitate_produs = valabilitate_produs.split('</p')[0]
                dict_item.update({"valabilitate_produs": valabilitate_produs})
            if '<p class="product-new-price">' in new_line:
                pret_produs = new_line.split('<p class="product-new-price">')[1]
                pret_produs = pret_produs.replace('&#46;', '.')
                pret_after_comma = pret_produs.split('<sup>')[1]
                pret_after_comma = pret_after_comma.split('</sup>')[0]
                pret_moneda = pret_produs.split('<span>')[1]
                pret_moneda = pret_moneda.split('</span>')[0]
                pret_produs = pret_produs.split('<sup>')[0]
                pret_produs += "," + pret_after_comma + " " + pret_moneda
                dict_item.update({"pret_produs": pret_produs})
        except Exception as e:
            print "eroare", e
            print new_line
    return dict_item"""
    dict_item = {}
    item = item.replace('\n', '')
    try:
        if 'data-name="' in item:
            nume_produs = item.split('data-name="')[1]
            nume_produs = nume_produs.split('"', 1)[0]
            dict_item.update({"nume_produs": nume_produs})
        if '<img data-src="' in item:
            imagine_produs = item.split('<img data-src="')[1]
            imagine_produs = imagine_produs.split('"', 1)[0]
            dict_item.update({"imagine_produs": imagine_produs})
        if '<div class="card-heading"><a href="' in item:
            link_produs = item.split('<div class="card-heading"><a href="')[1]
            link_produs = link_produs.split('"', 1)[0]
            dict_item.update({"link_produs": link_produs})
        if 'class="star-rating-container js-product-url' in item:
            link_reviews = item.split('class="star-rating-container js-product-url')[0]
            link_reviews = link_reviews.split('<a href="')[1]
            link_reviews = link_reviews.split('"')[0]
            dict_item.update({"link_reviews": link_reviews})
        if '<div class="star-rating-inner " style="width:' in item:
            rating_produs = item.split('<div class="star-rating-inner " style="width: ')[1]
            rating_produs = rating_produs.split('"')[0]
            dict_item.update({"rating_produs": rating_produs})
        if '<span class="hidden-xs ">' in item:
            reviews_produs = item.split('<span class="hidden-xs ">')[1]
            reviews_produs = reviews_produs.split('</span')[0]
            dict_item.update({"reviews_produs": reviews_produs})
        if '<p class="product-stock-status text-availability-in_stock">' in item:
            valabilitate_produs = item.split('<p class="product-stock-status text-availability-in_stock">')[1]
            valabilitate_produs = valabilitate_produs.split('</p')[0]
            dict_item.update({"valabilitate_produs": valabilitate_produs})
        pret_produs = []
        if '<p class="product-old-price">' in item:
            pret_produs_vechi = item.split('<p class="product-old-price">')[1]
            pret_produs_vechi_backup = pret_produs_vechi.split('<p class="product-new-price">')[0]
            digits = string.digits
            ok = 0
            for chr in pret_produs_vechi_backup:
                if chr in digits:
                    ok = 1
            if ok == 1:
                pret_produs_vechi = pret_produs_vechi.replace('&#46;', '.')
                pret_produs_vechi = pret_produs_vechi.split('<s>')[1]
                pret_after_comma = pret_produs_vechi.split('<sup>')[1]
                pret_after_comma = pret_after_comma.split('</sup>')[0]
                pret_moneda = pret_produs_vechi.split('<span>')[1]
                pret_moneda = pret_moneda.split('</span>')[0]
                pret_produs_vechi = pret_produs_vechi.split('<sup>')[0]
                pret_produs_vechi += "," + pret_after_comma + " " + pret_moneda
                pret_produs.append(pret_produs_vechi)
            else:
                pret_produs.append(None)
        else:
            pret_produs.append(None)
            """dict_item.update({"pret_produs": [pret_produs_vechi]})
            else:
                dict_item.update({"pret_produs": []})"""
        if '<p class="product-new-price">' in item:
            pret_produs_nou = item.split('<p class="product-new-price">')[1]
            pret_produs_nou = pret_produs_nou.replace('&#46;', '.')
            pret_after_comma = pret_produs_nou.split('<sup>')[1]
            pret_after_comma = pret_after_comma.split('</sup>')[0]
            if '<span>' in pret_produs_nou:
                pret_moneda = pret_produs_nou.split('<span>')[1]
                pret_moneda = pret_moneda.split('</span>')[0]
                pret_produs_nou = pret_produs_nou.split('<sup>')[0]
            else:
                pret_moneda = 'Lei'
            pret_produs_nou += "," + pret_after_comma + " " + pret_moneda
            pret_produs.append(pret_produs_nou)
        else:
            pret_produs.append(None)
        timestamp = datetime.datetime.utcfromtimestamp(int(time.time()))
        pret_produs.append(timestamp)
        dict_item.update({"pret_produs": [pret_produs]})
        return dict_item
    except Exception as e:
        print e
        return None


def insert_principal_fields():
    # db_comit = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["principal_categories"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db_comit = db.principal_categories
    int_id = 0
    for principal_category in dict_principal_field.keys():
        inserted = db_comit.insert_one({"_id": "p_{}".format(int_id), "nume_categorie": principal_category})
        int_id += 1


def insert_second_fields():
    # db_comit_principal = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["principal_categories"]
    # db_comit_second = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["second_categories"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db_comit_principal = db.principal_categories
    db_comit_second = db.second_categories
    int_id = 0
    for second_category in dict_principal_field:
        id_principal_category = db_comit_principal.find({"nume_categorie": second_category}, {'_id': 1})
        for field in id_principal_category:
            id_principal_category = field['_id']
        for key_nume in dict_principal_field[second_category]:
            inserted = db_comit_second.insert_one({"_id": "s_{}".format(int_id),
                                                   "_id_principal_category": id_principal_category,
                                                   "nume_subcategorie": key_nume,
                                                   "resursa_subcategorie": dict_principal_field[second_category][
                                                       key_nume]})
            int_id += 1


def insert_items():
    # id_curent, id_categorie_principala, id_categorie_secundara, nume_subsubcategorie, informatii item
    # db_comit_items = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["items_emag"]
    # db_comit_second = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["second_categories"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db_comit_items = db.items_emag
    db_comit_second = db.second_categories
    id_int = db_comit_items.find().count() + 1
    second_category_db = db_comit_second.find()

    for category in second_category_db:
        dict_category_db = category
        print "from db", dict_category_db
        time.sleep(5)
        if os.path.exists("stop_emag"):
            print("Stopping emag in 5 seconds...")
            time.sleep(5)
            os.remove("stop_emag")
            return
        resursa = dict_category_db['resursa_subcategorie']
        data = http_data("www.emag.ro", resursa)
        str_menu = get_content_menubar(data)
        dict_categories = get_dict_categories(str_menu, dict_category_db[
            'nume_subcategorie'])  # contine toate subcategoriile din meniul de pe pagina
        for subcategory in dict_categories:
            for nume_subcategory in dict_categories[subcategory]:
                data_item = http_data("www.emag.ro", dict_categories[subcategory][nume_subcategory])
                time.sleep(30)
                if os.path.exists("stop_emag"):
                    print("Stopping emag in 5 seconds...")
                    time.sleep(5)
                    os.remove("stop_emag")
                    return
                list_items = get_content_items(data_item)
                for item in list_items:
                    dict_info_item = get_dict_item(item)
                    if dict_info_item is None:
                        continue
                    try:
                        # update part
                        my_query_for_check = {"nume_produs": dict_info_item['nume_produs']}
                        if db_comit_items.find(my_query_for_check).count() > 0:
                            old_items = db_comit_items.find(my_query_for_check)
                            for old_item in old_items:
                                new_list = []
                                for item_list in old_item['pret_produs']:
                                    new_list.append(item_list)
                                new_list.append(dict_info_item['pret_produs'][0])
                                print "update", (id_int, new_list, dict_info_item)
                                db_comit_items.update_one({"_id": old_item["_id"]}, {"$set": {"pret_produs": new_list}})
                        else:
                            dict_info_item.update({"_id": "i_{}".format(id_int),
                                                   "_id_principal_category": dict_category_db['_id_principal_category'],
                                                   "_id_second_category": dict_category_db['_id']})
                            inserted = db_comit_items.insert_one(dict_info_item)
                            id_int += 1
                            print "insert", (id_int, dict_info_item)
                    except Exception as e:
                        print "error ", e
                        print dict_info_item


def cleanup():
    files_to_delete = ["active_emag", "stop_emag", "finished_emag", "running_emag", "start_emag"]
    for item in files_to_delete:
        if os.path.exists(item):
            os.remove(item)


if __name__ == '__main__':
    atexit.register(cleanup)
    handler = open("active_emag", "w")
    # handler.write("{}".format(int(time.time())))
    handler.close()
    while True:
        try:
            if os.path.exists("start_emag"):
                print("Found start_emag, cooldown for 5 seconds and starting the job...")

                time.sleep(5)
                os.remove("start_emag")
                if os.path.exists("finished_emag"):
                    os.remove("finished_emag")

                h = open("running_emag", "w")
                # h.write("{}".format(int(time.time())))
                h.close()

                insert_items()
                print("Job has been finished...")

                os.remove("running_emag")

                h = open("finished_emag", "w")
                # h.write("{}".format(int(time.time())))
                h.close()
        except Exception as e:
            print("Exception: {}".format(e))
        print("Sleeping for 1 minute")
        time.sleep(60)
    os.remove("active_emag")

# if __name__ == '__main__':
# insert_principal_fields()  # am inserat categoriile principale (insert only one)
# insert_second_fields() # am inserat categoriile secundare in concordata cu cele principale (insert only one)
# insert_items()
