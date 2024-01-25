"""

This is the code for a shopping system called 'Digital Dynasty,' designed to make your online shopping journey enjoyable and convenient.

The platform includes user and seller logins and provides the following key features:

1. Login
2. Guest Login
3. Sign Up
4. Register as a Seller
5. Help
6. Forgot Password
7. Quit

It also checks whether the username for a new user or seller is already taken by someone else.

There are multiple options for both. Let's start with user features:

User Key Features:
1. Shop (users can buy anything available)
2. Cancel Orders
3. Change Account Settings
4. View Purchase History
5. Delete Account

Users can also purchase multiple items at once using the Add to Cart option. During checkout, users can view and change details such as name, address, phone number, etc.

Now, let's explore seller key features:

Seller Key Features:
1. Add a Product
2. Remove a Product
3. Edit Products
4. View My Products
5. View Order History
6. Account Settings
7. Delete Your Account

All data is securely saved to ensure no information is lost.

"""

from datetime import datetime
import os


class Product():

    def add_product(self, seller_info):
        self.clear_console()

        print("**************************************************")
        print("               Add a Product")
        print("**************************************************")

        name = input("Name of the Product: ")
        price = input("Price: ")
        quantity = input("Quantity: ")
        description = input("Description: ")

        product = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "description": description
        }

        product_str = f'{{"Name": "{name}", "Price": "{price}", "Quantity": "{quantity}", "Description": "{description}"}}'

        print("\nProduct Details:\n")
        for key, value in product.items():
            print(f"{key}: {value}")

        choice = input("\n1. Add\n2. Cancel\nEnter Your Choice (1 or 2): ")

        if choice == "1":
            # Update the product_data
            new_product_data = {"seller_name": seller_info["seller"]["store_name"], "product": product}
            self.product_data.append(new_product_data)
            self.save_product_data()

            self.clear_console()
            print("************************************************************")
            print("            The Product has been Added Successfully!")
            print("************************************************************")
        elif choice == "2":
            self.clear_console()
        else:
            print("Invalid Choice. Returning to Seller Menu.")


    def remove_product(self, seller_info):
        self.clear_console()

        print("**************************************************")
        print("             Remove a Product")
        print("**************************************************")

        # Update how you retrieve the seller's products
        seller_name = seller_info['seller']['store_name']
        seller_products = [item['product'] for item in self.product_data if item['seller_name'] == seller_name]

        if not seller_products:
            print("No Products to Remove.")
            return

        print("\nYour Products:\n")
        for idx, product in enumerate(seller_products, start=1):
            print(f"{idx}. {product['name']}")

        try:
            choice = input("\nEnter the Number of the Product to Remove or Press Enter to Cancel: ")
            if choice:
                idx = int(choice) - 1
                if 0 <= idx < len(seller_products):
                    removed_product = seller_products.pop(idx)

                    # Update the product_data
                    self.product_data = [item for item in self.product_data if not (item['seller_name'] == seller_name and item['product'] == removed_product)]
                    self.save_product_data()

                    print(f"\nThe Product '{removed_product['name']}' has been Removed Successfully!")
                else:
                    print("Invalid Choice. Returning to Seller Menu.")
            else:
                print("Returning to Seller Menu.")
        except ValueError:
            print("Invalid Input. Returning to Seller Menu.")



    def edit_products(self, seller_info):
        self.clear_console()

        print("**************************************************")
        print("           Edit Products")
        print("**************************************************")

        # Update How You Retrieve the Seller's Products
        seller_name = seller_info['seller']['store_name']
        seller_products = [item['product'] for item in self.product_data if item['seller_name'] == seller_name]

        if not seller_products:
            print("No Products to Edit.")
            input("Press Enter to Return to Seller Menu.")
            return

        print("\nYour Products:\n")

        for idx, product_dict in enumerate(seller_products, start=1):
            print(f" {idx}.\n Name: {product_dict.get('name')}\n Price: {product_dict.get('price')}$\n Quantity: {product_dict.get('quantity')}\n Description: {product_dict.get('description')}\n")

        try:
            choice = int(input("Enter the Number of the Product to Edit (or 0 to Cancel): "))
        except ValueError:
            print("Invalid Input. Please Enter a Number.")
            input("Press Enter to Return to Seller Menu.")
            return

        if choice == 0:
            print("Edit Canceled.")
            input("Press Enter to Return to Seller Menu.")
            return

        if 1 <= choice <= len(seller_products):
            selected_product = seller_products[choice - 1]

            print("\nSelected Product:\n")
            print(f"Name: {selected_product.get('name')}\nPrice: {selected_product.get('price')}$\nQuantity: {selected_product.get('quantity')}\nDescription: {selected_product.get('description')}\n")

            for key in selected_product.keys():
                new_value = input(f"Enter New {key} (or Leave Blank to Keep Current): ").strip()
                if new_value:
                    selected_product[key] = new_value

            # Update the product_data
            self.product_data = [item if not (item['seller_name'] == seller_name and item['product'] == selected_product) else {'seller_name': seller_name, 'product': selected_product} for item in self.product_data]
            self.save_product_data()

            self.clear_console()
            print("\nUpdated Product:\n")
            print(f"Name: {selected_product.get('name')}\nPrice: {selected_product.get('price')}$\nQuantity: {selected_product.get('quantity')}\nDescription: {selected_product.get('description')}\n")

        else:
            print("Invalid Choice. Please Enter a Valid Number.")

        input("Press Enter to Return to Seller Menu.")


    def view_my_products(self, seller_info):
        self.clear_console()

        print("**************************************************")
        print(f"          {seller_info['seller']['store_name']}'s Products")
        print("**************************************************")
        print()

        seller_name = seller_info['seller']['store_name']

        # Get products of the seller
        seller_products = []
        for item in self.product_data:
            if item['seller_name'] == seller_name:
                seller_products.append(item['product'])

        # Check if there are no products
        if not seller_products:
            print("\nNo Products to Display\n\n.")
            input("Press Enter to Return to Seller Menu.")
            return

        # Display number of products
        num_products = len(seller_products)
        print(f"Number of Products Listed: {num_products}\n")

        print("Your Products:\n")
        for idx, product_dict in enumerate(seller_products, start=1):
            try:
                if isinstance(product_dict, dict):
                    print(f"Product {idx}:\nName: {product_dict.get('name')}\nPrice: {product_dict.get('price')}$\nQuantity: {product_dict.get('quantity')}\nDescription: {product_dict.get('description')}\n")
                else:
                    print("Error: Product Information is Not in the Expected Format.")
            except TypeError:
                print("Error: Unable to Parse Product Information.")

        input("Press Enter to Return to Seller Menu.")


class User():

    def subtract_quantity(self, selected_product, quantity):
        selected_product['quantity'] = str(int(selected_product['quantity']) - quantity)
        self.save_product_data()


    def buy_product(self, user_info, selected_product,quantity,selected_products_seller):
        self.clear_console()
        print(selected_product)
        print("**************************************************")
        print("                 Digital Dynasty")
        print("                 Purchase Summary")
        print("**************************************************\n")

        product_name = selected_product.get('name')
        product_price = float(selected_product.get('price'))

        total_amount = quantity * product_price
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\nProduct: {product_name}")
        print(f"Quantity: {quantity}")
        print(f"Price per unit: {product_price}$")
        print(f"Total Amount: {total_amount}$")
        print(f"Date: {current_date}")
        print("\n------------------------------------")

        confirmation = input("\nDo you want to confirm the purchase? (yes/no): ")
        user_data = self.user_data
        if confirmation == "yes":
            print(f"\nPlease Check Your Details.")
            self.view_account_info(user_info)
            choice2 = input("\nDo You Want To Change It? (yes/no)  : ").lower()
            if choice2 == "yes":
                self.account_settings(user_info)
                self.subtract_quantity(selected_product, quantity)

                for entry in user_data:
                    if 'seller' in entry:
                        seller_data = entry['seller']
                        if 'store_name' in seller_data and seller_data['store_name'] in selected_products_seller:
                            if 'purchase_history' in seller_data:
                                seller_data['order_history'].append(purchase_details)

                # Saving the updated product data
                self.save_product_data()

                # Add the purchase details to user's purchase history
                purchase_details = {
                    "product_name": product_name,
                    "quantity": quantity,
                    "price_per_unit": product_price,
                    "total_amount": total_amount,
                    "date": current_date
                }
                user_info['user']['purchase_history'].append(purchase_details)

                # Saving the updated user data
                self.save_user_data()

                print("\nPurchase Successful! Thank you for shopping with us.")
            elif choice2 ==  "no":
                # Subtract the bought quantity from available quantity
                selected_product['quantity'] = str(int(selected_product['quantity']) - quantity)

                # Saving the updated product data
                self.save_product_data()
                for entry in user_data:
                    if 'seller' in entry:
                        seller_data = entry['seller']
                        if 'store_name' in seller_data and seller_data['store_name'] in selected_products_seller:
                            if 'order_history' not in seller_data:
                                seller_data['order_history'] = []                
                            purchase_details = {
                                "product_name": product_name,
                                "quantity": quantity,
                                "price_per_unit": product_price,
                                "total_amount": total_amount,
                                "date": current_date
                            }
                            seller_data['order_history'].append(purchase_details)

                # Add the purchase details to user's purchase history
                purchase_details = {
                    "product_name": product_name,
                    "quantity": quantity,
                    "price_per_unit": product_price,
                    "total_amount": total_amount,
                    "date": current_date
                }
                user_info['user']['purchase_history'].append(purchase_details)

                # Save the updated user data
                self.save_user_data()

                print("\nPurchase Successful! Thank you for shopping with us.")
        else:
            print("\nPurchase canceled. Returning to the shop menu.")



    def add_to_cart(self, user_info, product):
        global quantity_to_add
        quantity_to_add = int(input(f"\nHow many units of '{product['name']}' do you want to add to your cart? "))

        if 0 < quantity_to_add <= int(product['quantity']):
            # Add product to user's cart
            cart_item = {
                "Product Name": product['name'],
                "Quantity": quantity_to_add,
                "Price per unit": float(product['price'])
            }

            # Updating the cart
            user_info['user'].setdefault('cart', []).append(cart_item)

            # Save the updated user data
            self.save_user_data()

            print(f"\n'{product['name']}' added to your cart successfully!")
        else:
            print("Invalid quantity. Please enter a valid quantity.")


    def checkout_cart(self, user_info, cart):
        if not cart:
            print("Your cart is empty.")
            return

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_amount = 0
        self.clear_console()
        print("\n*** Cart Items ***")
        for idx, item in enumerate(cart, 1):
            print(f"\n{idx}. Product Name: {item['Product Name']}\n   Quantity: {item['Quantity']}\n   Price per unit: {item['Price per unit']}$\n   Total Amount: {item['Quantity'] * item['Price per unit']}$")
            total_amount += item['Quantity'] * item['Price per unit']

        print(f"\nTotal Amount for Cart: {total_amount}$")

        # Ask user to confirm the purchase
        choice = input("\nDo you want to complete the purchase? (yes/no): ").lower()
        
        if choice == "yes":
            print(f"\nPlease Check Your Details.")
            self.view_account_info(user_info)
            choice2 = input("\nDo You Want To Change It? (yes/no)  : ").lower()
            if choice2 == "yes":
                self.account_settings(user_info)
                for item in cart:
                    purchase_item = {
                        'product_name': item['Product Name'],
                        'quantity': item['Quantity'],
                        'price_per_unit': item['Price per unit'],
                        'total_amount': item['Quantity'] * item['Price per unit'],
                        'date': current_date
                    }
                    user_info['user']['purchase_history'].append(purchase_item)
                    

                print("\nPurchase Successful! Thank you for shopping with us.")

                # Remove purchased items from the cart
                user_info['user']['cart'] = []

                # Save the updated user data
                self.save_user_data()

            elif choice2 == "no":
            # Add items to purchase history
                for item in cart:
                    purchase_item = {
                        'product_name': item['Product Name'],
                        'quantity': item['Quantity'],
                        'price_per_unit': item['Price per unit'],
                        'total_amount': item['Quantity'] * item['Price per unit'],
                        'date': current_date
                    }
                    user_info['user']['purchase_history'].append(purchase_item)

                    # Subtract the bought quantity from the available quantity in the product data
                    for product_data in self.product_data:
                        if product_data['product']['name'] == item['Product Name']:
                            product_data['product']['quantity'] = str(int(product_data['product']['quantity']) - item['Quantity'])

                print("\nPurchase Successful! Thank you for shopping with us.")

                # Remove purchased items from the cart
                user_info['user']['cart'] = []

                # Save the updated user data
                self.save_user_data()

        else:
            print("\nPurchase canceled. Returning to the shop menu.")


    def show_cart(self, user_info):
        cart = user_info['user'].get('cart', [])

        if not cart:
            print("Your cart is empty.")
            return

        selected_cart = []
        print("\n*** Cart Items ***")
        for idx, item in enumerate(cart, 1):
            print(f"\n{idx}. Product Name: {item['Product Name']}\n   Quantity: {item['Quantity']}\n   Price per unit: {item['Price per unit']}$")

            selected_cart.append(item)

        choice = input("\nEnter the numbers of the products you want to buy separated by commas (e.g., 1, 2): ")
        

        selected_indices = [int(idx) - 1 for idx in choice.split(',') if idx.strip()]

        if not selected_indices:
            print("Invalid input. Please enter valid numbers.")
            return

        selected_products = [selected_cart[idx] for idx in selected_indices]

        self.checkout_cart(user_info, selected_products)

        # Remove the purchased items from the cart
        user_info['user']['cart'] = [item for i, item in enumerate(cart) if i not in selected_indices]


    def show_purchase_history(self, user_info):
        self.clear_console()
        purchase_history = user_info['user'].get('purchase_history', [])

        if not purchase_history:
            print("************************************")
            print("        Purchase History")
            print("************************************\n")

            print("No purchase history to display.\n")
            return

        print("************************************")
        print("        Purchase History")
        print("************************************\n")

        for item in purchase_history:
            print(f"\nProduct Name: {item.get('product_name')}\nQuantity: {item.get('quantity')}\nPrice per unit: {item.get('price_per_unit')}$\nTotal Amount: {item.get('total_amount')}$\nDate: {item.get('date')}")


    def cancel_order(self, user_info):
        self.clear_console()
        print("**************************************************")
        print("              Order Cancellation")
        print("**************************************************\n")

        # Display user's purchase history for reference
        self.show_purchase_history(user_info)

        order_to_cancel = input("\nEnter the Product Name You Want to Cancel the Order For: ")

        # Check if the product exists in the purchase history
        purchase_history = user_info['user'].get('purchase_history', [])
        order_to_cancel_index = None

        for idx, order in enumerate(purchase_history):
            if order.get('product_name') == order_to_cancel:
                order_to_cancel_index = idx
                break

        if order_to_cancel_index is not None:
            # Get the details of the order to be canceled
            order_to_cancel_details = purchase_history[order_to_cancel_index]

            # Increase the product quantity in the product data
            for product_data in self.product_data:
                if product_data['product']['name'] == order_to_cancel_details['product_name']:
                    product_data['product']['quantity'] = str(int(product_data['product']['quantity']) + order_to_cancel_details['quantity'])

            # Remove the canceled order from purchase history
            user_info['user']['purchase_history'].pop(order_to_cancel_index)

            # Remove the canceled order from seller's order history
            for entry in self.user_data:
                if 'seller' in entry:
                    seller_data = entry['seller']
                    if 'order_history' in seller_data:
                        for order in seller_data['order_history']:
                            if order.get('product_name') == order_to_cancel_details['product_name']:
                                seller_data['order_history'].remove(order)
                                break

            print(f"\nOrder for '{order_to_cancel}' has been canceled successfully.")
            self.save_user_data()
            self.save_product_data()

        else:
            print(f"\nNo order found for product '{order_to_cancel}' in your purchase history.")
        
        input("\nPress Enter to go back to the user menu.")
        self.user_menu(user_info)



    def shop(self, user_info):
        selected_products = []
        selected_products_seller = []

        while True:
            self.clear_console()

            print("**************************************************")
            print("         Welcome To Digital Dynasty.")
            print("**************************************************")

            for idx, product_dict in enumerate(self.product_data):
                print(f" {idx + 1}.\n Name: {product_dict['product'].get('name')}\n Price: {product_dict['product'].get('price')}$\n Quantity: {product_dict['product'].get('quantity')}\n Description: {product_dict['product'].get('description')}\n")

            choice = input("\nEnter the numbers of the products you want to buy separated by commas (e.g., 1, 2), 'cart' to view your cart, or 'exit' to go to the user menu: ")

            if choice.lower() == "exit":
                self.user_menu(user_info)
            elif choice.lower() == "cart":
                self.show_cart(user_info)
                input("\nPress Enter to Continue Shopping.")
            else:
                try:
                    product_indices = [int(idx) - 1 for idx in choice.split(',')]
                    selected_products = [self.product_data[idx]['product'] for idx in product_indices]
                    selected_products_seller = [self.product_data[idx]['seller_name'] for idx in product_indices]

                    # Displaying selected products
                    for product in selected_products:
                        print(f"\nSelected Product:\n")
                        print(f"Name: {product.get('name')}\nPrice: {product.get('price')}$\nQuantity: {product.get('quantity')}\nDescription: {product.get('description')}\n")

                    action = input("\nChoose an action:\n\n1. Buy Now\n2. Add to Cart\n3. Cancel\n4. Go back to the Main Menu\n\nEnter your choice (1, 2, or 3): ")

                    if action == "1":
                        for product in selected_products:
                            quantity = self.get_valid_quantity(product)
                            self.buy_product(user_info, product, quantity,selected_products_seller)
                        input("\nPress Enter to Continue Shopping.")
                    elif action == "2":
                        for product in selected_products:
                            self.add_to_cart(user_info, product)
                        input("\nPress Enter to Continue Shopping.")
                    elif action == "3":
                        self.shop(user_info)
                    elif action == "4":
                        self.user_menu(user_info)
                    else:
                        print("Invalid Choice. Please Enter 1, 2, or 3.")
                except (ValueError, IndexError):
                    print("Invalid Input. Please Enter Valid Numbers.")



    def get_valid_quantity(self, selected_product):
        try:
            name = str(selected_product.get('name'))
            quantity = int(input(f"\nEnter the Number of Units You Want To Buy of {name}: "))
            available_quantity = int(selected_product.get('quantity'))

            if 1 <= quantity <= available_quantity:
                return quantity
            else:
                print(f"Invalid quantity. Please enter a valid number of units (1-{available_quantity}).")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


class Seller():

    def view_order_history(self, seller_info):
        self.clear_console()
        print("************************************")
        print("        Order History")
        print("************************************\n")

        if 'seller' in seller_info and 'order_history' in seller_info['seller']:
            order_history = seller_info['seller']['order_history']

            if not order_history:
                print("No order history to display.")
            else:
                for order in order_history:
                    print(f"\nProduct Name: {order.get('product_name')}")
                    print(f"Quantity: {order.get('quantity')}")
                    print(f"Price per unit: {order.get('price_per_unit')}$")
                    print(f"Total Amount: {order.get('total_amount')}$")
                    print(f"Date: {order.get('date')}")
                    print("\n------------------------------------")
        else:
            print("No order history to display.")

        input("\nPress Enter to go back to the user menu.")


    def account_settings(self, info):

        email = input("Enter Your Email: ")
        password = input("Enter Your Password: ")

        if user_type == "1":
            print("**************************************************")
            print("            User Account Settings")
            print("**************************************************")

            if email == info['user']['email'] and password == info['user']['password']:
                print("\n1. View Account Information\n2. Change Name\n3. Change Password\n4. Change Address\n5. Change Phone Number\n6. Change Security Questions\n7. Back to User Menu")
                choice = input("Enter Your Choice (1, 2, 3, 4, 5, 6, or 7): ")

                if choice == "1":
                    self.clear_console()
                    self.view_account_info(info)
                elif choice == "2":
                    self.change_name(info)
                elif choice == "3":
                    self.change_password(info)
                elif choice == "4":
                    self.change_address(info)
                elif choice == "5":
                    self.change_phone_number
                elif choice == "6":
                    self.change_security_questions(info)
                elif choice == "7":
                    pass
                else:
                    print("Invalid Choice. Please Enter 1, 2, 3, 4, 5, 6 or 7.")
            else:
                print("\nIncorrect Email or Password. Access Denied.")
            input("\nPress Enter to Logout.")
            
        elif user_type == "2":
            print("**************************************************")
            print("            Seller Account Settings")
            print("**************************************************")

            if email == info['seller']['email'] and password == info['seller']['password']:
                print("\n1. View Account Information\n2. Change Name\n3. Change Password\n4. Change Address\n5. Change Phone Number\n6. Change Security Questions\n7. Back to User Menu")
                choice = input("Enter Your Choice (1, 2, 3, 4, 5, 6, or 7): ")

                if choice == "1":
                    self.clear_console()
                    self.view_account_info(info)
                elif choice == "2":
                    self.change_name(info)
                elif choice == "3":
                    self.change_password(info)
                elif choice == "4":
                    self.change_address(info)
                elif choice == "5":
                    self.change_phone_number
                elif choice == "6":
                    self.change_security_questions(info)
                elif choice == "7":
                    pass
                else:
                    print("Invalid Choice. Please Enter 1, 2, 3, 4, 5, 6 or 7.")
            else:
                print("\nIncorrect Email or Password. Access Denied.")
            input("\nPress Enter to Logout.")

    def view_account_info(self, info):
        

        if user_type == "1":
            print("**************************************************")
            print("           User Account Information")
            print("**************************************************")

            print(f"\nEmail: {info['user']['email']}")
            print(f"Name: {info['user']['name']}")
            print(f"Address: {info['user']['address']}")
            print(f"Phone Number: {info['user']['phone_number']}")
            input("\nPress Enter to Continue.")

        elif user_type == "2":
            print("**************************************************")
            print("           Seller Account Information")
            print("**************************************************")

            print(f"\nEmail: {info['seller']['email']}")
            print(f"Name: {info['seller']['name']}")
            print(f"Address: {info['seller']['address']}")
            print(f"Phone Number: {info['seller']['phone_number']}")
            input("\nPress Enter to Continue.")

    def change_name(self, info):
        self.clear_console()

        if user_type == "1":
            print("**************************************************")
            print("             Change User Name")
            print("**************************************************")

            new_name = input("Enter New Name: ")
            if new_name:
                info['user']['name'] = new_name
                print("\nName Changed Successfully!")
            else:
                print("Invalid Name. Name not changed.")

            input("\nPress Enter to Return to User Menu.")

        elif user_type == "2":
            print("**************************************************")
            print("             Change Seller Name")
            print("**************************************************")

            new_name = input("Enter New Name: ")
            if new_name:
                info['seller']['name'] = new_name
                print("\nName Changed Successfully!")
            else:
                print("Invalid Name. Name not changed.")

            input("\nPress Enter to Return to Seller Menu.")


    def change_password(self, info):
        self.clear_console()

        if user_type == "1":
            print("**************************************************")
            print("            Change User Password")
            print("**************************************************")

            current_password = input("Enter Current Password: ")

            if current_password == info['user']['password']:
                new_password = input("Enter New Password: ")
                info['user']['password'] = new_password
                print("\nPassword Changed Successfully!")
            else:
                print("\nIncorrect Current Password. Password not Changed.")

            input("\nPress Enter to Return to User Menu.")

        elif user_type == "2":
            print("**************************************************")
            print("            Change Seller Password")
            print("**************************************************")

            current_password = input("Enter Current Password: ")

            if current_password == info['seller']['password']:
                new_password = input("Enter New Password: ")
                info['seller']['password'] = new_password
                print("\nPassword Changed Successfully!")
            else:
                print("\nIncorrect Current Password. Password not Changed.")

            input("\nPress Enter to Return to Seller Menu.")


    def change_address(self, info):
        self.clear_console()

        if user_type == "1":
            print("**************************************************")
            print("            Change User Address")
            print("**************************************************")

            new_address = input("Enter New Address: ")
            if new_address:
                info['user']['address'] = new_address
                print("\nAddress Changed Successfully!")
            else:
                print("Invalid Address. Address not changed.")

            input("\nPress Enter to Return to User Menu.")

        elif user_type == "2":
            print("**************************************************")
            print("            Change Seller Address")
            print("**************************************************")

            new_address = input("Enter New Address: ")
            if new_address:
                info['seller']['address'] = new_address
                print("\nAddress Changed Successfully!")
            else:
                print("Invalid Address. Address not changed.")

            input("\nPress Enter to Return to Seller Menu.")



    def change_phone_number(self, info):
        self.clear_console()

        if user_type == "1":
            print("**************************************************")
            print("             Change User Phone Number")
            print("**************************************************")

            new_number = input("Enter New Phone Number: ")
            if new_number:
                info['user']['phone_number'] = new_number
                print("\Phone Number Changed Successfully!")
            else:
                print("Invalid Phone Number. Phone Number not changed.")

            input("\nPress Enter to Return to User Menu.")

        elif user_type == "2":
            print("**************************************************")
            print("             Change Seller Phone Number")
            print("**************************************************")

            new_number = input("Enter New Phone Number: ")

            if new_number:
                info['seller']['phone_number'] = new_number
                print("\nPhone Number Changed Successfully!")
            else:
                print("Invalid Phone Number. Phone Number not changed.")

            input("\nPress Enter to Return to Seller Menu.")



    def change_security_questions(self, info):
        self.clear_console()

        if user_type == "1":
            print("**************************************************")
            print("        Change User Security Questions")
            print("**************************************************")

            new_question1 = input("Enter New Security Question 1: ")
            new_question2 = input("Enter New Security Question 2: ")

            if new_question1 and new_question2:
                info['user']['security_questions_answers']['question1'] = new_question1
                info['user']['security_questions_answers']['question2'] = new_question2

                print("\nSecurity Questions Changed Successfully!")
            else:
                print("Invalid Security Questions. Security Questions not changed.")

            input("\nPress Enter to Return to User Menu.")
        
        elif user_type == "2":
            print("**************************************************")
            print("        Change Seller Security Questions")
            print("**************************************************")

            new_question1 = input("Enter New Security Question 1: ")
            new_question2 = input("Enter New Security Question 2: ")

            if new_question1 and new_question2:
                info['seller']['security_questions_answers']['question1'] = new_question1
                info['seller']['security_questions_answers']['question2'] = new_question2
                print("\nSecurity Questions Changed Successfully!")
            else:
                print("Invalid Security Questions. Security Questions not changed.")

            input("\nPress Enter to Return to Seller Menu.")




class Menu(Product, User, Seller):

    def seller_menu(self, seller_info):
        while True:
            self.clear_console()

            print("**************************************************")
            print(f"         Welcome {seller_info['seller']['store_name']} .")
            print("**************************************************")
            print("\n1. Add a Product\n2. Remove a Product\n3. Edit Products\n4. View My Products\n5. View Order History\n6. Account Settings\n7. Delete Your Account\n8. Logout")
            
            choice = input("Enter Your Choice (1, 2, 3, 4, 5, or 6): ")

            if choice == "1":
                self.add_product(seller_info)
            elif choice == "2":
                self.remove_product(seller_info)
            elif choice == "3":
                self.edit_products(seller_info)
            elif choice == "4":
                self.view_my_products(seller_info)
            elif choice == "5":
                print(seller_info)
                self.view_order_history(seller_info)
            elif choice == "6":
                self.clear_console()
                self.account_settings(seller_info)
            elif choice == "7":
                self.delete_seller_account()
            elif choice == "8":
                AuthenticationSystem().start()
            else:
                print("Invalid Choice. Please Enter 1, 2, 3, 4, 5, or 6.")


    def user_menu(self, user_info):
        while True:
            self.clear_console()

            print("**************************************************")
            print(f"         Welcome {user_info['user']['name']} .")
            print("**************************************************")
            print("\n1. Shop\n2. Cancel Order\n3. Account Settings\n4. View Purchase History\n5. Delete Your Account \n6. Logout")
            choice = input("Enter Your Choice (1, 2, 3, or 4): ")

            if choice == "1":
                self.shop(user_info)
            elif choice == "2":
                self.cancel_order(user_info)
            elif choice == "3":
                self.account_settings(user_info)
            elif choice == "4":
                self.show_purchase_history(user_info)
                input("Press Enter to continue.")
            elif choice == "5":
                self.delete_user_account()
            elif choice == "6":
                AuthenticationSystem().start()
            else:
                print("Invalid Choice. Please Enter 1, 2, 3, or 4.")




class AuthenticationSystem(Menu):

    def __init__(self):

        self.USER_DATA_PATH = "C:\\Users\\92321\\OneDrive\\Desktop\\Project\\User_Data.txt"
        self.PRODUCTS_PATH = "C:\\Users\\92321\\OneDrive\\Desktop\\Project\\Products.txt"

        self.user_data = self.load_user_data()
        self.product_data = self.load_product_data()

        self.clear_console()

    def clear_console(self):
        os.system('cls')


    def load_user_data(self):
        try:
            with open(self.USER_DATA_PATH, "r") as file:
                data = file.read()
                if data:
                    return eval(data)
                return []
        except (SyntaxError, FileNotFoundError):
            print(f"Error loading user data")
            return []


    def load_product_data(self):
        try:
            with open(self.PRODUCTS_PATH, "r") as file:
                data = file.read()
                if data:
                    return eval(data)
                return []
        except (SyntaxError, FileNotFoundError):
            print(f"Error loading product data")
            return []


    def save_user_data(self):
        with open(self.USER_DATA_PATH, "w") as file:
            file.write(str(self.user_data))


    def save_product_data(self):
        with open(self.PRODUCTS_PATH, "w") as file:
            file.write(str(self.product_data))


    def login(self):
        global user_type

        self.clear_console()
        print("\n************************************************************")
        print(f"              Welcome! Enter Login Information: ")
        print("************************************************************\n")
        email = input("Enter Your Email: ")
        print()
        password = input("Enter Your Password: ")
        print()
        user_type = input("Are You a [1] User or [2] Seller? Enter 1 or 2: ")

        if user_type == "1":
            for user_info in self.user_data:
                user = user_info.get("user", {})
                if user.get("email") == email and user.get("password") == password:
                    self.clear_console()

                    print("************************************************************")
                    print(f"                Welcome, {user['name']}!")
                    print("************************************************************")

                    return user_info
                self.clear_console()
            print("The Email or Password is Not Correct\n")
            return None
        elif user_type == "2":
            for seller_info in self.user_data:
                seller = seller_info.get("seller", {})
                if seller.get("email") == email and seller.get("password") == password:
                    self.clear_console()
                    return seller_info
            self.clear_console()    
            print("The Email or Password is Not Correct\n")
            return None
        else:
            self.clear_console()
            print("Invalid Choice. Please Enter 1 or 2.\n")
            return None


    def guest_login(self):
        self.clear_console()

        total_products = len(self.product_data)

        if total_products == 0:
            print("\nNo products to display.")
            return

        print("*****************************************************************************")
        print("                 Guest Login Successful! (Limited Access!)")
        print("*****************************************************************************")

        for idx, product_data in enumerate(self.product_data, start=1):
            product_dict = product_data['product']
            print(f" {idx}.\n Name: {product_dict.get('name')}\n Price: {product_dict.get('price')}$\n Quantity: {product_dict.get('quantity')}\n Description: {product_dict.get('description')}\n")

        input("\nIf You Want To Buy Something You Have To Make an Account First.\n\nPress Enter To Return To The Main Menu.")
        self.clear_console()

    def checking(self, phone_number, user_type):
        for user in self.user_data:
            if user_type in user and user[user_type]['phone_number'] == phone_number:
                return True
        return False

    def register_seller(self):
        self.clear_console()

        print("*******************************************************************")
        print("              Welcome! Register as a Seller Information:")
        print("*******************************************************************")

        email = input("Email: ")
        password = input("Password: ")
        number = input("Phone Number: ")
        store_name = input("Name of the Store: ")
        address = input("Address: ")

        # Check if the store name or phone number is already taken by another seller
        if any(seller['seller']['store_name'].lower() == store_name.lower() for seller in self.user_data if 'seller' in seller):
            print("Store name is already taken by another seller. Please choose a different one.")
            return

        if self.checking(number, 'seller'):
            print("Phone number is already taken by another seller. Please choose a different one.")
            return


        print("Now Please Answer Some Security Questions")
        question1 = input("Best Friend's Name: ")
        question2 = input("City of Birth: ")

        new_seller = {
            "seller": {
                "email": email,
                "password": password,
                "phone_number": number,
                "store_name": store_name,
                "address": address,
                "security_questions_answers": {
                    "question1": question1,
                    "question2": question2,
                "order_history": []
                }
            }
        }

        if not all([email, password, store_name, address, number, question1, question2]):
            print("One of the Given Field is Empty. Please Ensure to Fill All of Them.")
        else:
            self.user_data.append(new_seller)
            self.save_user_data()
            self.clear_console()

            print("************************************************************************************************")
            print("         Congratulations! Your Seller Account Has Been Created. You Can Now Log In.")
            print("************************************************************************************************")

    def sign_up(self):
        self.clear_console()

        print("*******************************************************************")
        print("               Welcome! Enter Sign Up Information:")
        print("*******************************************************************")

        email = input("Email: ")
        password = input("Password: ")
        name = input("Name: ")
        age = input("Age: ")
        address = input("Address: ")
        number = input("Phone Number: ")

        # Check if the name and phone number is already taken by another user
        if any(user['user']['name'].lower() == name.lower() for user in self.user_data if 'user' in user):
            print("Name is already taken by another user. Please choose a different one.")
            return
        
        if self.checking(number, 'user'):
            print("Phone number is already taken by another user. Please choose a different one.")
            return


        print("Now Please Answer Some Security Questions")
        question1 = input("Best Friend's Name: ")
        question2 = input("City of Birth: ")

        new_user = {
            "user": {
                "email": email,
                "password": password,
                "name": name,
                "age": age,
                "address": address,
                "phone_number": number,
                "security_questions_answers": {
                    "question1": question1,
                    "question2": question2
                },
                "purchase_history": [],
                "cart": []
            }
        }

        if not all([email, password, name, age, address, number, question1, question2]):
            print("One of the Given Fields is Empty. Please Ensure to Fill All of Them.")
        else:
            self.user_data.append(new_user)
            self.save_user_data()
            self.clear_console()

            print("************************************************************************************************")
            print("         Congratulations! Your Account Has Been Created. You Can Now Log In.")
            print("************************************************************************************************")



    def delete_user_account(self):
        self.clear_console()

        print("*******************************************************************")
        print("                 Delete User Account Information:")
        print("*******************************************************************")

        email = input("Enter Your Email: ")
        print()
        password = input("Enter Your Password: ")
        print()

        found_user = None
        for user_info in self.user_data:
            user = user_info.get("user", {})
            if user.get("email") == email and user.get("password") == password:
                found_user = user_info
                break

        if found_user:
            confirm_delete = input("Are you sure you want to delete your account? (yes/no): ").lower()
            if confirm_delete == "yes":
                self.user_data.remove(found_user)
                self.save_user_data()
                self.clear_console()
                print("************************************************************************************************")
                print("                Your Account Has Been Deleted Successfully.")
                print("************************************************************************************************")
                input("\nPress Enter To Go To The Main Menu")
                AuthenticationSystem().start()
            else:
                print("Account deletion canceled.")
        else:
            print("User not found.")


    def delete_seller_account(self):
        self.clear_console()

        print("*******************************************************************")
        print("               Delete Seller Account Information:")
        print("*******************************************************************")

        email = input("Enter Your Email: ")
        print()
        password = input("Enter Your Password: ")
        print()

        found_seller = None
        for seller_info in self.user_data:
            seller = seller_info.get("seller", {})
            if seller.get("email") == email and seller.get("password") == password:
                found_seller = seller_info
                break

        if found_seller:
            confirm_delete = input("Are You Sure You Want To Delete Your Account? All Your Products Will Also be Removed. (yes/no): ").lower()
            if confirm_delete == "yes":
                # Remove seller's account
                self.user_data.remove(found_seller)

                # Remove seller's products from products_data
                seller_name = seller.get("store_name")
                self.remove_seller_products(seller_name)

                # Save updated user_data and products_data
                self.save_user_data()
                self.save_product_data()

                self.clear_console()
                print("************************************************************************************************")
                print("                Your Seller Account Has Been Deleted Successfully.")
                print("************************************************************************************************")
                input("\nPress Enter To Go To The Main Menu")

                AuthenticationSystem().start()
            else:
                print("Account deletion canceled.")
        else:
            print("Seller not found.")

    def remove_seller_products(self, seller_name):

        products_data = self.load_product_data()

        # Removing all products listed by the Seller from products_data
        updated_products_data = [product for product in products_data if product.get("seller_name") != seller_name]

        # Saving updated products_data
        with open(self.PRODUCTS_PATH, "w") as file:
            file.write(str(updated_products_data))

        self.products_data = updated_products_data


    def forgot_password(self):
        self.clear_console()

        print("**************************************************")
        print("              Forgot Password")
        print("**************************************************")
        user_type = input("\nAre You a [1] User or [2] Seller? Enter 1 or 2: ")

        if user_type == "1":
            self.forgot_password_user()
        elif user_type == "2":
            self.forgot_password_seller()
        else:
            self.clear_console()
            print("Invalid Choice. Please Enter 1 or 2.\n")
        
        input("Press Enter to Return to the Main Menu.")
        self.clear_console()


    def forgot_password_user(self):
        email = input("\nEnter Your Email: ")

        user_info = None
        for info in self.user_data:
            user_email = info.get("user", {}).get("email", "").lower()

            if user_email == email.lower():
                user_info = info
                break
        if user_info:
            security_questions = user_info["user"]["security_questions_answers"]
            print("\nAnswer the Security Questions to Reset Your Password:\n")

            answer1 = input(f"Q1: What is Your Best Friend's Name? ")
            answer2 = input(f"\nQ2: In Which City Were You Born? ")

            if answer1 == security_questions["question1"] and answer2 == security_questions["question2"]:
                new_password = input("\nEnter Your New Password: ")
                user_info["user"]["password"] = new_password

                self.save_user_data()
                self.clear_console()

                print("\n\nPassword Reset Successful! You Can Now Log In With Your New Password.")
            else:
                
                print("\n\nIncorrect Answers to Security Questions. Password Reset Failed.")
        else:
            print("\nEmail not Found. Please Make Sure You Entered the Correct Email Address.")


    def forgot_password_seller(self):
        email = input("Enter Your Email: ")

        seller_info = None
        for info in self.user_data:
            seller_email = info.get("seller", {}).get("email", "").lower()

            if seller_email == email.lower():
                seller_info = info
                break

        if seller_info:
            security_questions = seller_info["seller"]["security_questions_answers"]
            print("\nAnswer the Security Questions to Reset Your Password:\n")

            answer1 = input(f"\nQ1: What is Your Best Friend's Name? ")
            answer2 = input(f"\nQ2: In Which City Were You Born? ")

            if answer1 == security_questions["question1"] and answer2 == security_questions["question2"]:
                new_password = input("\nEnter Your New Password: ")
                seller_info["seller"]["password"] = new_password
                self.save_user_data()

                print("\n\nPassword Reset Successful! You Can Now Log In With Your New Password.")
                self.clear_console()
            else:
                print("Incorrect Answers to Security Questions. Password Reset Failed.")
        else:
            print("Email Not Found. Please Make Sure You Entered the Correct Email Address.")



    def start(self):
        while True:
            print("**************************************************")
            print("         Welcome To Digital Dynasty.")
            print("**************************************************")

            print("\n1. Login\n2. Guest Login\n3. Sign Up\n4. Register as a Seller\n5. Help\n6. Forget Password\n7. Quit")
            print()
            choice = input("Enter your choice (1, 2, 3, 4, 5, 6, or 7): ")
            print()

            if choice == "1":
                user_info = self.login()
                if user_info:
                    if "user" in user_info and "name" in user_info["user"]:
                        self.user_menu(user_info)
                    elif "seller" in user_info and "store_name" in user_info["seller"]:
                        self.seller_menu(user_info)

            elif choice == "2":
                self.guest_login()

            elif choice == "3":
                self.sign_up()

            elif choice == "4":
                self.register_seller()

            elif choice == "5":
                self.clear_console()
                print("************************************************************")
                print(f"                  Welcome To Digital Dynasty Customer Support Center.")
                print("************************************************************")
                print(f"\n\nWe are So Sorry, The Live Support is not Working Right Now As We are in Developing Stage.\nYou Can Drop a Email To the Below Email Address, Our Team Will Resolve Your Issue Within\n24 Hours or They Will Contact You As Soon As Possible.")
                print(f"\n\n             ****************************************************")
                print(f"                 Email: customersupport@digitaldynasty.com.pk ")
                print(f"             ****************************************************\n\n")
                print("*********************")
                print(f"     Exit Menu")
                print("*********************")
                print("\n1.Continue\n2.Exit")
                print()
                enter = input("Enter Your Choice (1 or 2): ")

                if enter == "1":
                    self.clear_console()
                    continue
                elif enter == "2":
                    print(f"\nThank You for Visiting Digital Dynasty")
                    break

            elif choice == "6":
                self.forgot_password()

            elif choice == "7":
                print("*********************")
                print(f"     Exit Menu")
                print("*********************")
                print("\n1.Continue\n2.Exit")
                print()
                enter = input("Enter Your Choice (1 or 2): ")
                if enter == "1":
                    self.clear_console()
                    continue
                elif enter == "2":
                    print(f"\nThank You for Visiting Digital Dynasty")
                    break

            else:
                self.clear_console()
                print("Invalid Choice. Please Enter 1, 2, 3, 4, 5, 6, or 7.\n\n")

AuthenticationSystem().start()
