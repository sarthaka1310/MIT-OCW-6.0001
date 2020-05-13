semi_annual_raise = .07
portion_down_payment = 0.25
total_cost = 10**6
t = 36
r=.04
amt = int(portion_down_payment*total_cost) #total amount to be saved

starting_salary = int(input("Enter the starting salary: "))

#debugging statement
#print("amt : ", amt)

def calc(midnum):

    portion_saved = float(midnum)/10**4

    #debugging statement
    #print("percentage saved from salary: ", portion_saved)

    current_savings = 0
    annual_salary = starting_salary

    for i in range(1, t+1):
        val = (portion_saved*annual_salary)
        current_savings += ((current_savings*r) + val)//12

        #debugging
        #print("savings: ", int(current_savings))

        if i % 6 == 0:
            annual_salary += annual_salary*semi_annual_raise
    #print(int(midnum), int(amt - current_savings))
    return amt-current_savings


l = 0 #lower bound
u = 10000 #upper bound
mid = 1
steps = 0

# binary(or bisection) search over [0,10000]
while l <= u:
    steps += 1
    mid = l+(u-l)//2
    x = calc(mid)
    #debugging statement
    #print("mid :", mid," x: ", x)

    if(abs(x) < 100):
        break
    elif x > 0:
        l = mid+1
    else:
        u = mid-1

if abs(x) < 100:
    print("Best savings rate:​ 0.", mid,sep='')
    print("Steps in bisection search:​ ", steps, sep='')
else:
    print("It is not possible to pay the down payment in three years.")
