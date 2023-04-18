from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

available_menu = Menu()
coffee_machine = CoffeeMaker()
piggy_bank = MoneyMachine()
machine_on = True

while machine_on:
    available_drinks = available_menu.get_items()
    drink_selection = input(f"What would you like? ({available_drinks}): ")
    if drink_selection == "off":
        print("The coffee machine has been turned off.")
        machine_on = False
    elif drink_selection == "report":
        coffee_machine.report()
        piggy_bank.report()
    else:
        if drink_selection in available_drinks:
            drink = available_menu.find_drink(drink_selection)
            if coffee_machine.is_resource_sufficient(drink) and piggy_bank.make_payment(drink.cost):
                coffee_machine.make_coffee(drink)
        else:
            print("Sorry, that drink is not available. Please select another.")
