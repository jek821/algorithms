import numpy as np
np.random.seed(20)
n = 12
m = 1
min_possible_demand = 1
max_possible_demand = 20
d = np.random.randint(min_possible_demand, max_possible_demand, n)
big_d = sum(d)
dp = np.full((n+1, big_d+1), np.inf)
dp[n,0] = 0

def c(x):
    return x*3

def h(x):
    return x*5

print(f"Demands: {d}")
print(f"First month demand: {d[0]}")

# Debug first month, inventory 0 calculation
print("\nDebugging inventory 0, month 0:")
inventory = 0
month = 0

if d[month] == (inventory+m) or d[month] == inventory:
    print(f"Case 1: Exact match")
    print(f"Cost would be: {dp[month+1,0]}")
elif d[month] > (m+inventory):
    overtime = d[month]-(inventory+m)
    cost = dp[month+1,0] + c(overtime)
    print(f"Case 2: Need overtime")
    print(f"Demand: {d[month]}")
    print(f"Can produce regularly: {m}")
    print(f"Need overtime: {overtime}")
    print(f"Overtime cost: {c(overtime)}")
    print(f"Next month base cost: {dp[month+1,0]}")
    print(f"Total cost: {cost}")
else:
    print(f"Case 3: Regular production options")
    min_cost = float('inf')
    for potential_production in range(m+1):
        target_column = inventory - d[month] + potential_production
        if 0 <= target_column <= big_d:
            if target_column > 0:
                current_cost = h(target_column) + dp[month+1, target_column]
                print(f"Production {potential_production}, target inventory {target_column}")
                print(f"Cost = holding({target_column}): {h(target_column)} + future: {dp[month+1, target_column]} = {current_cost}")
            else:
                current_cost = dp[month+1, target_column]
                print(f"Production {potential_production}, target inventory {target_column}")
                print(f"Cost = future: {dp[month+1, target_column]}")
            min_cost = min(min_cost, current_cost)
    print(f"Final min cost: {min_cost}")

print("\nFirst few values of final solution:")
for i in range(5):
    print(f"Starting inventory {i}: {dp[0,i]}")