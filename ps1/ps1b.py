portion_down_payment = 0.25
current_savings=0
r=0.04

annual_salary=int(input("Enter your annual salary: "))
portion_saved=float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost=int(input("Enter the cost of your dream home: "))
semi_annual_raise=float(input("Enter the semi­annual raise, as a decimal:​ "))

t=0 #number of months required
amt=portion_down_payment*total_cost

while current_savings<amt :
    t+=1
    val= (portion_saved*annual_salary)/12
    current_savings+=current_savings*(r/12) + val
    if t%6==0:
        annual_salary+=annual_salary*semi_annual_raise

print("Number of months", t)