from functools import reduce

def l_print(a_list):
    for i in a_list:
        print(i)

def list_to_string_intervalls(a_list):
    temp=[]
    for i in a_list:
        temp.append(reduce(lambda i1, i2: str(i1) + str(i2), i))
    return ", ".join(temp)

def string_not_covered(covers):
    output = ""
    for i in covers:
        output += "    " + str(i[0]) + "\n        " + str(i[1])
    return output
