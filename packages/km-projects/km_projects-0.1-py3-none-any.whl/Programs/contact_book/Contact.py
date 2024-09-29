try:
    import json
    import os
    import time

    def Add_contact():
        os.system("cls")
        print("Enter Contact Name")
        contactname=input("> ")
        print(f"\nEnter {contactname}'s phone number")
        contactphone=int(input("> "))
        print(f"Enter {contactname}'s email")
        email=input("> ")
        print("Contact saved!")
        contactsfile=open('contact_book/contacts.json','a')
        contactlist=[]
        for i in range(1,6):
            contdata={
                "Name": contactname,
                "Phone":contactphone,
                "Email": email
            }
        contactlist.append(contdata)
        contactsfile.write(f"{json.dumps(contactlist, indent=4)},\n")
        if (contactphone <10):
            print("Contact Number should be up to 10 digits")
            time.sleep(2)
            Add_contact()

    def View_contact():
        os.system("cls")
        print("Your Contacts : \n\n")
        contactsfile=open('contact_book/contacts.json','r')
        print(contactsfile.read())
        print("\n\n=============================")
        print("1 : Add Contacts")
        print("2 : View Contacts")
        print("3 : Delete Contacts")
        print("4 : Exit")
        optioninput=int(input(">"))
        if(optioninput==1):
            Add_contact()
        elif(optioninput==2):
            View_contact()
        elif(optioninput==3):
            delete_contact()
        elif(optioninput==4):
            print("Program Exited.")
        else:
            print("Invalid option.")
        

    def delete_contact():
        os.system("cls")
        print("204 (No Content)")
        time.sleep(2)
        Main()
        # contactsfile=open('cont/contacts.json','r')
        # print(contactsfile.read())
        # print("\n==================================")
        # print("Enter contact details to delete")
        # for i in range(3):
        #     delinput=input("> ")
        #     if delinput in contactsfile:
        #         del contactsfile[delinput]
        #         print("Contact deleted!")
        # else:
        #     os.system("cls")
        #     print("Not Found")
        #     exit()

    def Main():
        os.system("cls")
        print("Contacts Book")
        print("\nSelect an option")
        print("1 : Add Contacts")
        print("2 : View Contacts")
        print("3 : Delete Contacts")
        print("4 : Exit")
        optioninput=int(input(">"))
        if(optioninput==1):
            Add_contact()
        elif(optioninput==2):
            View_contact()
        elif(optioninput==3):
            delete_contact()
        elif(optioninput==4):
            os.system("cls")
            print("Program Exited.")
        else:
            print("Invalid option.")
    Main()
except KeyboardInterrupt:
    os.system("cls")
    print("System Error.")
    exit()
except Exception:
    os.system("cls")
    print("Program failed.")
    exit()

