import numpy as np

from Utilities import *

class ValueUncertainty:
    
    _values_dict = {}

    _capture_calcs = False

    _last_operation = ''

    _last_var = '@0#'

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

        else:

            values = self.values + addend

            errors = self.errors
        
        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('+', self, addend)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)



    def __mul__(self, factor):


        if type(factor) == ValueUncertainty:

            values = self.values * factor.values

            errors = values * np.sqrt((self.errors / self.values)**2 + (factor.errors / factor.values)**2)

        else:

            values = self.values * factor

            errors = self.errors * factor

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('*', self, factor)

        variable = ValueUncertainty._get_var()
        
        return ValueUncertainty(values, errors, variable_name=variable)


    def __truediv__(self, divisor):
        

        if type(divisor) == ValueUncertainty:

            values = self.values / divisor.values

            errors = values * np.sqrt((self.errors / self.values)**2 + (divisor.errors / divisor.values)**2)

        else:
            values = self.values / divisor

            errors = self.errors / divisor

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('/', self, divisor)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rtruediv__(self, quotient):


        if type(quotient) == ValueUncertainty:

            values = quotient.values / self.values

            errors = values * np.sqrt((self.errors / self.values)**2 + (quotient.errors / quotient.values)**2)

        else:
            values = quotient / self.values

            errors = values * self.errors / self.values

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('/', quotient, self)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)
    

    def __pow__(self, power): 

        values = self.values ** power
        
        errors = power * values * self.errors / self.values

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('**', self, power)

        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rpow__(self, base):

        

        values = base ** self.values

        errors = values * np.log(base) * self.errors

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('**', base, self)

        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __radd__(self, addend):
        return self + addend


    def __sub__(self, term):


        if type(term) == ValueUncertainty:

            values = self.values - term.values

            errors = np.sqrt(self.errors**2 + term.errors**2)

        else:

            values = self.values - term

            errors = self.errors

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('-', self, term)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rsub__(self, term):


        if type(term) == ValueUncertainty:

            values = term.values - self.values

            errors = np.sqrt(self.errors**2 + term.errors**2)

        else:

            values = term - self.values

            errors = self.errors

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('-', term, self)

        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    def __rmul__(self, factor):
        return self * factor
    

    def __abs__(self):

        if ValueUncertainty._capture_calcs:
            ValueUncertainty._format_value_calcs('abs', self)

        variable = self._get_var()

        return ValueUncertainty(abs(self.values), self.errors, variable_name=variable)
    

    @staticmethod
    def sqrt(rooted):

        ## Format string for sqrt

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
        """
        IN RADS
        """
        
        if type(value_uncertainty) == ValueUncertainty:

            values = np.sin(value_uncertainty.values)

            errors = np.cos(value_uncertainty.values) * value_uncertainty.errors

        else:

            values = np.sin(value_uncertainty)

            errors = 0

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('sin', value_uncertainty)

        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)

    @staticmethod
    def cos(value_uncertainty):
        """
        IN RADS
        """
        
        if type(value_uncertainty) == ValueUncertainty:

            values = np.cos(value_uncertainty.values)

            errors = np.sin(value_uncertainty.values) * value_uncertainty.errors

        else:

            values = np.cos(value_uncertainty)

            errors = 0

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('cos', value_uncertainty)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    @staticmethod
    def tan(value_uncertainty):
        """
        IN RADS
        """
        
        if type(value_uncertainty) == ValueUncertainty:

            values = np.tan(value_uncertainty.values)

            errors =  value_uncertainty.errors / ((np.cos(value_uncertainty.values)) ** 2)
            
        else:

            values = np.tan(value_uncertainty)

            errors = 0

        if ValueUncertainty._capture_calcs:
            ValueUncertainty._format_value_calcs('tan', value_uncertainty)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    @staticmethod
    def arcsin(value_uncertainty):
        """
        IN RADS
        """
        
        if type(value_uncertainty) == ValueUncertainty:

            values = np.arcsin(value_uncertainty.values)

            errors =  1 / np.sqrt(1 - (value_uncertainty.values**2)) * value_uncertainty.errors
            
        else:

            values = np.arcsin(value_uncertainty)

            errors = 0

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('arcsin', value_uncertainty)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    @staticmethod
    def arccos(value_uncertainty):
        """
        IN RADS
        """
        
        if type(value_uncertainty) == ValueUncertainty:

            values = np.arccos(value_uncertainty.values)

            errors =  -1 / np.sqrt(1 - (value_uncertainty.values**2)) * value_uncertainty.errors
            
        else:

            values = np.arccos(value_uncertainty)

            errors = 0

        if ValueUncertainty._capture_calcs:
            
            ValueUncertainty._format_value_calcs('arccos', value_uncertainty)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    @staticmethod
    def arctan(value_uncertainty):
        """
        IN RADS
        """
        
        if type(value_uncertainty) == ValueUncertainty:

            values = np.arctan(value_uncertainty.values)

            errors =  1 / (1 + (value_uncertainty.values**2)) * value_uncertainty.errors
            
        else:

            values = np.arctan(value_uncertainty)

            errors = 0

        if ValueUncertainty._capture_calcs:

            ValueUncertainty._format_value_calcs('arctan', value_uncertainty)
        
        variable = ValueUncertainty._get_var()

        return ValueUncertainty(values, errors, variable_name=variable)


    @staticmethod
    def StartCalcCapture(precision = 4):
        
        ValueUncertainty._capture_calcs = True

        ValueUncertainty._precision = precision
    
    @staticmethod
    def EndCalcCapture():

        current_var = ValueUncertainty._last_var

        next_var = f"@{int(current_var[1:-1]) + 1}#"

        next_result = str(eval(ValueUncertainty._values_dict[current_var][1]))

        value_dict = ValueUncertainty._values_dict

        value_dict[next_var] = (current_var, next_result)

        final_var = f"@{int(current_var[1:-1]) + 2}#"

        value_dict[final_var] = (next_var, '')        
        
        latex_list = LatexCreator(value_dict[final_var][0], value_dict)

        latex_list.reverse()

        ValueUncertainty._values_dict = {}

        ValueUncertainty._capture_calcs = False

        ValueUncertainty._last_operation = ''

        ValueUncertainty._last_var = '@0#'

        return latex_list


    @staticmethod
    def _format_value_calcs(operation, *items):
        
        ValueUncertainty._update_last_var()

        items_func = lambda ele: (ele._variable_name, ele.values[0]) if type(ele) == ValueUncertainty else (str(ele), ele)

        variable_values = tuple(map(items_func, items))

        variable_str, numeric_str = CreateValueLatexSting(operation, *variable_values)

        ValueUncertainty._values_dict[ValueUncertainty._last_var] = (variable_str, numeric_str)


    @staticmethod
    def _update_last_var():
        ValueUncertainty._last_var = f"@{int(ValueUncertainty._last_var[1:-1]) + 1}#"


    @staticmethod
    def _get_var():

        if ValueUncertainty._capture_calcs:
            variable = ValueUncertainty._last_var

        else:
            variable = ''
        
        return variable







