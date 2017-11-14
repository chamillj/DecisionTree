#@@---------------------------@@
#  Author: Chamil Jayasundara
#  Date: 8/15/16
#  Description: Parsing the data file
#@@---------------------------@@

from collections import OrderedDict

class DataSet:
    def __init__(self):
        self.attributes = OrderedDict()
        self.data = {}

    def get_attribute_values(self, key):
        return self.attributes[key]


def parsefile(data_file):

    attributes = []
    data = []  # lists are memory efficient than dictionaries

    with open(data_file, 'r') as file:
        for i, line in enumerate(file):
            if i==1:
                attributes = line.split()
            elif i >= 3:
               data.append(line.split())

    return attributes,data


def crete_data_set(path_to_data_file):
    list_af_attributes, data = parsefile(path_to_data_file)

    my_data = DataSet()
    my_data.data = data

    for i, item in enumerate(list_af_attributes):
        temp_dic = {'column': i,
                    'values': list(set([row[i] for row in data]))}
        my_data.attributes[item] = temp_dic

    return my_data

