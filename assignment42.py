# Katherine Zhang

# This program analyzes food webs from files, stores them into a dictionary, and identifies relationships between organisms

import sys
from formatList import formatList

inf = open(sys.argv[1], "r")

############################## Part 1 ################################
def predprey(file_name):
    line = file_name.readline()
    # Initialize an empty list
    dict_predprey = {}
    while line != "":
        line = line.rstrip()
        list_preypred = line.split(",")
        line = inf.readline()
        # Identify the predator prey
        pred = list_preypred[0]
        prey = list_preypred[1:]
        # Populate a diction with predators as keys and prey as values
        dict_predprey[pred] = prey
    return dict_predprey


############################## Part 2 ################################
def apex(relationships):
    # Initialize lists
    list_pred = []
    list_prey = []
    list_apex = []
    # Add predator and prey to lists
    list_pred.append(relationships.keys())
    list_prey.append(relationships.values())
    for i in list_pred:
        if i not in list_prey:
            list_apex.append(i)
    #print(list_pred)
    #print(list_prey)
    #print(list_apex)
    return list_apex

############################## Part 3 ################################
def producer(relationships):
    # Initialize lists
    list_pred = []
    list_prey = []
    list_producer = []
    # Add predator and prey to lists
    list_pred.append(relationships.keys())
    list_prey.append(relationships.values())
    for i in list_prey:
        if i not in list_pred:
            list_producer.append(i)
    if i in list_producer:
        list_producer.remove(i)
    #print(list_pred)
    #print(list_prey)
    #print(list_apex)
    return list_producer
############################## Part 4 ################################
# This function determine which predator eats the most prey by counting the number of values in the list
# The predator is then added to a list of flexible predators.
    # Parameters: dictionary of predators and prey
    # Returns: list of flexible predators
def flexible_eater(relationships):
    num_prey = 0
    list_flexpred = []
    for i in relationships.keys():
        prey = relationships[i]
        previous_numprey = num_prey
        if len(prey) > num_prey:
            num_prey = len(prey)
            list_flexpred.append(i)
            if num_prey >= previous_numprey:
                list_flexpred.pop(0)
            #list_flexpred.pop(0)
        elif len(prey) == num_prey:
            list_flexpred.append(i)
    return(list_flexpred)

    # Create list of prey:
    #list_prey1 = []
    #for element in list_prey:
    #    if len(element) > 1:
    #        for animal in element:
    #            list_prey1.append(animal)
    #    elif len(element) == 1:
    #        list_prey1.append(element)


############################## Part 5 ################################
def tastiest(relationships):
    # Initialize an empty Dictionary
    counts = {}
    # Initialize an empty list for tastiest prey
    list_tasty = []
    list_prey =[]
    for i in relationships.keys():
        list_prey.append(relationships[i])
    print(list_prey)



    # Determine how many times each prey appears in the dictionary
#    for i in relationships:
        # If the value has not been encountered previously
#        if i not in counts.keys():
            # add the item into the dictionary with a count of 1
#            counts[i] = 1
        # If the value has been encountered before
#        else:
            # Add 1 to the count associated with the item
#            counts[i] = counts[i] + 1
    # Determine the value with the largest count
#    if len(counts) > 0:
#        tastiest_prey = max(counts.values())
#        for prey in counts.keys():
            # If the key has the most values
#            if counts[prey] == tastiest_prey:
                # Add the prey to the tastiest prey list
#                list_tasty.append(prey)
#    return list_tasty
############################## Part 6 ################################
#set the heights of all organisms, including the producers, to 0
#set changed to true
#while something has changed
    #set changed to false
    #for each animal, A, in the food web
        #for each animal, p, that A preys on
            #if the height of A is less than or equal to the height of p set the height of a to the height of p + 1
            #set changed to true

# Create a list of all organisms in the food web
def height(relationships):
    for pred in relationships.keys():
        height_a = 0
    for prey in relationships.values():
        height_p = 0
    changed = True
    while changed == False:
        changed = False
        for a in relationships.keys():
            for p in relationships[a]:
                if height_a <= height_p:
                    height_a = height_p + 1
                    changed = True
    #return ????

def main():
    # PART 1
    dictionary = predprey(inf)
    for i in dictionary.keys():
        print(i, "eats", formatList(dictionary[i]))
    # PART 2
    apex_pred = apex(dictionary)
    print("Apex Predators: ", formatList(apex_pred))
    # PART 3
    flex_eater = flexible_eater(dictionary)
    print("Most Flexible Eaters: ", formatList(flex_eater))
    # PART 4
    producers_list = producer(dictionary)
    print("Producers: ", formatList(producers_list))
    # PART 5
    tastiest_list = tastiest(dictionary)
    print("Tastiest Organisms: ", formatList(tastiest_list))
    # PART 6



main()
