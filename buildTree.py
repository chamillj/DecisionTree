#@@---------------------------@@
#  Author: Chamil Jayasundara
#  Date: 8/17/16
#  Description: Building a decision tree ground up
#@@---------------------------@@

from collections import defaultdict
from dataParser import *
from math import log


class DecisionNode:
    """Class for Decision Nodes"""
    def __init__(self, name):
        self.attribute_name = name
        self.children={}

    #This is to enable dictionary like behaviour
    def __getitem__(self, key):
        return self.children[key]


class Tree:
    """Class for the entire tree"""
    def __init__(self, root):
        self.root = root # Should be a decision node object

    def tree_traverse(self, set_of_attributes):
        #  set_of_attributes = {attribute:value}

        def traverse(node):

            next_node = node[set_of_attributes[node.attribute_name]]  # this dictionary like behaviour is enabled, see class def

            if type(next_node) is DecisionNode:
                return traverse(next_node)
            else:
                return next_node

        prediction = traverse(self.root)
        return prediction
    # do something here



def entropy(frequncies):
    # frequencies = [5, 6, 8, ...]

    entr = 0

    total = sum(frequncies)

    for f in frequncies:

        if f !=0:
            prob = f / total
            entr -= (prob * log(prob, 2))

        else:
            print("Check there is a zero")

    return entr


def get_information_gain(entropy_of_superset, size_of_superset, splitted_data):

    # set_of_subsets = [a:[1,2,4],b:[4,5,7]
    inf_gain = entropy_of_superset  # Good to pass this one here as otherwise this will be recalculated a lot due to recursion

    for key in splitted_data:
        frequencies = calculate_frequencies(splitted_data[key], 0).values()
        inf_gain -= (sum(frequencies)/size_of_superset) * entropy(frequencies)

    return inf_gain


def calculate_frequencies(array, column):
    # calculate fequencies of different values of each attributes
    frequencies = defaultdict(int)

    # for item in [element[0] for element in array]:
    for element in array:
        frequencies[element[column]] += 1

    return frequencies


def split_dataset(dataset, column):

    splitted_data = defaultdict(list)

    for element in dataset:
        splitted_data[element[column]].append(element)

    return splitted_data


def build_tree(data_obj, entropy_of_data):
    #This recuresively build the tree and return the root node

    next_node, split_data = pick_next_node(data_obj)
    # index_of_attribute = list_of_attributes.index(next_node)
    decision_node = DecisionNode(next_node)

    for attribute_value in data_obj.attributes[next_node]['values']:
        data_subset = split_data[attribute_value]

        if data_subset:
            entropy_of_subset = entropy(calculate_frequencies(data_subset, 0).values())

            if entropy_of_subset == 0:
                decision_node.children[attribute_value] = data_subset[0][0]  # since there will be only one type

            else:
                new_data_obj = DataSet()
                new_data_obj.data = split_data[attribute_value]
                new_data_obj.attributes = dict(data_obj.attributes)
                del new_data_obj.attributes[next_node]
                decision_node.children[attribute_value] = build_tree(new_data_obj, entropy_of_subset)

        else:
            frequencies = calculate_frequencies(data_obj.data, 0)
            decision_node.children[attribute_value] = max(frequencies, key=frequencies.get)
            # something somethon


    return decision_node


def pick_next_node(data_obj):
    entropy_of_data = entropy(calculate_frequencies(data_obj.data, 0).values())
    next_node = ""
    splitted_dataset={}
    max_information_gain = -1  # information gain always +ve

    for attribute in data_obj.attributes:
        split_on_i = split_dataset(data_obj.data, data_obj.attributes[attribute]['column'])
        information_gain = get_information_gain(entropy_of_data, len(data_obj.data), split_on_i)
        if information_gain > max_information_gain:
            next_node = attribute
            splitted_dataset = split_on_i

    return next_node, splitted_dataset


def main():

    ##Training
    train_data = crete_data_set('data/noisy10_train.ssv')

    ##This is the orginal entropy of dataset before we split
    entropy_of_data = entropy(calculate_frequencies(train_data.data, 0).values())

    my_tree = Tree(build_tree(train_data, entropy_of_data))


    ##Validation
    validation_data = crete_data_set('data/noisy10_valid.ssv')
    keys = list(validation_data.attributes.keys())
    for d in validation_data.data:
        test = {keys[i]: d[i] for i in range(1, len(keys))}
        predict = my_tree.tree_traverse(test)

        # print("prediction= " + predict + " actual: " + str(d[0]))
        if predict is not d[0]:
            print("error")

        else:
            print("not an error")


if __name__ == "__main__":
    main()
