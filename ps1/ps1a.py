portion_down_payment = 0.25
current_savings=0
r=0.04

annual_salary=int(input("Enter your annual salary: "))
portion_saved=float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost=int(input("Enter the cost of your dream home: "))

t=0 #number of months required
amt=portion_down_payment*total_cost
val= (portion_saved*annual_salary)/12

while current_savings<amt :
    t+=1
    current_savings+=current_savings*(r/12) + val

print("Number of months", t)