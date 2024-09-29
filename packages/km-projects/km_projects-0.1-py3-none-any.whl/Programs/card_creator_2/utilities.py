try:
    import time
    import sys
    import os
    import random
    import logging

    def CARDNUM():
        rannumbers=[random.choice(range(100)) for _ in range(6)]
        return ''.join(map(str, rannumbers))
    cardnum=CARDNUM()

    def CARDCVV():
        rannumbers=[random.choice(range(4)) for _ in range(4)]
        return ''.join(map(str, rannumbers))
    cardcvv=CARDCVV()

    def Mastercard():
        os.system("cls")
        print("="*20)
        print("MASTERCARD\n")
        print("Please wait...")
        time.sleep(3)
        rerun1=True
        while rerun1:
            try:
                print("="*22)
                print("Enter cardHolder Name")
                cardname=str(input("")).capitalize()
                print("\nEnter the expiry date (Month/Day/Year)")
                cardexpiry=str(input(""))
                if(cardexpiry.__contains__("/")):
                    print("\nEnter the name of the bank that issued the card.")
                    bank=str(input("")).capitalize()
                    print("="*22)
                    print("\ncreating your card.....")
                    time.sleep(4)
                    os.system("cls")
                    print("="*20)
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User created Mastercard.")
                    print("🎉Your Card was created!🎉".upper())
                    print("")
                    print("-----------------------------------------------------")
                    print(f"| BANK NAME : {bank}                                ")
                    print(f"|                                                   ")
                    print(f"| {cardname}                                        ")
                    print(f"|                               MASTERCARD          ")
                    print(f"| {cardnum}                                         ")                        
                    print(f"|                                                   ")
                    print(f"| Expiry Date : {cardexpiry}    CVV : {cardcvv}     ")
                    print("-----------------------------------------------------")
                    print("")
                    sys.exit()
                else:
                    print("\nInvalid Expiry Date.\nTry again")
                    time.sleep(2)
                    os.system("cls")
                    rerun1
            except Exception:
                print("Input is required!")
                time.sleep(1)
                os.system("cls")
                rerun1    

    def VISA():
        os.system("cls")
        print("="*20)
        print("VISA\n")
        print("Please wait...")
        time.sleep(3)
        rerun2=True
        while rerun2:
            try:
                print("="*22)
                print("Enter cardHolder Name")
                cardname=str(input("")).capitalize()
                print("\nEnter the expiry date")
                cardexpiry=str(input(""))
                if(cardexpiry.__contains__("/")):
                    print("\nEnter the name of the bank that issued the card.")
                    issingbank=str(input("")).capitalize()
                    print("="*22)
                    print("\ncreating your card.....")
                    time.sleep(4)
                    os.system("cls")
                    print("="*20)
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User created VISA card.")
                    print("🎉Your Card was created!🎉".upper())
                    print("")
                    print("---------------------------------------------------")
                    print(f"| BANK NAME : {issingbank}                        ")
                    print(f"|                                                 ")
                    print(f"| {cardname}                                      ")
                    print(f"|                         VISA CARD               ")
                    print(f"| {cardnum}                                       ")                        
                    print(f"|                                                 ")
                    print(f"| Expiry Date : {cardexpiry}    CVV : {cardcvv}   ")
                    print("---------------------------------------------------")
                    print("")
                    sys.exit()
                else:
                    print("\nInvalid ExpiryDate.\nTry again")
                    time.sleep(2)
                    os.system("cls")
                    rerun2
            except Exception:
                print("Input is required!")
                time.sleep(1)
                os.system("cls")
                rerun2

    def virtual():
        os.system("cls")
        print("="*20)
        print("VIRTUAL\n")
        print("Please wait...")
        time.sleep(3)
        rerun3=True
        while rerun3:
            try:
                print("="*22)
                print("Enter cardHolder Name")
                cardname=str(input("")).capitalize()
                print("\nEnter the expiry date")
                cardexpiry=str(input(""))
                if(cardexpiry.__contains__("/")):
                    print("\nEnter card type")
                    issingbank=str(input("")).capitalize()
                    print("="*22)
                    print("\ncreating your card.....")
                    time.sleep(4)
                    os.system("cls")
                    print("="*20)
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User created Virtual card")
                    print("🎉Your Card was created!🎉".upper())
                    print("\n-------------------------------------------------")
                    print(f"| BANK NAME : {issingbank}                        ")
                    print(f"|                                                 ")
                    print(f"| {cardname}                                      ")
                    print(f"|                        VIRTUAL CARD             ")
                    print(f"| {cardnum}                                       ")                        
                    print(f"|                                                 ")
                    print(f"| Expiry Date : {cardexpiry}    CVV : {cardcvv}   ")
                    print("-------------------------------------------------\n")
                    sys.exit()
                else:
                    print("\nInvalid ExpiryDate\nTry again")
                    time.sleep(2)
                    os.system("cls")
                    rerun3
            except Exception:
                print("Input is required!")
                time.sleep(1)
                os.system("cls")
                rerun3

    def B_Mastercard():
        os.system("cls")
        print("="*20)
        print("BUSINESS MASTERCARD\n")
        print("Please wait...")
        time.sleep(3)
        rerun1=True
        while rerun1:
            try:
                print("="*22)
                print("Enter cardHolder Name")
                cardname=str(input("")).capitalize()
                print("\nEnter the expiry date")
                cardexpiry=str(input(""))
                if(cardexpiry.__contains__("/")):
                    print("\nEnter the name of the bank that issued the card.")
                    bank=str(input("")).capitalize()
                    print("Enter Business name")
                    businessname=str(input(""))
                    print("="*22)
                    print("\ncreating your card.....")
                    time.sleep(4)
                    os.system("cls")
                    print("="*20)
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User created business Mastercard")
                    print("🎉Your Card was created!🎉".upper())
                    print("")
                    print("-----------------------------------------------------")
                    print(f"| BANK NAME : {bank}                                ")
                    print(f"|                                                   ")
                    print(f"| {cardname}               BUSINESS MASTERCARD      ")
                    print(f"|                                                   ")
                    print(f"|                   Business Name : {businessname}  ")
                    print(f"| {cardnum}                                         ")                        
                    print(f"|                                                   ")
                    print(f"| Expiry Date : {cardexpiry}    CVV : {cardcvv}     ")
                    print("-----------------------------------------------------")
                    print("")
                    sys.exit()
                else:
                    print("\nInvalid ExpiryDate.\nTry again.")
                    time.sleep(2)
                    os.system("cls")
                    rerun1
            except Exception:
                print("Input is required!")
                time.sleep(1)
                os.system("cls")
                rerun1 
    def B_VISA():
        os.system("cls")
        print("="*20)
        print("BUSINESS VISA CARD\n")
        print("Please wait...")
        time.sleep(3)
        rerun2=True
        while rerun2:
            try:
                print("="*22)
                print("Enter cardHolder Name")
                cardname=str(input("")).capitalize()
                print("\nEnter the expiry date")
                cardexpiry=str(input(""))
                if(cardexpiry.__contains__("/")):
                    print("\nEnter the name of the bank that issued the card.")
                    bank=str(input("")).capitalize()
                    print("Enter Business name")
                    businessname=str(input(""))
                    print("="*22)
                    print("\ncreating your card.....")
                    time.sleep(4)
                    os.system("cls")
                    print("="*20)
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User created business VISA card")
                    print("🎉Your Card was created!🎉".upper())
                    print("")
                    print("-----------------------------------------------------")
                    print(f"| BANK NAME : {bank}                                ")
                    print(f"|                                                   ")
                    print(f"| {cardname}               BUSINESS VISA CARD       ")
                    print(f"|                                                   ")
                    print(f"|                   Business Name : {businessname}  ")
                    print(f"| {cardnum}                                         ")                        
                    print(f"|                                                   ")
                    print(f"| Expiry Date : {cardexpiry}    CVV : {cardcvv}     ")
                    print("-----------------------------------------------------")
                    print("")
                    sys.exit()
                else:
                    print("\nInvalid ExpiryDate.\nTry again")
                    time.sleep(2)
                    os.system("cls")
                    rerun2
            except Exception:
                print("Input is required!")
                time.sleep(1)
                os.system("cls")
                rerun2    
    def B_Virtual():
        os.system("cls")
        print("="*20)
        print("BUSINESS VIRTUAL CARD\n")
        print("Please wait...")
        time.sleep(3)
        rerun3=True
        while rerun3:
            try:
                print("="*22)
                print("Enter cardHolder Name")
                cardname=str(input("")).capitalize()
                print("\nEnter the expiry date")
                cardexpiry=str(input(""))
                if(cardexpiry.__contains__("/")):
                    print("\nEnter the name of the bank that issued the card.")
                    bank=str(input("")).capitalize()
                    print("Enter Business name")
                    businessname=str(input(""))
                    print("="*22)
                    print("\ncreating your card.....")
                    time.sleep(4)
                    os.system("cls")
                    print("="*20)
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User created business virtual card")
                    print("🎉Your Card was created!🎉".upper())
                    print("")
                    print("-----------------------------------------------------")
                    print(f"| BANK NAME : {bank}                                ")
                    print(f"|                                                   ")
                    print(f"| {cardname}               BUSINESS VIRTUAL CARD    ")
                    print(f"|                                                   ")
                    print(f"|                   Business Name : {businessname}  ")
                    print(f"| {cardnum}                                         ")                        
                    print(f"|                                                   ")
                    print(f"| Expiry Date : {cardexpiry}    CVV : {cardcvv}     ")
                    print("-----------------------------------------------------")
                    print("")
                    sys.exit()
                else:
                    print("\nInvalid ExpiryDate.\nTry again.")
                    time.sleep(2)
                    os.system("cls")
                    rerun3
            except Exception:
                print("Input is required!")
                time.sleep(1)
                os.system("cls")
                rerun3

except KeyboardInterrupt:
    os.system("cls")
    print("Error with the utilities file.")
    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
    logging.error("User interupted the program (in utilities)")
    exit()
except Exception:
    os.system("cls")
    print("Error with the utilities file.")
    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
    logging.warning("An Error occured in the utilities file.")
    exit()

