"""
Houses functions that work to create the latex formatting 
"""

from collections import namedtuple


def CreateVariableValues(*variable_value_pairs):
    """
    Takes in any number of tuples each of length 2, then
    formats and returns a list of named tuples
    """

    VariableValueTup = namedtuple('VariableValueTup', ["Variable", "Value"])

    return tuple(map(lambda tup: VariableValueTup(*tup), *variable_value_pairs))

def CreateValueUncertainties(*value_error_pairs):

    ValueUncertaintiesTup = namedtuple('ValueUncertaintiesTup', ["Value", "Error"])

    return tuple(map(lambda tup: ValueUncertaintiesTup(*tup), *value_error_pairs))


def LatexCreator(current_str: str, variable_dict : dict):

    """
    Recursive function that takes in a string with variables
    and replaces the variables with their corresponding values
    by indexing into the dictionary

    Returns a list of latex strings

    Used internally in the program
    """

    start_ind = current_str.find("@")

    if start_ind == -1:
        return ['$' + current_str + '$'] # Need to put something here
    
    else:

        end_ind = current_str.find('#')

        dict_value = variable_dict[current_str[start_ind:end_ind+1]]

        result_str = current_str.replace(current_str[start_ind:end_ind+1], dict_value[1])

        while result_str.find('@') != -1:

            next_start = result_str.find('@')

            next_end = result_str.find('#')

            next_var = result_str[next_start:next_end + 1]

            result_str = result_str.replace(next_var, variable_dict[next_var][1])

        variable_str = current_str.replace(current_str[start_ind:end_ind+1], dict_value[0])

        return ['$' + result_str + '$'] + LatexCreator(variable_str, variable_dict)
    

def ErrorBeginning2Items(operation, item1, item2):

    format_func = lambda a, b: f"{{{a}}} {operation} {{{b}}}"

    pm_func = lambda n: f"{n.Value}\\pm{n.Error}"

    if item1.Error == 0 and item2.Error == 0:
        return format_func(item1.Value, item2.Value)
    
    elif item1.Error == 0:
        return format_func(item1.Value, pm_func(item2)) 
    
    elif item2.Error == 0:
        return format_func(pm_func(item1), item2.Value)  
    
    else:
        return format_func(pm_func(item1), pm_func(item2))
    
def ErrorBeginning1Item(format_func, item):

    if item.Error == 0:
        return format_func(item.Value)
    
    else:
        return format_func(f"{item.Value}\\pm{item.Error}")

    
def CreateValueLatexSting(operation, *variable_value_pairs):
    
    item1, *item2 = CreateVariableValues(variable_value_pairs)

    if item2 != []:
        item2 = item2[0]

    match operation:

        case '+':
            
            variable_string = f"{item1.Variable} + {item2.Variable}"

            numeric_string = f"{item1.Value} + {item2.Value}"

        case '-':
            variable_string = f"{item1.Variable} - {item2.Variable}"

            numeric_string = f"{item1.Value} - {item2.Value}"

        case '*':
            variable_string = f"{item1.Variable} * {item2.Variable}"

            numeric_string = f"{item1.Value} * {item2.Value}"

        case '/':
            variable_string = f"\\frac{{{item1.Variable}}}{{{item2.Variable}}}"

            numeric_string = f"\\frac{{{item1.Value}}}{{{item2.Value}}}"

        case '**':
            variable_string = f"{item1.Variable}^{{{item2.Variable}}}"

            numeric_string = f"{item1.Value}^{{{item2.Value}}}"
        
        case 'sin':
            variable_string = f"\\sin({item1.Variable})"

            numeric_string = f"\\sin({item1.Value})"

        case 'cos':
            variable_string = f"\\cos({item1.Variable})"

            numeric_string = f"\\cos({item1.Value})"

        case 'tan':
            variable_string = f"\\tan({item1.Variable})"

            numeric_string = f"\\tan({item1.Value})"

        case 'arcsin':
            variable_string = f"\\arcsin({item1.Variable})"

            numeric_string = f"\\arcsin({item1.Value})"

        case 'arccos':
            variable_string = f"\\arccos({item1.Variable})"

            numeric_string = f"\\arccos({item1.Value})"

        case 'arctan':
            variable_string = f"\\arctan({item1.Variable})"

            numeric_string = f"\\arctan({item1.Value})"

        case 'e':
            variable_string = f"e^{{{item1.Variable}}}"

            numeric_string = f"e^{{{item1.Value}}}"

        case 'log':
            variable_string = f"\\log({item1.Variable})"

            numeric_string = f"\\log({item1.Value})"

        case 'sum':
            pass

        case 'abs':
            variable_string = f"|{item1.Variable}|"

            numeric_string = f"|{item1.Value}|"

    
    return variable_string, numeric_string



def CreateErrorLatexString(operation, error_result, *value_error_pairs):

        item1, *item2 = CreateValueUncertainties(value_error_pairs)

        if item2 != []:
            item2 = item2[0]

        match operation:

            case '+':
                return ErrorBeginning2Items('+', item1, item2) + f"\\text{{, Error }} = \\sqrt{{{item1.Error}^2 + {item2.Error}^2}} \\approx {error_result}"

            case '-':
                return ErrorBeginning2Items('-', item1, item2) + f"\\text{{, Error }} = \\sqrt{{{item1.Error}^2 + {item2.Error}^2}} \\approx {error_result}"

            case '*':
                return ErrorBeginning2Items('*', item1, item2) + f"\\text{{, Error }} = {item1.Value} * {item2.Value}\\sqrt{{(\\frac{{{item1.Error}}}{{{item1.Value}}})^2 + (\\frac{{{item2.Error}}}{{{item2.Value}}})^2}} \\approx {error_result}"

            case '/':
                return ErrorBeginning2Items('/', item1, item2) + f"\\text{{, Error }} = \\frac{{{item1.Value}}}{{{item2.Value}}}\\sqrt{{(\\frac{{{item1.Error}}}{{{item1.Value}}})^2 + (\\frac{{{item2.Error}}}{{{item2.Value}}})^2}} \\approx {error_result}"

            case 'l**':
                return ErrorBeginning2Items('^', item1, item2) + f"\\text{{, Error }} = \\frac{{{item2.Value}*{item1.Value}^{item2.Value}*{item1.Error}}}{{{item1.Value}}} \\approx {error_result}"
            
            case 'r**':
                return ErrorBeginning2Items('^', item1, item2) + f"\\text{{, Error }} = {item1.Value}^{{{item2.Value}}}*\\log{{{item1.Value}}}*{item2.Error} \\approx {error_result}"

            case 'sin':
                
                format_func = lambda x: f"\\sin{{{x}}}"
                return ErrorBeginning1Item(format_func, item1) + f"\\text{{, Error }} = {item1.Error} * \\cos({item1.Value}) \\approx {error_result}"

            case 'cos':
                
                format_func = lambda x: f"\\cos{{{x}}}"
                return ErrorBeginning1Item(format_func, item1) + f"\\text{{, Error }} = {item1.Error} * \\sin({item1.Value}) \\approx {error_result}"

            case 'tan':
                format_func = lambda x: f"\\tan{{{x}}}"
                return ErrorBeginning1Item(format_func, item1) + f"\\text{{, Error }} = {item1.Error} * \\sec^2({item1.Value}) \\approx {error_result}"

            case 'arcsin':
                pass

            case 'arccos':
                pass

            case 'arctan':
                pass

            case 'e':
                format_func = lambda x: f"e^{{{x}}}"
                return ErrorBeginning1Item(format_func, item1) + f"\\text{{, Error}} = {item1.Error} * e^{{{item1.Value}}} \\approx {error_result}"

            case 'log':
                pass