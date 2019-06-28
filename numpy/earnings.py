salary = 5413
vacation_yield = 2946 / 5313
vacation_money = vacation_yield * salary

xmas_yield = 2946 / 5313
xmas_money = xmas_yield * salary
tzug = 0.27 * salary

epm = (salary*12 + vacation_money + xmas_money + tzug)/12

print("Salary: {:f}".format(salary))
print("Factor:  {:f}".format(salary/epm))
print("Effective salary: {:f}".format(epm))
print("Difference: {:f}".format(epm-salary))
print("Emergency per Month: {:f}".format((epm-salary)*0.6))