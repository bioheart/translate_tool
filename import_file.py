import pandas as pd
import polib
import csv

def get_data_from_po(path_template):
    data = dict()
    po_path = path_template
    po = polib.pofile(po_path)
    for entry in po:
        msgid = str(entry.msgid)
        msgstr = str(entry.msgstr)
        data[msgid]=[msgstr]
    return data

def get_data_from_csv(file_name):
    df = (pd.read_csv(file_name)).to_dict()
    data = dict()
    keys = list(df.keys())
    for i in range(len(df[keys[0]])):
        data[df[keys[0]][i]]=df[keys[1]][i]
    return data

def compare_with_po(main_data, comp_data , show_value = False):
    results = main_data.copy()
    if(show_value):
        print("=== Update List === ")
    for key in main_data:
        if(key in comp_data.keys()):
            if(main_data[key] == comp_data[key][0]):
                if not (show_value):
                    if(key in results):
                        # print('DROP : ',key ,main_data[key],':',comp_data[key][0])
                        del results[key]
            else:
                if(show_value):
                        print("gettext('%s');"%key)

    if(show_value):
        print("================== ")
    return results

def print_gettext(csv_data, compare_text=False):
    words=[]
    for key in csv_data:
        if(compare_text):
            if not(("gettext('%s');"%key) in compare_text):
                words.append([("gettext('%s');"%key),key,csv_data[key]])
            else:
                print('remove ' , ("gettext('%s');"%key))
                pass
        # print('gettext("%s");'%csv_data[key])
        else:
            words.append([("gettext('%s');"%key),key,csv_data[key]])
    return words


# compare_text is a custom-i18n [gettext('text');] that you want to check or not
# the default of this value is False (not check)
def wirte_to_file(csv_data, file_name ,compare_text = False,file_type=''):
    if(file_type=='' or file_type=='csv'):
        data = print_gettext(csv_data,compare_text)
        writer = csv.writer(open(file_name, "w"), delimiter=",")
        writer.writerows(data)
    else:
        with open(file_name, 'w+') as file:
            file.writelines("% s\n" % data for data in print_gettext(csv_data,compare_text))

def get_words_i18n(file_name):
    words = []
    with open(file_name) as f:
        lines = f.read().splitlines()
        words.append(lines)
    # print(words)
    return words
#code here.
csv_data = get_data_from_csv('translate.csv')

core_data = get_data_from_po('CORE_it.po')
wedget_data = get_data_from_po('WEDGET_it.po')

operator_data = get_data_from_po('OPERATOR_it.po')

#compare with .po file
csv_data = compare_with_po(csv_data,core_data)
csv_data = compare_with_po(csv_data,wedget_data)
csv_data = compare_with_po(csv_data,operator_data)

#compare with .po file to see update list
csv_data = compare_with_po(csv_data,operator_data,show_value=True)

#get text data with custom-i18n.txt
custom_gettext = get_words_i18n('custom-i18n.txt')

#write to file
wirte_to_file(csv_data,'forNew.csv',custom_gettext)
# wirte_to_file(csv_data,'forNew.js',custom_gettext)



