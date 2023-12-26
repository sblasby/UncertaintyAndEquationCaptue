"""
Houses functions that work to create the latex formatting 
"""

from collections import namedtuple


def CreateVariableValues(*variable_value_pairs):
    """
    Takes in any number of tuples each of length 2, then
    formats and returns a list of named tuples
    """

    VariableValue = namedtuple('VariableValue', ["Variable", "Value"])

    return tuple(map(lambda tup: VariableValue(*tup), *variable_value_pairs))


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



def _format_error_calcs(self, value_error1: tuple, value_error2: tuple, operation):

        value1, error1 = value_error1
        value2, error2 = value_error2

        match operation:

            case '+':
                pass

            case '-':
                pass

            case '*':
                pass

            case '/':
                pass

            case '**':
                pass
            
            case 'sin':
                pass

            case 'cos':
                pass

            case 'tan':
                pass

            case 'arcsin':
                pass

            case 'arccos':
                pass

            case 'arctan':
                pass

            case 'e':
                pass

            case 'log':
                pass