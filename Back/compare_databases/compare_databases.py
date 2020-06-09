import time
import json
import pymongo


MONGODB_URI = "mongodb://heroku_xzc0r78w:iipvtiu45d221kjg9fjjtqi7r9@ds243812.mlab.com:43812/heroku_xzc0r78w?retryWrites=false"


def get_promotion_list_items():
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


if __name__ == '__main__':
    print len(get_promotion_list_items())