from Error import ValueUncertainty



# e = ValueUncertainty([1, 2, 1], [0.5, 0.5, 0.5])

a = ValueUncertainty([1,2], variable_name='a')

b = ValueUncertainty([2,1], variable_name='b')

ValueUncertainty.StartCalcCapture()

r = a**2 / 3 * 3 * b

[print(n) for n in ValueUncertainty.EndCalcCapture()]