import json
import os
import socket
import string

from bson import json_util
import sys
import re
import pymongo
import datetime
import subprocess
import signal
import atexit
import time
import facebook

MONGODB_URI = "mongodb://heroku_xzc0r78w:iipvtiu45d221kjg9fjjtqi7r9@ds243812.mlab.com:43812/heroku_xzc0r78w?retryWrites=false"
SCRAPPERS = {
    "emag":"emag_scrapping/emag_scrapping.py",
    "evomag":"evomag_scrapping/evomag_scrapping.py",
}
running_scrappers = {}
dict_mapping_emag_evomag = {
    "p_0": ["evo_p14"],
    "p_1": ["evo_p0", "evo_p1"],
    "p_3": ["evo_p6"],
    "p_4": ["evo_p2", "evo_p8", "evo_p9"],
    "p_6": ["evo_p13"],
    "p_7": ["evo_p15"],
    "p_8": ["evo_p3", "evo_p4", "evo_p5", "evo_p7", "evo_p10", "evo_p11"],
    "p_9": ["evo_p16"],
    "p_10": ["evo_p12"]
}


class TCPServer:
    def __init__(self, host='0.0.0.0', port=int(sys.argv[1])):
        self.host = host
        self.port = port

    def response_function(self, conn):
        data = conn.recv(1024)
        # aici primesc requestul
        print "Request: \n", data
        http_server = HTTPServer()
        response = http_server.handle_request(data)
        # aici dau response
        conn.sendall(response)
        conn.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        print "Listening at", s.getsockname()
        while True:

            # conn, addr = s.accept()
            # print "Connected by ", addr
            # thr = Thread(target=self.response_function, args=(conn,))
            # thr.start()

            conn, addr = s.accept()
            print "Connected by ", addr
            data = conn.recv(4096)
            # aici primesc requestul
            print "Request: \n", data
            http_server = HTTPServer()
            response = http_server.handle_request(data)
            # aici dau response
            conn.sendall(response)
            conn.close()


def receive_all(sock, chunk_size=1024):
    chunks = []
    while True:
        chunk = sock.recv(int(chunk_size))
        if chunk:
            chunks.append(chunk)
        else:
            break
    _str = ''.join(chunks)
    my = _str.split("\r\n")[-1]
    return json.loads(my)


def http_data_post(url, resursa, requestline, encoding='utf-8'):
    port = 80
    crlf = '\r\n\r\n'

    def make_header(requestline):
        #requestline = "source=google_shopping&country=us&topic=search_results&key=id&values=iphone&timeout=1&token=MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ" 
        requestline = json.dumps(requestline, indent=4)
        headers = [
            'POST %s HTTP/1.0' % resursa,
            'Content-Type: application/json',
            'Content-Length: {}'.format(len(requestline)),
            'User-Agent: Chrome/83.0.4103.61',
            'Accept: */*',
            'Host: %s' % url,
            'Accept-Encoding: gzip, deflate, br',
            'Connection: keep-alive',

            # 'User-Agent: Chrome/83.0.4103.61',
            #'Accept: application/json',
            #'Connection: keep-alive',
            #'Content-Type: application/x-www-form-urlencoded',
            #'Content-Length: {}'.format(len(requestline)),
        ]                                                                                                                                                     
        header = '\n'.join(headers)
        header = header.strip()
        header += crlf
        header += '{}'.format(requestline)
        return header

    def request(header):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((url, port))
        try:
            sock.sendall(header)
            str_ = receive_all(sock)
        finally:
            sock.shutdown(1)
            sock.close()
        return str_

    str_final = request(make_header(requestline))
    return str_final


def http_data_get(url, resursa, requestline, encoding='utf-8'):
    port = 80
    crlf = '\r\n\r\n'

    def make_header(requestline):
        headers = [
            'GET %s/%s HTTP/1.0' % (resursa, requestline), 
            'User-Agent: Chrome/83.0.4103.61',
            'Accept: */*',
            'Host: %s' % url,
            'Accept-Encoding: gzip, deflate, br',
            'Connection: keep-alive',

            # 'User-Agent: Chrome/83.0.4103.61',
            #'Accept: application/json',
            #'Connection: keep-alive',
            #'Content-Type: application/x-www-form-urlencoded',
            #'Content-Length: {}'.format(len(requestline)),
        ]                                                                                                                                                     
        header = '\n'.join(headers)
        header = header.strip()
        header += crlf
        return header

    def request(header):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((url, port))
        try:
            sock.sendall(header)
            str_ = receive_all(sock)
        finally:
            sock.shutdown(1)
            sock.close()
        return str_

    str_final = request(make_header(requestline))
    return str_final


def facebook_post(message):
    try:
        #{"access_token": "EAAIQW0NryWABAKs73jbuYAgfzZCMLuD9MbHmdRNwLfZCKQKNIZCoTfBxxGqryZCCmLM357doZB2GPx00DiOeQ1dOcK2Np1niZA7RV8sSjGMs7lp3dOyQwUSPvylHhjqtv8ZCI8XuK3enWgUjS3oD02FfrdvBgPAv9ElYh4fpsRRRgZDZD","token_type": "bearer", "expires_in": 5102265}
        graph = facebook.GraphAPI(access_token="EAAIQW0NryWABAKs73jbuYAgfzZCMLuD9MbHmdRNwLfZCKQKNIZCoTfBxxGqryZCCmLM357doZB2GPx00DiOeQ1dOcK2Np1niZA7RV8sSjGMs7lp3dOyQwUSPvylHhjqtv8ZCI8XuK3enWgUjS3oD02FfrdvBgPAv9ElYh4fpsRRRgZDZD", version="3.0")
        graph.put_object(
           parent_object="109369880809577",
           connection_name="feed",
           message='{} #comit'.format(message),
        )
        return "Message Posted With Success", 200, None
    except Exception as e:
        return str(e), 501, None


def post_message(request):
    if request.method != "GET":
        return "Error 501. Method not implemented", 501, None

    _body = request.parsed_uri['params']
    if "message" not in _body:
        return "Bad Request. Please subimt message param", 400, None
    _body = _body['message']
    _body = _body.replace("%22", '"')
    _body = _body.replace("%20", " ")
    _body = _body.replace('%26', "&")
    _body = _body.replace("%2F", "/")
    if not _body or len(_body) == 0:
        return "Bad Request! Please submit a message", 400, None
    msg, c, h = facebook_post(_body)
    return msg, c, h


def search_product_api(request):
    if request.method != "GET":
        return "Error 501. Method not implemented", 501, None
    
    term = ""
    if "content_search" in request.parsed_uri["params"]:
        term = request.parsed_uri["params"]["content_search"].lower()
    term = term.split("%20")

    myterm = []
    for word in term:
        word = word.replace(",", "")
        word = word.replace('"', "")
        myterm.append(word)
    
    term = " ".join(myterm).strip()

    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db_comit_items_amazon = db.items_amazon
    db_comit_items_google = db.items_google
    
    google_shopping_request_line = {"source":"google_shopping", "country":"us", "topic":"search_results", "key":"term", "values":"{}".format(term), "timeout":"1", "token":"MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ"}
    amazon_request_line = {"source":"amazon", "country":"gb", "topic":"search_results", "key":"term", "values":"{}".format(term), "timeout":"1", "token":"MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ"}
    
    google_job_id = http_data_post("api.priceapi.com", "/v2/jobs", google_shopping_request_line)["job_id"]
    amazon_job_id = http_data_post("api.priceapi.com", "/v2/jobs", amazon_request_line)["job_id"]
    
    time.sleep(2)
    
    requestline = "{}?token=MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ".format(amazon_job_id)
    response_json = http_data_get("api.priceapi.com", "/v2/jobs", requestline)["status"]
    if response_json != "finished":
        while response_json != "finished":
            response_json = http_data_get("api.priceapi.com", "/v2/jobs", requestline)["status"]
            time.sleep(2)
    
    requestline = "{}?token=MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ".format(google_job_id)
    response_json = http_data_get("api.priceapi.com", "/v2/jobs", requestline)["status"]
    if response_json != "finished":
        while response_json != "finished":
            response_json = http_data_get("api.priceapi.com", "/v2/jobs", requestline)["status"]
            time.sleep(2)            
           
    
    
    amazon_job_download = "{}/download?token=MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ".format(amazon_job_id)
    amazon_content = http_data_get("api.priceapi.com", "/v2/jobs", amazon_job_download)
    #handler = open("{}_amazon_job_id_{}".format(term, amazon_job_id), "w")
    #handler.write("{}".format(json.dumps(http_data_get("api.priceapi.com", "/v2/jobs", amazon_job_download), indent=4)))
    #handler.close()
    
    google_download = "{}/download?token=MSISENUBCHJALBCTMNBJKAJYCJZALDUANFTLRADNYDNUMKRCURGAYGQOWCEOYUUQ".format(google_job_id)
    google_content = http_data_get("api.priceapi.com", "/v2/jobs", google_download)
    #handler = open("{}_google_job_id_{}".format(term, google_job_id), "w")
    #handler.write("{}".format(json.dumps(http_data_get("api.priceapi.com", "/v2/jobs", google_download), indent=4)))
    #handler.close()

    amazon_items = []
    googleshop_items = []

    if "results" in amazon_content:
        results = amazon_content["results"]
        if "content" in results[0]:
            content = results[0]["content"]
            url = ""
            search_results = ""

            if "url" in content:
                url = content["url"]
            if "search_results" in content:
                search_results = content["search_results"]

            if isinstance(search_results, list):
                for item in search_results:
                    to_append_items = {}
                    to_append_items["nume_produs"] = item.get("name", "")
                    to_append_items["pret_produs"] = [["{} {}".format(item.get("max_price", ""), item.get("currency", "")), "{} {}".format(item.get("min_price", ""), item.get("currency", "")), datetime.datetime.utcfromtimestamp(int(time.time()))]]
                    #to_append_items['pret_produs'] = "Max price: {} {} | Min price: {} {}".format(item.get("max_price", ""), item.get("currency", ""), item.get("min_price", ""), item.get("currency", ""))
                    to_append_items["rating_produs"] = item.get("review_rating", "")
                    to_append_items["link_produs"] = item.get("url", "")
                    to_append_items["imagine_produs"] = item.get("image_url", "")
                    to_append_items["reviews_produs"] = item.get("review_count", "")
                    amazon_items.append(to_append_items)

    if "results" in google_content:
        results = google_content["results"]

        if "content" in results[0]:
            content = results[0]["content"]
            url = ""
            search_results = ""

            if "url" in content:
                url = content["url"]
            if "search_results" in content:
                search_results = content["search_results"]

            if isinstance(search_results, list):
                for item in search_results:
                    if "price_with_shipping" not in item:
                        continue
                    to_append_items = {}
                    to_append_items["nume_produs"] = item.get("name", "")
                    price1 = item.get("price", 0)
                    if price1 is None:
                        price1 = 0
                    price1 = float(price1)
                    price2 = item.get("price_with_shipping", 0)
                    if price2 is None:
                        price2 = 0
                    price2 = float(price2)
                    to_append_items["pret_produs"] = [[None, "{} {}".format(max(price1, price2), item.get("currency", "")), datetime.datetime.utcfromtimestamp(int(time.time()))]]
                    #to_append_items["pret_produs"] = "{} {}".format(max(price1, price2), item.get("currency", ""))
                    to_append_items["rating_produs"] = item.get("shop_review_rating", "")                
                    to_append_items["link_produs"] = item.get("url", "")
                    to_append_items["imagine_produs"] = item.get("shop_url", "")
                    to_append_items["reviews_produs"] = item.get("shop_review_count", "")
                    googleshop_items.append(to_append_items)


    id_int = db_comit_items_amazon.find().count() + 1
    for item in amazon_items:
        if db_comit_items_amazon.find({'nume_produs': item['nume_produs']}).count() == 0:
            item.update({"_id": "amazon_i{}".format(id_int)})
            inserted = db_comit_items_amazon.insert_one(item)
            id_int += 1
        else:
            old_items = db_comit_items_amazon.find({'nume_produs': item['nume_produs']})
            for old_item in old_items:
                new_list = []
                for item_list in old_item['pret_produs']:
                    new_list.append(item_list)
                new_list.append(item['pret_produs'][0])
                #print "update", (id_int, new_list, dict_info_item)
                db_comit_items_amazon.update_one({"_id": old_item["_id"]}, {"$set": {"pret_produs": new_list}})

    id_int = db_comit_items_google.find().count() + 1
    for item in googleshop_items:
        if db_comit_items_google.find({'nume_produs': item['nume_produs']}).count() == 0:
            item.update({"_id": "google_i{}".format(id_int)})
            inserted = db_comit_items_google.insert_one(item)
            id_int += 1
        else:
            old_items = db_comit_items_google.find({'nume_produs': item['nume_produs']})
            for old_item in old_items:
                new_list = []
                for item_list in old_item['pret_produs']:
                    new_list.append(item_list)
                new_list.append(item['pret_produs'][0])
                #print "update", (id_int, new_list, dict_info_item)
                db_comit_items_google.update_one({"_id": old_item["_id"]}, {"$set": {"pret_produs": new_list}})

    for x in range(len(amazon_items)):
        amazon_items[x]["pret_produs"] = "Max price: {} | Min price: {}".format(amazon_items[x]["pret_produs"][-1][0], amazon_items[x]["pret_produs"][-1][1])

    for x in range(len(googleshop_items)):
        #for i in range(len(googleshop_items[x]["pret_produs"])):
        #googleshop_items[x]["pret_produs"][i][2] = str(googleshop_items[x]["pret_produs"][i][2])
        googleshop_items[x]["pret_produs"] = googleshop_items[x]["pret_produs"][-1][1]

    result_dict = {
        "amazon":amazon_items,
        "google":googleshop_items
    }

    return json.dumps(result_dict, default=json_util.default), 200, None


def search_product(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items = db.items_emag
        string_to_search = ""
        if "content_search" in request.parsed_uri["params"]:
            string_to_search = request.parsed_uri["params"]["content_search"]
        list_words_to_search = string_to_search.split("%20")

        myquery = []
        for word in list_words_to_search:
            word = word.replace(",", "")
            word = word.replace('"', "")
            print word

        word_count = len(list_words_to_search)
        if word_count <= 3:
            word_70_procent = 1
            word_80_procent = 1
            word_100_procent = word_count
        else:
            word_70_procent = int(word_count * 0.7)
            word_80_procent = int(word_count * 0.8)
            word_100_procent = word_count

        list_70_procent = []
        list_80_procent = []
        list_100_procent = []
        for word in list_words_to_search[:word_70_procent]:
            list_70_procent.append(word)
        if word_70_procent != word_80_procent:
            for word in list_words_to_search[word_70_procent:word_80_procent]:
                list_80_procent.append(word)
        else:
            for word in list_words_to_search[word_70_procent:]:
                list_100_procent.append(word)
        if word_70_procent != word_80_procent != word_100_procent:
            for word in list_words_to_search[word_80_procent:word_100_procent]:
                list_100_procent.append(word)
        for word in list_70_procent:
            myquery.append({"nume_produs": {'$in': [re.compile(word, re.IGNORECASE)]}})

        result = db_comit_items.aggregate([{"$match": {"$and": myquery}}])
        final_result = []
        current_product_70 = []
        current_product_80 = []
        current_product_100 = []
        for product in result:
            """for i in range(len(product["pret_produs"])):
                product["pret_produs"][i][2] = str(product["pret_produs"][i][2])"""
            current_product_70.append(product)

        for result_current in current_product_70:
            for word in list_80_procent:
                if word.upper() in result_current['nume_produs'].upper() and result_current not in current_product_80:
                    current_product_80.append(result_current)
                    current_product_70.remove(result_current)
            for word in list_100_procent:
                if word.upper() in result_current['nume_produs'].upper() and result_current not in current_product_100:
                    current_product_100.append(result_current)
                    if result_current in current_product_70:
                        current_product_70.remove(result_current)
                    if result_current in current_product_80:
                        current_product_80.remove(result_current)
        for current_result in current_product_100:
            final_result.append(current_result)
        for current_result in current_product_80:
            final_result.append(current_result)
        for current_result in current_product_70:
            final_result.append(current_result)
        status_code = 200
        return json.dumps(final_result, default=json_util.default), status_code, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_product_from_category_emag(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_emag = db.items_emag
        db_comit_principal_category = db.principal_categories
        category_to_print = ""
        if "category_name" in request.parsed_uri["params"]:
            category_to_print = request.parsed_uri["params"]["category_name"]
        if category_to_print == "undefined":
            return None, 200, None
        category_to_print = category_to_print.replace('%20', ' ')
        category_to_print = category_to_print.replace('%26', '&')
        category_to_print = category_to_print.replace('%2F', '/')
        category_dict = db_comit_principal_category.find_one({'nume_categorie': re.compile(category_to_print, re.IGNORECASE)})
        if not isinstance(category_dict, dict):
            return None, 200, None
        id_category = category_dict['_id']
        list_result = []
        for result in db_comit_items_emag.find({'_id_principal_category': id_category}):
            list_result.append(result)
        return json.dumps(list_result, default=json_util.default), 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_product_from_category_evomag(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_evomag = db.items_evomag
        db_comit_principal_category = db.principal_categories_evomag
        category_to_print = ""
        if "category_name" in request.parsed_uri["params"]:
            category_to_print = request.parsed_uri["params"]["category_name"]
        if category_to_print == "undefined":
            return None, 200, None
        category_to_print = category_to_print.replace('%20', ' ')
        category_to_print = category_to_print.replace('%26', '&')
        category_to_print = category_to_print.replace('%2F', '/')
        category_dict = db_comit_principal_category.find_one({'nume_categorie': re.compile(category_to_print, re.IGNORECASE)})
        if not isinstance(category_dict, dict):
            return None, 200, None
        id_category = category_dict['_id']
        list_result = []
        for result in db_comit_items_evomag.find({'_id_principal_category': id_category}):
            list_result.append(result)
        return json.dumps(list_result, default=json_util.default), 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_product_from_subcategory_emag(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_emag = db.items_emag
        db_comit_second_category = db.second_categories
        category_to_print = ""
        if "subcategory_name" in request.parsed_uri["params"]:
            category_to_print = request.parsed_uri["params"]["subcategory_name"]
        if category_to_print == "undefined":
            return None, 200, None
        category_to_print = category_to_print.replace('%20', ' ')
        category_to_print = category_to_print.replace('%26', '&')
        category_to_print = category_to_print.replace('%2F', '/')
        category_dict = db_comit_second_category.find_one({'nume_subcategorie': re.compile(category_to_print, re.IGNORECASE)})
        if not isinstance(category_dict, dict):
            return None, 200, None
        id_category = category_dict['_id']
        list_result = []
        for result in db_comit_items_emag.find({'_id_second_category': id_category}):
            list_result.append(result)
        return json.dumps(list_result, default=json_util.default), 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_product_from_subcategory_evomag(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_evomag = db.items_evomag
        db_comit_second_category = db.second_categories_evomag
        category_to_print = ""
        if "subcategory_name" in request.parsed_uri["params"]:
            category_to_print = request.parsed_uri["params"]["subcategory_name"]
        if category_to_print == "undefined":
            return None, 200, None
        category_to_print = category_to_print.replace('%20', ' ')
        category_to_print = category_to_print.replace('%26', '&')
        category_to_print = category_to_print.replace('%2F', '/')
        category_dict = db_comit_second_category.find_one({'nume_subcategorie': re.compile(category_to_print, re.IGNORECASE)})
        if not isinstance(category_dict, dict):
            return None, 200, None
        id_category = category_dict['_id']
        list_result = []
        for result in db_comit_items_evomag.find({'_id_second_category': id_category}):
            list_result.append(result)
        return json.dumps(list_result, default=json_util.default), 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_offers(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_evomag = db.items_evomag
        db_comit_items_emag = db.items_emag
        db_comit_items_offer = db.promotions_evomag
        link = request.parsed_uri['params']
        link = link['product_link']
        tag_emag = False
        tag_evomag = False
        tag_nothing = False

        if 'emag' in link:
            tag_emag = True
        else:
            if 'evomag' in link:
                tag_evomag = True
            else:
                tag_nothing = True

        if tag_emag == True:
            items_emag = db_comit_items_emag.find({'link_produs': link})
            if items_emag.count() == 0:
                return None, 200, None
            else:
                categorie_produs = ""
                for item in items_emag:
                    categorie_produs = item['_id_principal_category']
                    break
                list_items_to_return = []
                if categorie_produs in dict_mapping_emag_evomag:
                    for associative_id in dict_mapping_emag_evomag[categorie_produs]:
                        print associative_id
                        item = db_comit_items_offer.find({'_id_principal_category': associative_id})
                        if len(dict_mapping_emag_evomag[categorie_produs]) >= 2:
                            if len(list_items_to_return) == 2:
                                break
                            else:
                                for it in item:
                                    if len(list_items_to_return) == 2:
                                        break
                                    else:
                                        list_items_to_return.append(it)
                        else:
                            for it in item:
                                if len(list_items_to_return) == 2:
                                    break
                                else:
                                    list_items_to_return.append(it)
                    return json.dumps(list_items_to_return, default=json_util.default), 200, None
                else:
                    return None, 200, None

        if tag_evomag == True:
            items_evomag = db_comit_items_evomag.find({'link_produs': link})
            if items_evomag.count() == 0:
                return None, 200, None
            else:
                categorie_produs = ""
                for item in items_evomag:
                    categorie_produs = item['_id_principal_category']
                    break
                list_items_to_return = []
                item = db_comit_items_offer.find({'_id_principal_category': categorie_produs})
                for it in item:
                    if len(list_items_to_return) == 2:
                        break
                    else:
                        list_items_to_return.append(it)
                return json.dumps(list_items_to_return, default=json_util.default), 200, None

        if tag_nothing == False:
            return None, 200, None

        return None, 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_similar_from_all(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_evomag = db.items_evomag
        db_comit_items_emag = db.items_emag
        db_comit_items_amazon = db.items_amazon
        db_comit_items_google = db.items_google
        link = request.parsed_uri['params']
        link = link['product_link']
        tag_emag = False
        tag_evomag = False
        tag_nothing = False

        if 'emag' in link:
            tag_emag = True
        else:
            if 'evomag' in link:
                tag_evomag = True
            else:
                tag_nothing = True
        myquery = []
        if tag_emag == True:
            items_emag = db_comit_items_emag.find({'link_produs': link})
            if items_emag.count() == 0:
                return None, 200, None
            else:
                nume_produs = ""
                for item in items_emag:
                    nume_produs = item['nume_produs']
                    break
                list_words_to_search = nume_produs.split(' ')

                len_list = len(list_words_to_search)
                if len_list <= 4:
                    len_max = len_list
                else:
                    len_max = 4
                for word in list_words_to_search[:len_max]:
                    word = word.replace(",", "")
                    word = word.replace('"', "")
                    word = word.replace("(", "")
                    word = word.replace(")", "")
                    word = '.*' + word + '.*'
                    myquery.append({"nume_produs": {"$in": [re.compile(word, re.IGNORECASE)]}})

        if tag_evomag == True:
            items_evomag = db_comit_items_evomag.find({'link_produs': link})
            if items_evomag.count() == 0:
                return None, 200, None
            else:
                nume_produs = ""
                for item in items_evomag:
                    nume_produs = item['nume_produs']
                    break

                list_words_to_search = nume_produs.split(' ')
                len_list = len(list_words_to_search)
                if len_list <= 6:
                    len_max = len_list
                else:
                    len_max = 6
                for word in list_words_to_search[:len_max]:
                    word = word.replace(",", "")
                    word = word.replace('"', "")
                    word = word.replace("(", "")
                    word = word.replace(")", "")
                    word = '.*' + word + '.*'
                    myquery.append({"nume_produs": {'$in': [re.compile(word, re.IGNORECASE)]}})

        if tag_nothing == False:
            current_result = []

            result = db_comit_items_google.find({"$or": myquery})
            for product in result:
                new_product = {}
                new_product.update({'nume_produs': product['nume_produs'], 'link_produs': product['link_produs']})
                pret_produs = product['pret_produs']
                len_list_price = len(pret_produs)
                last_price = pret_produs[len_list_price-1][1]
                new_product.update({'pret_produs': last_price})
                current_result.append(product)
                break

            result = db_comit_items_amazon.find({"$or": myquery})
            for product in result:
                new_product = {}
                new_product.update({'nume_produs': product['nume_produs'], 'link_produs': product['link_produs']})
                pret_produs = product['pret_produs']
                len_list_price = len(pret_produs)
                last_price = pret_produs[len_list_price-1][1]
                new_product.update({'pret_produs': last_price})
                current_result.append(product)
                break

            result = db_comit_items_evomag.find({"$or": myquery})
            for product in result:
                new_product = {}
                new_product.update({'nume_produs': product['nume_produs'], 'link_produs': product['link_produs']})
                pret_produs = json.loads(product['pret_produs'])
                len_list_price = len(pret_produs)
                last_price = pret_produs[len_list_price-1][1]
                new_product.update({'pret_produs': last_price})
                current_result.append(product)
                break

            result = db_comit_items_emag.find({"$or": myquery})
            for product in result:
                new_product = {}
                new_product.update({'nume_produs': product['nume_produs'], 'link_produs': product['link_produs']})
                pret_produs = json.loads(product['pret_produs'])
                len_list_price = len(pret_produs)
                last_price = pret_produs[len_list_price-1][1]
                new_product.update({'pret_produs': last_price})
                current_result.append(product)
                break

            return json.dumps(current_result, default=json_util.default), 200, None
        else:
            return None, 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def get_price_fluctuation(request):
    if request.method == "GET":
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        db_comit_items_evomag = db.items_evomag
        db_comit_items_emag = db.items_emag
        link = request.parsed_uri['params']
        link = link['product_link']
        tag_emag = False
        tag_evomag = False
        tag_nothing = False

        if 'emag' in link:
            tag_emag = True
        else:
            if 'evomag' in link:
                tag_evomag = True
            else:
                tag_nothing = True

        digits = string.digits
        def check_contains_digit(string):
            for chr in string:
                if chr in digits:
                    return True
            return False

        if tag_emag == True:
            items_emag = db_comit_items_emag.find({'link_produs': link})
            if items_emag.count() == 0:
                return None, 200, None
            else:
                for item in items_emag:
                    new_item = item
                    pret_produse = json.loads(new_item['pret_produs'])
                    current_list = []
                    for i in range(len(pret_produse)-1, -1, -1):
                        for j in range(len(pret_produse[i])-1):
                            if pret_produse[i][j] is not None:
                                if check_contains_digit(pret_produse[i][j]) and len(pret_produse[i][j]) <= 10:
                                    print convert_pret_to_float(pret_produse[i][j])
                                    current_list.append(convert_pret_to_float(pret_produse[i][j]))
                    if len(current_list) == 0:
                        return None, 200, None
                    if len(current_list) == 1:
                        new_item['pret_produs'] = []
                        for i in range(3):
                            new_item['pret_produs'].append(current_list[0])
                    if len(current_list) == 2:
                        new_item['pret_produs'] = []
                        new_item['pret_produs'].append(float(current_list[0] + current_list[1])/ 2)
                        new_item['pret_produs'].append(current_list[0])
                        new_item['pret_produs'].append(current_list[1])
                    if len(current_list) == 3:
                        new_item['pret_produs'] = current_list[-3:]
                    print new_item['pret_produs']
                    return json.dumps(new_item, default=json_util.default), 200, None

        if tag_evomag == True:
            items_evomag = db_comit_items_evomag.find({'link_produs': link})
            if items_evomag.count() == 0:
                return None, 200, None
            else:
                for item in items_evomag:
                    new_item = item
                    pret_produse = json.loads(new_item['pret_produs'])
                    current_list = []
                    for i in range(len(pret_produse) - 1, -1, -1):
                        for j in range(len(pret_produse[i]) - 1):
                            if pret_produse[i][j] is not None:
                                if check_contains_digit(pret_produse[i][j]) and len(pret_produse[i][j]) <= 10:
                                    print convert_pret_to_float(pret_produse[i][j])
                                    current_list.append(convert_pret_to_float(pret_produse[i][j]))
                    if len(current_list) == 0:
                        return None, 200, None
                    if len(current_list) == 1:
                        new_item['pret_produs'] = []
                        for i in range(3):
                            new_item['pret_produs'].append(current_list[0])
                    if len(current_list) == 2:
                        new_item['pret_produs'] = []
                        new_item['pret_produs'].append(float(current_list[0] + current_list[1])/ 2)
                        new_item['pret_produs'].append(current_list[0])
                        new_item['pret_produs'].append(current_list[1])
                    if len(current_list) == 3:
                        new_item['pret_produs'] = current_list[-3:]
                    print new_item['pret_produs']
                    return json.dumps(new_item, default=json_util.default), 200, None

        if tag_nothing == True:
            return None, 200, None

        return None, 200, None
    else:
        return "Error 501. Method not implemented", 501, None


def generate_item_in_rss_feed(item):
    old_price = ""
    new_price = ""
    ignore = "ignore"
    preturi = item["pret_produs"]
    try:
        preturi = json.loads(preturi)
    except:
        pass
    if len(preturi):
        last = preturi[-1]
        if len(last) > 2:
            new_price = last[1]
            if last[0] is not None:
                old_price = last[0]
            else:
                if len(preturi) > 1:
                    last_last = preturi[-2]
                    old_price = last_last[1]
    item_title = item["nume_produs"]
    if item_title:
        item_title = item_title.encode("ascii", ignore)
    item_link = item.get("link_produs", "")
    if item_link:
        item_link = item_link.encode("ascii", ignore)
    imagine_produs = item.get("imagine_produs", "")
    if imagine_produs:
        imagine_produs = imagine_produs.encode("ascii", ignore)
    if old_price:
        old_price = old_price.encode("ascii", ignore)
    if new_price:
        new_price = new_price.encode("ascii", ignore)
    template_rss = """      <item>
        <title><![CDATA[ {item_title} ]]></title>
        <link>{item_link}</link>
        <description><![CDATA[ <table><tr><td><a href="{item_link}"><img src="{prod_img}" alt="" border="0" align="left" height="75" width="75" /></a></td><td style="text-decoration:none;"><p>Old Price: <span class="price">{old_price}</span> Special Price: <span class="price">{new_price}</span></p></td></tr></table> ]]></description>
        </item>
""".format(item_title=item_title, item_link=item_link, prod_img=imagine_produs, old_price=old_price,
            new_price=new_price)
    return template_rss


def generate_rss_feed(title, description, link, content):
    rss_head = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
    <channel>
    <title><![CDATA[ {content_title} ]]></title>
    <link>{content_link}</link>
    <description><![CDATA[ {content_descrition} ]]></description>
    <language>ro_RO</language>
    <docs>http://blogs.law.harvard.edu/tech/rss</docs>
""".format(content_title=title, content_descrition=description, content_link=link)
    rss_foot = """  </channel>
</rss>"""
    rss_content = "".join([generate_item_in_rss_feed(item) for item in content])
    rss_result = rss_head + rss_content + rss_foot
    # handler = open("{}_feed.xml".format(title.lower().replace(" ", "")), "w").write(rss_result)
    return rss_result


def convert_pret_to_float(pret):
    try:
        pret = pret.split()[0]
        int_part = pret.split(',')[0]
        if ',' in pret:
            float_part = pret.split(',')[1]
        else:
            float_part = 0
        int_part = int_part.replace('.', '')
        pret = int(int_part) + float(int(float_part)) / (pow(10, len(float_part)))
        return pret
    except:
        return 0


def check_kind_of_promotion(item):
    list_prices = json.loads(item['pret_produs'])
    if len(list_prices):
        last_price = list_prices[len(list_prices) - 1]
        if last_price[0] is None:
            current_price = convert_pret_to_float(last_price[1])
            if len(list_prices) >= 2:
                last_last_price = list_prices[len(list_prices) - 2]
                old_price = convert_pret_to_float(last_last_price[1])
                if old_price is not None:
                    if old_price > current_price:
                        return item
        else:
            if last_price[1] is None:
                return None
            else:
                current_price = convert_pret_to_float(last_price[1])
                old_price = convert_pret_to_float(last_price[0])
                if old_price > current_price:
                    return item
    return None


def get_news_emag(request):
    if request.method == "GET":

        def get_promotion_list_items():
            client = pymongo.MongoClient(MONGODB_URI)
            db = client.get_default_database()
            db_comit_items = db.items_emag
            list_for_rss = []
            for i in range(11):
                count_list = 0
                for item in db_comit_items.find({'_id_principal_category': "p_{}".format(i)}):
                    item_to_add = check_kind_of_promotion(item)
                    if item_to_add is not None:
                        list_for_rss.append(item)
                        count_list += 1
                    if count_list == 5:
                        break
            return list_for_rss

        rss_result = generate_rss_feed("Emag promotions", "Promotions for each category", "www.emag.ro", get_promotion_list_items())

        return rss_result, 200, {'Content-Type': 'application/rss+xml'}
    else:
        return "Error 501. Method not implemented", 501, None


def get_news_evomag(request):
    if request.method == "GET":

        def get_promotion_list_items():
            client = pymongo.MongoClient(MONGODB_URI)
            db = client.get_default_database()
            db_comit_items = db.items_evomag
            list_for_rss = []
            for i in range(17):
                count_list = 0
                for item in db_comit_items.find({'_id_principal_category': "evo_p{}".format(i)}):
                    item_to_add = check_kind_of_promotion(item)
                    if item_to_add is not None:
                        list_for_rss.append(item)
                        count_list += 1
                    if count_list == 5:
                        break
            return list_for_rss

        rss_result = generate_rss_feed("Evomag promotions", "Promotions for each category", "www.evomag.ro", get_promotion_list_items())

        return rss_result, 200, {'Content-Type': 'application/rss+xml'}
    else:
        return "Error 501. Method not implemented", 501, None


def activate_scrapper(request):
    if request.method == "GET":
        name = ""
        if "name" in request.parsed_uri["params"]:
            name = request.parsed_uri["params"]["name"].lower()
        if name != "":
            if name in SCRAPPERS:
                if name in running_scrappers:
                    return "The scrapper is already running", 400, None
                child = subprocess.Popen(["python", "{}".format(SCRAPPERS[name])])
                running_scrappers[name] = child.pid
                return "Starting request performed cu success!", 200, None
            else:
                return "{} is not a valid scrapper".format(name), 400, None
        else:
            return "Name has not been provided", 400, None
    else:
        return "Error 501. Method not implemented", 501, None


def run_scrapper(request):
    if request.method == "GET":
        name = ""
        if "name" in request.parsed_uri["params"]:
            name = request.parsed_uri["params"]["name"].lower()
        if name != "":
            if name in SCRAPPERS:
                if name not in running_scrappers:
                    return "Scrapper {} is not active".format(name), 400, None
                handler = open("start_{}".format(name), "w")
                handler.close()
                facebook_post(
                    "New products offers have arrived! Please check them out: https://comittw.herokuapp.com/news/{}".format(
                        name))
                return "Starting request performed cu success!", 200, None
            else:
                return "{} is not a valid scrapper".format(name), 400, None
        else:
            return "Name has not been provided", 400, None
    else:
        return "Error 501. Method not implemented", 501, None


def status_scrapper(request):
    if request.method == "GET":
        name = ""
        return_str = ""
        if "name" in request.parsed_uri["params"]:
            name = request.parsed_uri["params"]["name"].lower()
        if name != "":
            if name in SCRAPPERS:
                if name not in running_scrappers:
                    return_str = "{} is not active".format(name)
                    return return_str, 200, None
                if os.path.exists("active_{}".format(name)):
                    return_str += "{} is active... ".format(name)
                if not os.path.exists("active_{}".format(name)):
                    return_str += "{} is not active... ".format(name)
                if os.path.exists("start_{}".format(name)):
                    # handler = open("running_{}".format(name), "r")
                    # content = handler.read()
                    # handler.close()
                    # timestamp = datetime.datetime.utcfromtimestamp(int(content.strip(".")[0])*1000)
                    return_str += "{} is starting... ".format(name)
                if os.path.exists("stop_{}".format(name)):
                    # handler = open("running_{}".format(name), "r")
                    # content = handler.read()
                    # handler.close()
                    # timestamp = datetime.datetime.utcfromtimestamp(int(content.strip(".")[0])*1000)
                    return_str += "{} is stopping... ".format(name)

                if os.path.exists("running_{}".format(name)):
                    # handler = open("running_{}".format(name), "r")
                    # content = handler.read()
                    # handler.close()
                    # timestamp = datetime.datetime.utcfromtimestamp(int(content.strip(".")[0])*1000)
                    return_str += "{} is running... "
                if os.path.exists("finished_{}".format(name)):
                    # handler = open("finished_{}".format(name), "r")
                    # content = handler.read()
                    # handler.close()
                    # timestamp = datetime.datetime.utcfromtimestamp(int(content.strip(".")[0])*1000)
                    return_str += "{} was finisihed... "
                return return_str, 200, None
            else:
                return "{} is not a valid scrapper".format(name), 400, None
        else:
            return "Name has not been provided", 400, None
    else:
        return "Error 501. Method not implemented", 501, None


def stop_scrapper(request):
    if request.method == "GET":
        name = ""
        if "name" in request.parsed_uri["params"]:
            name = request.parsed_uri["params"]["name"].lower()
        if name != "":
            if name in SCRAPPERS:
                handler = open("stop_{}".format(name), "w")
                handler.close()
                return "Stopping request performed with success! It might take a while until the real stop. Please check the status", 200, None
            else:
                return "{} is not a valid scrapper".format(name), 400, None
        else:
            return "Name has not been provided", 400, None
    else:
        return "Error 501. Method not implemented", 501, None


def deactivate_scrapper(request):
    if request.method == "GET":
        name = ""
        if "name" in request.parsed_uri["params"]:
            name = request.parsed_uri["params"]["name"].lower()
        if name != "":
            if name in SCRAPPERS:
                if name not in running_scrappers:
                    return "The scrapper is currently not running", 400, None
                os.kill(running_scrappers[name], signal.SIGTERM)
                del running_scrappers[name]
                return "Kill request performed with success!", 200, None
            else:
                return "{} is not a valid scrapper".format(name), 400, None
        else:
            return "Name has not been provided", 400, None
    else:
        return "Error 501. Method not implemented", 501, None


class HTTPServer(TCPServer):
    headers = {
        'Server': 'TWServer',
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
    }

    dict_principal_routes = {}

    dict_entire_routes = {
        "/search_product": search_product,  # /search_product?content_search=
        '/search_product_api': search_product_api,  # /search_product_api?content_search=
        "/news/emag": get_news_emag,  # /news/emag
        "/news/evomag": get_news_evomag,  # /news/evomag
        "/get_products/emag": get_product_from_category_emag,  # /get_products/category/emag?category_name=
        "/get_products/evomag": get_product_from_category_evomag,  # /get_products/category/evomag?category_name=
        "/get_products/subcategory/evomag": get_product_from_subcategory_evomag,  # /get_products/subcategory/evomag?subcategory_name=
        "/get_products/subcategory/emag": get_product_from_subcategory_emag,  # /get_products/subcategory/emag?subcategory_name=
        "/get_similar": get_similar_from_all, # /get_similar?product_link=
        "/scrapper/activate": activate_scrapper,  # /scrapper/activate?name=
        "/scrapper/run": run_scrapper,  # /scrapper/run?name=
        "/scrapper/status": status_scrapper,  # /scrapper/status?name=
        "/scrapper/stop": stop_scrapper,  # /scrapper/stop?name=
        "/scrapper/deactivate": deactivate_scrapper,
        "/send/message": post_message, # put a message to sent
        "/get_price_fluctuation": get_price_fluctuation,  # /get_price_fluctuation?product_link=
        "/get_offers": get_offers  # /get_offers?product_link=
    }

    dict_mime_types = None
    dict_status_codes = None

    def __init__(self):
        TCPServer.__init__(self)
        handler_mime_types = open("Helpers/mime_types_dict", "r")
        self.dict_mime_types = json.load(handler_mime_types)
        handler_mime_types.close()
        handler_status_code = open("Helpers/status_codes_dict", "r")
        self.dict_status_codes = json.load(handler_status_code)
        handler_status_code.close()

    def handle_request(self, data):
        print(data)
        request = HttpRequest(data)
        response = None
        handler = None
        print(request.parsed_uri)

        entire_uri = request.parsed_uri["entire_route"]
        if entire_uri in self.dict_entire_routes:
            handler = self.dict_entire_routes[entire_uri]
        else:
            for partial_url in self.dict_principal_routes:
                if partial_url in entire_uri:
                    handler = self.dict_principal_routes[partial_url]
                    break
            if not handler:
                if request.method == "GET":
                    handler = self.handle_GET
                else:
                    response = self.HTTP_501_handler(request)
        if request.method is None:
            response = self.HTTP_501_handler(request)
        elif response is None and handler is not None:
            text, status, extra_headers = handler(request)
            response_line = self.response_line(status)
            response_headers = self.response_headers(extra_headers)
            response_body = text

            blank_line = "\r\n"

            return "%s%s%s%s" % (
                response_line,
                response_headers,
                blank_line,
                response_body
            )

        else:
            response = self.HTTP_501_handler(request)
        return response

        """
        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            response = self.HTTP_501_handler(request)
        if request.method is None:
            response = self.HTTP_501_handler(request)
        elif response is None and handler is not None:
            response = handler(request)
        else:
            response = self.HTTP_501_handler(request)
        return response
        """

    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
        blank_line = "\r\n"
        response_body = "<h1>501 Not Implemented</h1"
        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )

    def handle_OPTIONS(self, request):
        response_line = self.response_line(200)
        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)

        blank_line = "\r\n"

        return "%s%s%s" % (
            response_line,
            response_headers,
            blank_line
        )

    def handle_GET(self, request):
        filename = request.uri.strip('/')
        filename = "Views/" + filename
        extra_headers = None
        status_code = None
        if os.path.exists(filename) and os.path.isfile(filename):
            status_code = 200
            response_line = self.response_line(200)
            if "." in filename:
                extension = "." + filename.rsplit(".")[1]
                content_type = str(self.dict_mime_types[extension][1])
            else:
                content_type = "text/html"
            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)

            with open(filename, "rb") as f:
                response_body = f.read()
        else:
            status_code = 404
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = "<h1> 404 Not Found </h1>"

        blank_line = "\r\n"
        return response_body, status_code, extra_headers
        """
        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )"""

    def handle_POST(self, request):
        uri = request.uri.strip('/')
        response_line = self.response_line(200)
        response_headers = self.response_headers()
        blank_line = "\r\n"
        return "%s%s%s" % (
            response_line,
            response_headers,
            blank_line
        )

    def response_line(self, status_code):
        """
        :param status_code:
        :return: response_line
        """
        reason = str(self.dict_status_codes[str(status_code)][0])
        return "HTTP/1.1 %s %s \r\n" % (status_code, reason)

    def response_headers(self, extra_headers=None):
        """
        :param extra_headers: dict for sending extra headers for the current response
        :return: headers
        """
        headers_copy = self.headers.copy()
        if extra_headers:
            headers_copy.update(extra_headers)
        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])
        return headers


class HttpRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.parsed_uri = {"entire_route": "", "principal_route": "", "target": "",
                      "params": ""}
        self.http_version = '1.1'
        self.headers = {}
        self.body = None
        self.mime_type = None
        self.parse(data)

    def parse(self, data):
        print(data)
        lines = data.split('\r\n')
        request_line = lines[0]  # first line
        lines2 = data.split('\r\n\r\n', 1)  # body request
        request_body = ""
        if len(lines2) == 2:
            request_body = lines2[1]
        if len(request_line):
            self.parse_request_line(request_line)
            self.parse_request_uri()
            self.parse_request_headers(lines[1:])  # headers
            if len(request_body):
                self.parse_request_body(request_body)

    def parse_request_uri(self):  # /products/id/test?a=what&b=ce&c="mere%20are%20ana"#test
        params_uri = ""
        if "?" in self.uri:
            new_uri = self.uri.split('?')[0]
            params_uri = self.uri.split('?')[1]
        else:
            new_uri = self.uri
        list_component = new_uri.split('/')
        principal_route = "/".join(list_component[:-1])
        current_component = list_component[-1]
        dict_params = {}
        print current_component
        if "?" in self.uri:
            target = current_component.split("?")[0]
            # params = current_component.split("?")[1]
            # params_final = params.split("&")
            params_final = params_uri.split('&')
            for param in params_final:
                arg = param.split("=")
                dict_params[arg[0]] = arg[1]
        else:
            target = current_component
        entire_route = principal_route + "/" + target
        route_dict = {"entire_route": entire_route, "principal_route": principal_route, "target": target,
                      "params": dict_params}
        self.parsed_uri = route_dict

    def parse_request_line(self, request_line):
        words = request_line.split(' ')
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.http_version = words[2]

    def parse_request_body(self, request_body):
        self.body = request_body

    def parse_request_headers(self, request_headers):
        for element in request_headers:
            if 'Content-Type:' in element:
                mt = element.split(": ")
                self.mime_type = mt[1].strip()


def kill_child():
    for child_pid in running_scrappers:
        os.kill(running_scrappers[child_pid], signal.SIGTERM)


def start_scrappers():
    for item in SCRAPPERS:
        print("Starting... {}".format(item))
        child = subprocess.Popen(["python","{}".format(SCRAPPERS[item])])
        running_scrappers[item] = child.pid
    atexit.register(kill_child)


if __name__ == '__main__':
    start_scrappers()
    server = TCPServer()
    server.start()
