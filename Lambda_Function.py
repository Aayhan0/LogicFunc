import re 

# Checks if it is a bool Function (semantics)
brackets = 0
def bracket_check(z):
    global brackets
    brackets += z
    if brackets < 0:
        return True
    return False
def automaton(input_string):
    length = len(input_string)
    state = 0
    while input_string:
        while input_string[0] == " ":
            input_string = input_string[1:]
        if state == 0:
            if input_string[0] == "(":
                if bracket_check(+1):
                    return "Bracket Error %i" % brackets
                input_string = input_string[1:]
            elif input_string[0] == "-":
                input_string = input_string[1:]
            elif input_string[0] == "x":
                state = 1
                input_string = input_string[1:]
            else:
                return "unallowed Symbol %c at %i" % (input_string[0],length - len(input_string)+1)
        elif state == 1:
            if input_string[0].isdigit():
                input_string = input_string[1:]
            elif input_string[0] == "V" or input_string[0] == "A" or input_string[0] == "O":
                state = 0
                input_string = input_string[1:]
            elif input_string[0] == ")":
                if bracket_check(-1):
                    return "Bracket Error %i" % brackets
                state = 2
                input_string = input_string[1:]
            else:
                return "unallowed Symbol %c at %i" % (input_string[0],length-len(input_string)+1)
        elif state == 2:
            if input_string[0] == ")":
                if bracket_check(-1):
                    return "Bracket Error %i" % brackets
                input_string = input_string[1:]
            elif input_string[0] == "V" or input_string[0] == "A" or input_string[0] == "O":
                state = 0
                input_string = input_string[1:]
            else:
                return "unallowed Symbol %c at %i" % (input_string[0],length-len(input_string)+1)
        else:
            return False
    if brackets == 0:
        return True
    return "Bracket Error %i" % brackets
# get the used Variables (x0-x99)
def sorting_key_variables(inputChar):
    return int(inputChar[1:])
def get_variables(input_string):
    var=[]
    temp=re.findall('x[0123456789]{1,2}', input_string)
    for i in temp:
        if not(i in var):
            var.append(i)
    var.sort(key=sorting_key_variables)
    return var

# returns valubels and function part of lambda
# if it is not a logical function it will return false,false
def string_to_lambda_components(input_string):
    result=automaton(input_string)
    if result==True:
        edited_input_string = "".join(input_string.split(" "))
        function_string=" not ".join(" ^ ".join(" and ".join(" or ".join(edited_input_string.split("V")).split("A")).split("O")).split("-"))
        lFuncX=re.findall("not x[0123456789]{1,2}",function_string)
        lFuncS=re.split("not x[0123456789]{1,2}",function_string)
        if lFuncS:
            function_string=""
            for i in range(len(lFuncX)):
                function_string=function_string+lFuncS[i]+"(not " + lFuncX[i][4:] + ")"
            function_string=function_string+lFuncS[len(lFuncS)-1]
        return get_variables(edited_input_string), function_string
    return False,result