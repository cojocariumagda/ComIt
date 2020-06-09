import pymongo

dict_mapping_categorii_principale_emag = {
    9: "p_0",
    1: "p_1",
    5: "p_2",
    4: "p_3",
    3: "p_4",
    6: "p_5",
    7: "p_6",
    11: "p_7",
    2: "p_8",
    8: "p_9",
    10: "p_10"
}

dict_mapping_categorii_principale_evomag = {
    1: "evo_p0",
    2: "evo_p1",
    3: "evo_p2",
    4: "evo_p3",
    5: "evo_p4",
    6: "evo_p5",
    7: "evo_p6",
    8: "evo_p7",
    9: "evo_p8",
    10: "evo_p9",
    11: "evo_p10",
    12: "evo_p11",
    13: "evo_p12",
    14: "evo_p13",
    15: "evo_p14",
    16: "evo_p15",
    17: "evo_p16"
}


def get_dict_categorii_nume(site):
    if site == "emag":
        db_comit_principal = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["principal_categories"]
    else:
        db_comit_principal = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["principal_categories_evomag"]
    result = []
    for principal_category in db_comit_principal.find():
        result.append(principal_category)
    return result


def get_dict_categorii_secundare_by_id_princ(site, id_princ):
    if site == "emag":
        db_comit_second = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["second_categories"]
        result = []
        for second_category in db_comit_second.find({"_id_principal_category": id_princ}):
            result.append(second_category)
    else:
        db_comit_second = pymongo.MongoClient("mongodb://localhost:27017/")["ComIt"]["second_categories_evomag"]
        result = []
        for second_category in db_comit_second.find({"_id_principal_category": id_princ}):
            result.append(second_category)
    return result


if __name__ == '__main__':
    handler = open('helper_front_evomag.txt', 'w')
    site = "evomag"
    site_count = 18
    categorii_principale = get_dict_categorii_nume(site)
    cod_final_emag = ""

    for i in range(1, site_count):
        categorie_principala_curenta = {}
        for j in range(len(categorii_principale)):
            if site == "emag":
                if categorii_principale[j]["_id"] == dict_mapping_categorii_principale_emag[i]:
                    categorie_principala_curenta = categorii_principale[j]
            else:
                if categorii_principale[j]["_id"] == dict_mapping_categorii_principale_evomag[i]:
                    categorie_principala_curenta = categorii_principale[j]
        nume_categorie_principala = categorie_principala_curenta['nume_categorie']
        index_categorie = i
        print nume_categorie_principala, index_categorie
        if site == "emag":
            categorii_secundare_index_curent = get_dict_categorii_secundare_by_id_princ(site,
                                                                                        dict_mapping_categorii_principale_emag[
                                                                                            index_categorie])
        else:
            categorii_secundare_index_curent = get_dict_categorii_secundare_by_id_princ(site,
                                                                                        dict_mapping_categorii_principale_evomag[
                                                                                            index_categorie])
        print categorii_secundare_index_curent
        if site == "emag":
            code_current = """<div class ="dropdownSecond">
                            <a class = "dropbtnSecond" href="#categoria{}_emag">{}</a>
                            <div class = "dropdown-content-second">\n""".format(index_categorie, nume_categorie_principala)
        else:
            code_current = """<div class ="dropdownSecond">
                                        <a onclick="getEvomagCategory('{}')" class = "dropbtnSecond" href="#produse"> {} </a>
                                        <div class = "dropdown-content-second">\n""".format(nume_categorie_principala.replace('&', '%26'), nume_categorie_principala)
        subcode_current = ""
        count = 1
        for categorie_secundara in categorii_secundare_index_curent:
            if site == "emag":
                subcode_current += '                              <a href = "#subcategoria{}_{}_emag">{}</a>\n'.format(
                    count, index_categorie, categorie_secundara['nume_subcategorie'])
            else:
                subcode_current += """                              <a onclick="getEvomagSubcategory('{}')" href = "#produse">{}</a>\n""".format(categorie_secundara['nume_subcategorie'].replace('&', '%26'), categorie_secundara['nume_subcategorie'])
            count += 1
        code_current += subcode_current
        code_current += "</div> </div>\n"

        handler.write(code_current)
    handler.close()

