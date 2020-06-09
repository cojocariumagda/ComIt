import os
import json
import time
import datetime
import socket
import ssl
import string
import pymongo

MONGODB_URI = "mongodb://heroku_xzc0r78w:iipvtiu45d221kjg9fjjtqi7r9@ds243812.mlab.com:43812/heroku_xzc0r78w?retryWrites=false"


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
        # new_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
        new_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2)
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


def get_resourse_principal_bar(data_http):
    lines = data_http.split('\n')
    found_body = 0
    found_principal_bar = 0
    str_principal_bar = ""
    for line in lines:
        new_line = line.strip()
        if '<body' in new_line and '>' in new_line:
            found_body = 1
        if found_body == 1:
            if '<ul class="index-category-menu"' in new_line:
                found_principal_bar = 1
            if found_principal_bar == 1:
                str_principal_bar += new_line
                str_principal_bar += '\n'
            if '<ul class="top_header' in new_line and found_principal_bar == 1:
                found_principal_bar = 0
        if '</body' in new_line:
            found_body = 0
    return str_principal_bar


def get_dict_promotions(list_promotions, id_principal, id_curent):
    list_items = list_promotions.split('<div class="left_vertical_promozone">')
    list_items_promotion = []
    list_of_dict_promotion = []
    list_items_promotion.append(list_items[0])
    if '<div class="left_vertical_promozone last' in list_items[1]:
        new_list_item = list_items[1].split('<div class="left_vertical_promozone last')
        list_items_promotion.append(new_list_item[0])
        list_items_promotion.append(new_list_item[1])
    for item in list_items_promotion:
        link_produs = item.split('<div class="left_vertical_promozone_img"><a href="')
        link_produs = link_produs[1].split('"')[0]
        link_produs = "https://www.evomag.ro" + link_produs

        info_produs = item.split('<img')
        info_produs = info_produs[1].split('<div class="left_vertical_promozone_title')[0]
        nume_produs = info_produs.split('title="')[1]
        nume_produs = nume_produs.split('"')[0]

        imagine_produs = info_produs.split('src="')[1]
        imagine_produs = imagine_produs.split('"')[0]

        info_pret = item.split('<div class="left_vertical_promozone_price"><span class="promozone_price">')[1]
        info_pret = info_pret.split('</span>')[0]
        dict_promotion = {"nume_produs": nume_produs, "pret_produs": info_pret, "link_produs": link_produs,
                          "imagine_produs": imagine_produs, "_id_principal_category": id_principal,
                          "_id": "evo_i{}".format(id_curent)}
        id_curent += 1
        list_of_dict_promotion.append(dict_promotion)
    return list_of_dict_promotion, id_curent


def get_dict_categories(str_principal_bar):
    list_of_dict_principal_categories = []
    list_of_dict_second_categories = []
    list_of_dict_promotions = []
    lines = str_principal_bar.split('<li data-submenu-id=')
    id_int_princ = 0
    id_int_sec = 0
    id_int_prom = 0
    for line in lines[1:]:
        new_line = line.replace('\n', '')
        if '<a class="" style="color:red;" href="/asigurari/">Asigurari</a>' in new_line \
                or '<a class="" style="" href="/servicii/">Servicii</a>' in new_line \
                or '<a class="" style="color: green" href="/resigilate-produse-resigilate/">Resigilate</a>' in new_line:
            continue
        splited_line = new_line.split('class="popover hidden"')
        info_principal_category = splited_line[0].split('href="')[1]
        link_title_principal_category = info_principal_category.split('"')[0]
        title_principal_category = info_principal_category.split('>')[1]
        title_principal_category = title_principal_category.split('<')[0]
        list_of_dict_principal_categories.append(
            {"nume_categorie": title_principal_category, "resursa_categorie": link_title_principal_category,
             "_id": "evo_p{}".format(id_int_princ)})
        id_int_princ += 1
        splited_line = splited_line[1].split('CELE MAI ACCESATE</span><ul><li><a')[1]
        info_second_category = splited_line.split('<span>ALTE CATEGORII')
        list_promotions = new_line.split('II</span><div class="left_vertical_promozone')[1]
        list_dict_promotions, id_int_prom = get_dict_promotions(list_promotions, "evo_p{}".format(id_int_princ - 1),
                                                                id_int_prom)
        for prom in list_dict_promotions:
            list_of_dict_promotions.append(prom)
        info_second_category = info_second_category[0].split('href="')
        for second_category in info_second_category:
            if second_category.strip() == "":
                continue
            link_second_category = second_category.split('">')[0]
            titlu_second_category = second_category.split('">')[1]
            if '(' in titlu_second_category and ')' in titlu_second_category:
                titlu_second_category = titlu_second_category.split('(')[0]
            else:
                continue
            list_of_dict_second_categories.append(
                {"nume_subcategorie": titlu_second_category, "resursa_subcategorie": link_second_category,
                 "_id": "evo_s{}".format(id_int_sec), "_id_principal_category": "evo_p{}".format(id_int_princ - 1)})
            id_int_sec += 1

    return list_of_dict_principal_categories, list_of_dict_second_categories, list_of_dict_promotions


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
            if "<div" in new_line and "id" in new_line and '"product_grid"' in new_line:
                found_div = 1
            if found_div == 1:
                if found_current_item == 1:
                    if 'class="nice_product_container"' not in new_line:
                        str_items += new_line
                        str_items += '\n'
                    else:
                        found_current_item = 0
                        str_items += new_line.split('<div class="nice_product_container"')[0]
                        str_items += '\n'
                        list_items.append(str_items)
                        str_items = ""
                if '<div class="nice_product_container"' in new_line:
                    str_items += new_line.split('<div class="nice_product_container"')[1]
                    str_items += '\n'
                    found_current_item = 1
        if "</body" in new_line:
            found_body = 0
    return list_items


def get_dict_item(item, id_item, id_second, id_princ):
    dict_item = {}
    item = item.replace('\n', '')
    print item
    try:
        if '<div class="npi_image">' in item:
            info_image = item.split('<div class="npi_image">')[1]
            info_image = info_image.split('<div class="npi_name')[0]
            nume_produs = info_image.split('title="')[1]
            nume_produs = nume_produs.split('"')[0]
            dict_item.update({"nume_produs": nume_produs})

            link_produs = info_image.split('href="')[1]
            link_produs = link_produs.split('"')[0]
            link_produs = "www.evomag.ro" + link_produs
            dict_item.update({"link_produs": link_produs})

            imagine_produs = info_image.split('src="')
            if len(imagine_produs) == 3:
                imagine_produs = imagine_produs[2]
            else:
                imagine_produs = imagine_produs[1]
            imagine_produs = imagine_produs.split('"')[0]
            dict_item.update({"imagine_produs": imagine_produs})

        if '<div class="price_block_list">' in item:
            pret_produs = []
            info_price = item.split('<div class="price_block_list">')[1]
            info_price = info_price.split('<div class="npi_stock')[0]
            pret_vechi = info_price.split('<span class="old_price')[1]
            pret_vechi = pret_vechi.split('</span>')[0]
            digits = string.digits
            ok = 0
            for chr in pret_vechi:
                if chr in digits:
                    ok = 1
            if ok == 1:
                pret_vechi = pret_vechi.split('&nbsp;', 1)[1]
                pret_vechi = pret_vechi.split('&nbsp;')[0]
            else:
                pret_vechi = None

            pret_nou = info_price.split('<span class="real_price">')[1]
            pret_nou = pret_nou.split('</span>')[0]

            ok = 0
            for chr in pret_nou:
                if chr in digits:
                    ok = 1

            if ok == 0:
                pret_nou = None

            timestamp = datetime.datetime.utcfromtimestamp(int(time.time()))
            pret_produs.append(pret_vechi)
            pret_produs.append(pret_nou)
            pret_produs.append(timestamp)

            dict_item.update({"pret_produs": [pret_produs]})

        if '<div class="stoc_produs">' in item:
            info_stoc_produs = item.split('<div class="stoc_produs">')[1]
            info_stoc_produs = info_stoc_produs.split('class="')[1]
            info_stoc_produs = info_stoc_produs.split('</span>')[0]
            info_stoc_produs = info_stoc_produs.split('">')[1]
            info_stoc_produs = info_stoc_produs.strip()
            dict_item.update({"valabilitate_produs": info_stoc_produs})

        dict_item.update(
            {"_id": "evo_i{}".format(id_item), "_id_principal_category": id_princ, "_id_second_category": id_second})
        return dict_item
    except Exception as e:
        print "error", e
        print "item_error", item
        return None


def insert_categories():
    # db_comit_principal = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["principal_categories_evomag"]
    # db_comit_second = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["second_categories_evomag"]
    # db_comit_promotions = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["promotions_evomag"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db_comit_principal = db.principal_categories_evomag
    db_comit_second = db.second_categories_evomag
    db_comit_promotions = db.promotions_evomag
    data = http_data("www.evomag.ro", "/")
    str_principal_bar = get_resourse_principal_bar(data)
    list_of_dict_principal_categories, list_of_dict_second_categories, list_of_dict_promotions = get_dict_categories(
        str_principal_bar)
    for principal_category in list_of_dict_principal_categories:
        inserted = db_comit_principal.insert_one(principal_category)
    for second_category in list_of_dict_second_categories:
        inserted = db_comit_second.insert_one(second_category)
    for promotion_item in list_of_dict_promotions:
        inserted = db_comit_promotions.insert_one(promotion_item)
    # print list_of_dict_principal_categories
    # print list_of_dict_second_categories
    # print list_of_dict_promotions


def insert_items():
    # db_comit_second = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["second_categories_evomag"]
    # db_comit_items = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["items_evomag"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db_comit_items = db.items_evomag
    db_comit_second = db.second_categories_evomag
    id_int = db_comit_items.find().count() + 1
    second_category_db = db_comit_second.find(no_cursor_timeout=True)
    list_of_second_category = []
    for category in second_category_db:
        list_of_second_category.append(category)
    for category in list_of_second_category:
        dict_category_db = category
        print "from db", dict_category_db
        resursa = dict_category_db["resursa_subcategorie"]
        data_items = http_data("www.evomag.ro", resursa)
        time.sleep(15)
        list_items = get_content_items(data_items)
        for item in list_items:
            dict_item = get_dict_item(item, id_int, dict_category_db["_id"], dict_category_db["_id_principal_category"])
            print dict_item
            id_int += 1
            if dict_item is not None:
                inserted = db_comit_items.insert_one(dict_item)


if __name__ == '__main__':
    handler = open("active_evomag", "w")
    # handler.write("{}".format(int(time.time())))
    handler.close()
    while True:
        try:
            if os.path.exists("stop_evomag"):
                print("Killing evomag in 5 seconds...")
                time.sleep(5)
                os.remove("stop_evomag")
                break
            if os.path.exists("start_evomag"):
                print("Found start_evomag, cooldown for 5 seconds and starting the job...")

                time.sleep(5)
                os.remove("start_evomag")
                if os.path.exists("finished_evomag"):
                    os.remove("finished_evomag")

                h = open("running_evomag", "w")
                # h.write("{}".format(int(time.time())))
                h.close()

                insert_items()
                print("Job has been finished...")

                os.remove("running_evomag")

                h = open("finished_evomag", "w")
                # h.write("{}".format(int(time.time())))
                h.close()
        except Exception as e:
            print("Exception: {}".format(e))
        print("Sleeping for 1 minute")
        time.sleep(60)
    os.remove("active_evomag")
    # insert_categories()  # - inserted only one - se insereaza categoriile principale, secundare si itemii promotionali