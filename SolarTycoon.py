# Define variables
day = 0
money = 1000
solar_panels = 1
problems = 0
# Track upgrade levels for each panel
solar_panel_upgrades = [0 for _ in range(solar_panels)]
# Track age for each panel
solar_panel_ages = [0 for _ in range(solar_panels)]
stability_level = 0
stability_upgrade_cost = 1000
import random

# Randomly generate problems for the day (example: 0-3 problems)
def get_problem_chance():
    # Base chance increases with panels, reduced by stability
    base_chance = min(0.05 + 0.02 * solar_panels, 0.95)
    reduction = 0.10 * stability_level
    chance = max(base_chance - reduction, 0)
    return chance

def roll_for_problems():
    chance = get_problem_chance()
    if random.random() < chance:
        # Number of problems increases with panels
        return random.randint(1, max(1, solar_panels // 2))
    else:
        return 0

problems = roll_for_problems()
if day == 0:
    print("Hello and welcome to Solar Tycoon")

# Infinite game loop
while True:
    print("\nYou have " + str(money) + " dollars and " + str(solar_panels) + " solar panals")
    # Show panel status: active/inactive
    active_panels = solar_panels - problems
    inactive_panels = problems
    for i in range(solar_panels):
        status = "ACTIVE" if i < active_panels else "INACTIVE"
        print(f"Solar Panel {i+1}: Upgrade Level {solar_panel_upgrades[i]} Age: {solar_panel_ages[i]} [{status}]")
    fail_rate = get_problem_chance()
    print(f"System Stability Level: {stability_level} (Fail Rate: {int(fail_rate*100)}%)")
    if fail_rate > 0.75:
        print(f"5. Upgrade Stability for {stability_upgrade_cost} dollars")
    print("Day " + str(day) + " : What will you do today? ")
    print("1. Buy a new solar panel for 500 dollars")
    print("2. End the day")
    print("3. Upgrade a solar panel for 200 dollars (choose which one)")
    print("6. Upgrade ALL solar panels for 200 dollars each")
    if problems > 0:
        print("4. Fix Problems for: " + str(problems * 100) + " dollars")

    # Softlock detection: can't earn, can't fix, can't buy, can't upgrade
    can_earn = active_panels > 0
    can_fix = problems > 0 and money >= problems * 100
    can_buy = money >= 500
    can_upgrade_panel = money >= 200 and active_panels > 0
    can_upgrade_stability = fail_rate > 0.75 and money >= stability_upgrade_cost
    if not (can_earn or can_fix or can_buy or can_upgrade_panel or can_upgrade_stability):
        print("\nGAME OVER: You are softlocked!")
        retry = input("Try again? (y/n): ")
        if retry.lower() == "y":
            # Reset game state
            day = 0
            money = 1000
            solar_panels = 1
            solar_panel_upgrades = [0]
            stability_level = 0
            stability_upgrade_cost = 1000
            problems = roll_for_problems()
            print("\nRestarting game...")
            continue
        else:
            print("Thanks for playing!")
            break

    if fail_rate > 0.75:
        choice = input("Enter your choice (1-6): ")
    else:
        choice = input("Enter your choice (1-4 or 6): ")
    if choice == "1":
        if money >= 500:
            solar_panels += 1
            solar_panel_upgrades.append(0)
            solar_panel_ages.append(0)
            money -= 500
            print("Bought a new solar panel!")
        else:
            print("Not enough money!")
    elif choice == "2":
        # End the day, earn money based on active panels and upgrades
        panel_earnings = []
        for i in range(active_panels):
            # Panel earning by age: 100, 75, 50, 25, 0
            if solar_panel_ages[i] == 0:
                earn = 100
            elif solar_panel_ages[i] == 1:
                earn = 75
            elif solar_panel_ages[i] == 2:
                earn = 50
            elif solar_panel_ages[i] == 3:
                earn = 25
            else:
                earn = 0
            panel_earnings.append(earn)
        daily_income = sum(panel_earnings)
        money += daily_income
        day += 1
        # Age all panels by 1 day
        for i in range(solar_panels):
            solar_panel_ages[i] += 1
        problems = roll_for_problems()
        print(f"Day ended. You earned {daily_income} dollars.")
    elif choice == "3":
        panel_num = input(f"Which panel to upgrade? (1-{solar_panels}): ")
        try:
            panel_idx = int(panel_num) - 1
            if 0 <= panel_idx < solar_panels:
                if money >= 200:
                    solar_panel_upgrades[panel_idx] += 1
                    money -= 200
                    print(f"Upgraded Solar Panel {panel_idx+1} to Level {solar_panel_upgrades[panel_idx]}")
                else:
                    print("Not enough money!")
            else:
                print("Invalid panel number!")
        except ValueError:
            print("Invalid input!")
    elif choice == "6":
        total_cost = 200 * solar_panels
        if money >= total_cost:
            for i in range(solar_panels):
                solar_panel_upgrades[i] += 1
            money -= total_cost
            print(f"Upgraded ALL solar panels to next level for {total_cost} dollars!")
        else:
            print("Not enough money to upgrade all panels!")
    elif choice == "4" and problems > 0:
        if money >= problems * 100:
            money -= problems * 100
            print(f"Fixed {problems} problems for {problems * 100} dollars.")
            problems = 0
        else:
            print("Not enough money to fix problems.")
    else:
        print("Invalid choice!")
    if choice == "5" and fail_rate > 0.75:
        if money >= stability_upgrade_cost:
            stability_level += 1
            money -= stability_upgrade_cost
            stability_upgrade_cost = int(stability_upgrade_cost * 1.5)
            print(f"Stability upgraded to level {stability_level}!")
        else:
            print("Not enough money to upgrade stability!")
