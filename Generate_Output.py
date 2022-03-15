from dis import dis
from functools import reduce
from operator import not_
import string
from newprint import l_print
from copy import deepcopy
import re 

def update_bool(bool_val):
    temp=1
    for i in range(len(bool_val)-1,-1,-1):
        bool_val[i]+=temp
        if bool_val[i]>=2:
            temp=1
            bool_val[i]=0
        else:
            temp=0
    return bool_val

def logicals_function(parameter, function):
    bool_val=[0]*len(parameter)
    i=0
    on_set = []
    off_set = []
    bool_tabel = ""
    f = eval("lambda " + ", ".join(parameter) + ": " + function)
    bool_tabel += "|".join(parameter)+"|f(x)\n"
    while i < 2**len(parameter):
        k = 0
        for j in bool_val:
            if k % 4 != 0:
                bool_tabel += " "
            k += 1
            bool_tabel+=" %i|"%j
        b = f(*bool_val)
        if b:
            on_set.append(bool_val[:])
        else:
            off_set.append(bool_val[:])
        bool_tabel += "%3i \n"%b
        bool_val = update_bool(bool_val)
        i+=1
    return bool_tabel, on_set, off_set

def numbers_of_ones(var_bool):
    return reduce(lambda x1, x2: x1+x2, var_bool)

def sort_by_number_of_ones(on_set):
    if not on_set:
        return False
    sorted_list=[[]]*(len(on_set[0])+1)
    for i in on_set:
        sorted_list[numbers_of_ones(i)] = sorted_list[numbers_of_ones(i)] + [[i,0]]
    return [x for x in sorted_list if x != []]

def distance_intervalls(i1,i2):
    distance = 0
    first_difference_position=None
    for i in range(len(i1)):
        if i1[i] != i2[i]:
            if first_difference_position == None:
                first_difference_position = i
            distance += 1
    if first_difference_position!=None:
        i1[first_difference_position]="-"
    return distance,i1

def generate_maximal_intervalls(sorted_list):
    steps = [sorted_list]
    prim_elemets = []
    stop_loop = 1
    while len(steps[-1])>1 and stop_loop != 0:
        next_step = []
        for i in range(len(steps[-1])-1): # doesnt cover the last prim_elelemts, thats why the for looper later
            intervalls = []
            stop_loop = 0
            for j in range(len(steps[-1][i])):
                for k in range(len(steps[-1][i+1])):
                    distance, intervall = distance_intervalls(steps[-1][i][j][0][:],steps[-1][i+1][k][0][:])
                    if distance == 1:
                        if steps[-1][i][j][1] == 0:
                            steps[-1][i][j][1] = 1
                        if steps[-1][i+1][k][1] == 0:
                            steps[-1][i+1][k][1] = 1
                            intervalls.append([intervall,0])
                if steps[-1][i][j][1] == 0:
                    prim_elemets.append(steps[-1][i][j][0])
            if intervalls != []:
                stop_loop += 1
                next_step.append(intervalls)
        for i in steps[-1][-1]:
            if i[1] == 0:
                prim_elemets.append(i[0])
        if next_step != []:
            steps.append(next_step)
    if len(steps[-1]) == 1 and steps[-1] != [[]]:
        prim_elemets.append(steps[-1][0][0][0])
    return prim_elemets,steps

def mc_culskey_output(steps,prime):
    step_1 = []
    for i in steps:
        step_1.append(reduce(lambda x1, x2: x1 + x2, i))
    len_lists = []
    for i in range(len(step_1)):   
        len_lists.append(len(step_1[i])-1)
    output=[]
    for i in range(len(step_1[0])):
        steps_2 = []
        for j in range(len(len_lists)):
            if i<=len_lists[j]:
                steps_2.append(reduce(lambda i1,i2: str(i1) + str(i2), step_1[j][i][0]) + " " + str(step_1[j][i][1]))
        if steps_2 != []:
            output.append(" | ".join(steps_2))
    output_prime = []
    for i in prime:
        output_prime.append(reduce(lambda i1,i2: str(i1) + str(i2), i))
    return ", ".join(output_prime), "\n".join(output)

def is_literal_in_intervall(literal, intervall):
    for i in range(len(literal)):
        if literal[i] != intervall[i] and intervall[i] != "-":
            return False
    return True

def find_covered_iterals(needed_elements,elements_to_inspect):
    not_covered = []
    for elements in elements_to_inspect:
        skip_to_next = False
        for overlapping_element in elements[1]:
            for i in needed_elements:
                if overlapping_element == i:
                    skip_to_next = True
                    break
            if skip_to_next:
                break
        if not skip_to_next:
            not_covered.append(elements)
    return not_covered

def optimized_function(prim_elements,on_set):
    overlap_iterals = []
    needed_elements = []
    elements_to_inspect = []
    for i in on_set:
        overlap_iteral = []
        for j in prim_elements:
            if is_literal_in_intervall(i,j):
                overlap_iteral.append(j)
        overlap_iterals.append([i,overlap_iteral])
        if len(overlap_iteral) == 1:
            needed_elements.append(overlap_iteral[0])
        elif len(overlap_iteral) > 1:
            elements_to_inspect.append([i,overlap_iteral])
    return needed_elements, find_covered_iterals(needed_elements,elements_to_inspect)

def minimize(on_set):
    sorted_list = sort_by_number_of_ones(on_set)
    prim_elemets, steps = generate_maximal_intervalls(sorted_list)
    output_prime, output_steps = mc_culskey_output(deepcopy(steps), deepcopy(prim_elemets))
    cover = optimized_function(deepcopy(prim_elemets), deepcopy(on_set))
    return output_prime, output_steps, cover

def gen_VDNF(on_set):
    if on_set == []:
        return "0"
    output = ""
    for i in on_set:
        for j in range(len(i)):
            if i[j] == 0:
                output += "-x" + str(j+1)
            else:
                output += "x" + str(j+1)
        if i != on_set[-1]:
            output += " v "
    return output

def gen_KDNF(off_set):
    if off_set == []:
        return "0"
    output = "("
    for i in off_set:
        for j in range(len(i)):
            if i[j] == 0:
                output += "-x" + str(j+1)
            else:
                output += "x" + str(j+1)
            if j == len(i):
                output += "v"
        if i != off_set[-1]:
            output += ") A ("
    return output + ")"

if __name__ == "__main__":
    from Lambda_Function import string_to_lambda_components
    x,y,z= logicals_function(*string_to_lambda_components("x1 A x2 V x3 A x4 A x5"))
    print(minimize(deepcopy(y))[2])