import json
import random


class Restro:
    def __init__(self, c_name, c_num):
        self.c_name = c_name
        self.c_num = c_num

    def showmenu(self):
        menu = open('menu.json', 'r')
        self.all_data = json.loads(menu.read())
        menu.close()
        print('OPTION', 'ITEM', 'PRICE')
        for i, j in enumerate(self.all_data['data']):
            print(i + 1, j['item_name'], j['price'])
        return len(self.all_data['data'])

    def select_dishes(self, item):
        self.items = item
        print("===============  SELECTED DISHES  ====================")
        print('Item', 'Quantity')
        for i in item:
            print(self.all_data['data'][i['dish_option']]['item_name'], i['qty'])

    def generatereciept(self, student):
        order_number = f'OD{random.randint(1111, 9999)}'
        order_str = f'ORDER NUMBER : {order_number}\nCUSTOMER NAME : {self.c_name}\nCUSTOMER PHONE No : {self.c_num}\n'
        order_str += 'ORDERS\n********************\nITEM  QUANTITY PRICE\n'
        gt = 0
        for i in self.items:
            item_dict = self.all_data['data'][i['dish_option']]
            sum_price = item_dict['price'] * i['qty']
            order_str += f'{item_dict["item_name"]}     {i["qty"]}      {sum_price}\n'
            gt += sum_price
        order_str += '\n'
        if student == 'y':
            order_str += 'STUDENT DISCOUNT 5%\n'
            gt -= gt / 100 * 5

        order_str += 'TAX              18%\n'
        gt += gt / 100 * 18
        order_str += '********************\n'
        order_str += f'GRAND TOTAL     {round(gt)}/-'
        f = open(order_number + '.txt', 'w')
        f.write(order_str)
        f.close()
        return order_number + '.txt', gt


print("===== WELCOME TO RAIPUR RESTORENT ========\n")
u_name = input("Enter Your Name: ").title()
flag = True
while flag:
    u_mob = input("Enter Your Mobile Number: ")
    if len(u_mob) != 10 or u_mob[0] == "0":
        print("Mobile Number must be 10 digit and first digit should not be zero")
        continue
    if u_mob[0] not in "6789":
        print("Mobile Number Must Start with 6 to 9")
        continue
    for i in u_mob:
        if i.isalpha():
            print("Only Digit Allowed !")
            flag = False
            break
    if flag:
        flag = False
    else:
        flag = True

print("===== MENU ========\n")

hotel = Restro(u_name, u_mob)

items_selected = []

while True:
    total_dish = hotel.showmenu()
    try:
        user_s = input("Select Option: ")
        if user_s == '':
            break
        if int(user_s) > total_dish:
            print("Enter Option From 1 -", total_dish)
            continue
        option = int(user_s) - 1
        qty = int(input("Enter Quantity: "))
    except:
        print("Only Number Allowed")
    update = False
    for i in items_selected:
        if i['dish_option'] == option:
            i['qty'] += 1
            update = True
    if not update:
        items_selected.append({'dish_option': option, 'qty': qty})

hotel.select_dishes(items_selected)
input("Continue to Pay ? [Press Enter]")
while True:
    student = input("Are You A Student? [y/n]").lower()
    if student not in ['y', 'n']:
        print("Type [y/n] only !")
    else:
        break

amount = hotel.generatereciept(student)
print("Receipt Generated.", amount[0], "\nTotal Amount:", round(amount[1]), '/-')
