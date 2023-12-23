import numpy as np

class ValueUncertainty:
    
    _values_dict = {}

    _capture_calcs = False

    _last_operation = ''

    _last_var = ['@0#']

    @property
    def mean(self):

        return ValueUncertainty.sum(self) / len(self)
    

    @property
    def population_variance(self):

        numerator = (self - self.mean)**2

        return ValueUncertainty.sum(numerator) / len(self)


    @property
    def sample_variance(self):
        
        numerator = (self - self.mean)**2

        return ValueUncertainty.sum(numerator) / (len(self) - 1)


    @property
    def zipped(self):
        return zip(self.values.tolist(), self.errors.tolist())
    

    def __init__(self, values, errors = [], variable_name = ''):
        
        if not (values is np.ndarray):

            if hasattr(values, '__iter__'):

                values = np.array(list(values))

            elif type(values) == int or type(values) == float:
                
                values = np.array([values])
            
            else:
                raise ValueError("values field must be castable to a list, or a number (float/int)")
        
        if (type(errors) != np.ndarray):
             
            if hasattr(errors, '__iter__'):

                errors = np.array(list(errors))

            elif type(errors) == int or type(errors) == float:
                
                errors = np.array([errors])
            
            else:
                raise ValueError("errors field must be castable to a list, or a number (float/int)")
        
        if (len(errors) == 0):
            errors = np.array([0.0] * len(values))
        
        if len(values) != len(errors):
            raise ValueError("Values and errors must have the same length")

        self.values = values

        self.errors = abs(errors)

        self._variable_name = variable_name


    def __len__(self):
        return len(self.values)
    

    def __iter__(self):

        for value, error in self.zipped:

            yield ValueUncertainty(value, error)

    # Making i a tuple to allow for multi indexing?
    def __getitem__(self, i):
        
        if type(i) != int:
            raise IndexError(f"When indexing the index varible must be type 'int', not {type(i)}")
        
        return ValueUncertainty(self.values[i], self.errors[i])

    # Making i a tuple to allow for multi indexing?
    def __setitem__(self, i, value):
        
        if type(value) != ValueUncertainty:
            raise ValueError(f"Value must be of type ValueUncertainty, not {type(value)}")
        
        if len(value) > 1:
            raise ValueError(f"Value must have a length of 1, not {len(value)}")

        self.values[i] = value.values[0]

        self.errors[i] = value.errors[0]
    

    def __str__(self) -> str:

        s = [f'{round(value,2)} ± {round(error,2)}' for value, error in self.zipped]

        return f'[{", ".join(s)}]'
    

    def __add__(self, addend):

        if type(addend) == ValueUncertainty:

            values = self.values + addend.values

            errors = np.sqrt(self.errors**2 + addend.errors**2)

            if self._capture_calcs:

                self._format_value_calcs('+',(self._variable_name, self.values[0]), (addend._variable_name, addend.values[0]))

        else:

            values = self.values + addend

            errors = self.errors

            if self._capture_calcs:

                self._format_value_calcs('+',(self._variable_name, self.values[0]), (str(addend), addend))
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)



    def __mul__(self, factor):

        

        if type(factor) == ValueUncertainty:

            values = self.values * factor.values

            errors = values * np.sqrt((self.errors / self.values)**2 + (factor.errors / factor.values)**2)

            if self._capture_calcs:

                self._format_value_calcs('*',(self._variable_name, self.values[0]), (factor._variable_name, factor.values[0]))

        else:

            values = self.values * factor

            errors = self.errors * factor

            if self._capture_calcs:

                self._format_value_calcs('*',(self._variable_name, self.values[0]), (str(factor), factor))

        variable = ValueUncertainty._get_var()
        
        return ValueUncertainty(values, errors, variable_name=variable)


    def __truediv__(self, divisor):
        

        if type(divisor) == ValueUncertainty:

            values = self.values / divisor.values

            errors = values * np.sqrt((self.errors / self.values)**2 + (divisor.errors / divisor.values)**2)

            if self._capture_calcs:

                self._format_value_calcs('/',(self._variable_name, self.values[0]), (divisor._variable_name, divisor.values[0]))

        else:
            values = self.values / divisor

            errors = self.errors / divisor

            if self._capture_calcs:

                self._format_value_calcs('/',(self._variable_name, self.values[0]), (str(divisor), divisor))
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rtruediv__(self, quotient):


        if type(quotient) == ValueUncertainty:

            values = quotient.values / self.values

            errors = values * np.sqrt((self.errors / self.values)**2 + (quotient.errors / quotient.values)**2)

            if self._capture_calcs:

                self._format_value_calcs('/', (quotient._variable_name, quotient.values[0]), (self._variable_name, self.values[0]))

        else:
            values = quotient / self.values

            errors = values * self.errors / self.values

            if self._capture_calcs:

                self._format_value_calcs('/', (str(quotient), quotient), (self._variable_name, self.values[0]))
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)
    

    def __pow__(self, power): 

        values = self.values ** power
        
        errors = power * values * self.errors / self.values

        if self._capture_calcs:

                self._format_value_calcs('**',(self._variable_name, self.values[0]), (str(power), power))

        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rpow__(self, base):

        

        values = base ** self.values

        errors = values * np.log(base) * self.errors

        if self._capture_calcs:

            self._format_value_calcs('**', (str(base), base), (self._variable_name, self.values[0]))

        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __radd__(self, addend):
        return self + addend


    def __sub__(self, term):


        if type(term) == ValueUncertainty:

            values = self.values - term.values

            errors = np.sqrt(self.errors**2 + term.errors**2)

            if self._capture_calcs:

                self._format_value_calcs('-',(self._variable_name, self.values[0]), (term._variable_name, term.values[0]))

        else:

            values = self.values - term

            errors = self.errors

            if self._capture_calcs:

                self._format_value_calcs('-',(self._variable_name, self.values[0]), (str(term), term))
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rsub__(self, term):


        if type(term) == ValueUncertainty:

            values = term.values - self.values

            errors = np.sqrt(self.errors**2 + term.errors**2)

            if self._capture_calcs:

                self._format_value_calcs('-', (term._variable_name, term.values[0]), (self._variable_name, self.values[0]))

        else:

            values = term - self.values

            errors = self.errors

            if self._capture_calcs:

                self._format_value_calcs('-', (str(term), term),(self._variable_name, self.values[0]))
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rmul__(self, factor):
        return self * factor
    

    def __abs__(self):
        return ValueUncertainty(abs(self.values), self.errors)
    

    @staticmethod
    def sqrt(rooted):
        return rooted ** (1/2)
    

    @staticmethod
    def sum(iterable):
        
        ## Format string for the sum method

        result = 0

        for item in iterable:
            result += item
        
        return result


    @staticmethod
    def sin(value_uncertainty):
        pass


    @staticmethod
    def cos(value_uncertainty):
        pass


    @staticmethod
    def tan(value_uncertainty):
        pass


    @staticmethod
    def arcsin(value_uncertainty):
        pass


    @staticmethod
    def arccos(value_uncertainty):
        pass


    @staticmethod
    def arctan(value_uncertainty):
        pass

    @staticmethod
    def StartCalcCapture(precision = 4):
        
        ValueUncertainty._capture_calcs = True

        ValueUncertainty._precision = precision
    
    @staticmethod
    def EndCalcCapture():

        current_var = ValueUncertainty._last_var[0]

        next_var = f"@{int(current_var[1:-1]) + 1}#"

        next_result = str(eval(ValueUncertainty._values_dict[current_var][1]))

        value_dict = ValueUncertainty._values_dict

        value_dict[next_var] = (current_var, next_result)

        final_var = f"@{int(current_var[1:-1]) + 2}#"

        value_dict[final_var] = (next_var, '')        
        
        latex_list = ValueUncertainty._recursive_formula_creater(value_dict[final_var][0])

        latex_list.reverse()

        ValueUncertainty._values_dict = {}

        ValueUncertainty._capture_calcs = False

        ValueUncertainty._last_operation = ''

        ValueUncertainty._last_var = ['@0#']

        return latex_list



    def _format_value_calcs(self, operation, *variable_value_pairs):
        
        self._update_last_var()

        match operation:

            case '+':

                self._basic_opertaion(operation, *variable_value_pairs)
                return

            case '-':

                self._basic_opertaion(operation, *variable_value_pairs)
                return

            case '*':

                self._basic_opertaion(operation, *variable_value_pairs)
                return

            case '/':
                
                self._last_operation = '/'

                variable_string = f"\\frac{{{variable_value_pairs[0][0]}}}{{{variable_value_pairs[1][0]}}}"

                numeric_string = f"\\frac{{{round(variable_value_pairs[0][1], self._precision)}}}{{{round(variable_value_pairs[1][1], self._precision)}}}" 

            case '**':
                self._last_operation = '**'

                variable_string = f"{variable_value_pairs[0][0]}^{{{variable_value_pairs[1][0]}}}"

                numeric_string = f"{round(variable_value_pairs[0][1], self._precision)}^{{{round(variable_value_pairs[1][1], self._precision)}}}" 
            
            case 'sin':
                return

            case 'cos':
                return 

            case 'tan':
                return 

            case 'arcsin':
                return
            
            case 'arccos':
                return

            case 'arctan':
                return

            case 'e':
                return

            case 'log':
                return

        self._values_dict[self._last_var[0]] = (variable_string, numeric_string)


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


    def _basic_opertaion(self, *args):

        self._last_operation = args[0]

        variable_string = f"{args[1][0]} {args[0]} {args[2][0]}"

        numeric_string = f"{round(args[1][1], self._precision)} {args[0]} {round(args[2][1], self._precision)}"
        
        self._values_dict[self._last_var[0]] = (variable_string, numeric_string) 


    def _update_last_var(self):
        ValueUncertainty._last_var[0] = f"@{int(self._last_var[0][1:-1]) + 1}#"

    @staticmethod
    def _recursive_formula_creater(current_str : str):
        
        start_ind = current_str.find("@")

        if start_ind == -1:
            return ['$' + current_str + '$'] # Need to put something here
        
        else:

            end_ind = current_str.find('#')

            dict_value = ValueUncertainty._values_dict[current_str[start_ind:end_ind+1]]

            result_str = current_str.replace(current_str[start_ind:end_ind+1], dict_value[1])

            while result_str.find('@') != -1:

                next_start = result_str.find('@')

                next_end = result_str.find('#')

                next_var = result_str[next_start:next_end + 1]

                result_str = result_str.replace(next_var, ValueUncertainty._values_dict[next_var][1])

            variable_str = current_str.replace(current_str[start_ind:end_ind+1], dict_value[0])

            return ['$' + result_str + '$'] + ValueUncertainty._recursive_formula_creater(variable_str)

    @staticmethod
    def _get_var():

        if ValueUncertainty._capture_calcs:
            variable = ValueUncertainty._last_var[0]

        else:
            variable = ''
        
        return variable







