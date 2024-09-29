try:
    import os
    import logging
    def Main():
        from utilities import Mastercard
        from utilities import VISA
        from utilities import virtual
        from utilities import B_Mastercard
        from utilities import B_VISA
        from utilities import B_Virtual
        os.system("cls")
        logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
        logging.info("User Started the program.")
        print("="*25)
        print("Welcome To Card Creator.\nversion=2")
        print("\nWho are you creating the card for?")
        print("1 : for Myself")
        print("2 : for Business")
        cht=int(input("> "))
        if(cht==1):
            logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
            logging.info("User selected option 1")
            for rerun2 in range(2):
                print("\nWhich type of card are you creating?")
                print("1 : Mastercard")
                print("2 : VISA")
                print("3 : virtual")
                cht1=int(input(""))
                if(cht1==1):
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User selected Mastercard")
                    Mastercard()
                elif(cht1==2):
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User selected VISA")
                    VISA()
                elif(cht1==3):
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User selected Virtual")
                    virtual()
                else:
                    print("\nInput required.")
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User entered invalid number.")
                    continue
        elif(cht==2):
            logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
            logging.info("User selected option 2")
            for rerun3 in range(2):
                print("\nWhich type of card are you creating?")
                print("1 : Mastercard")
                print("2 : VISA")
                print("3 : virtual")
                cht1=int(input(""))
                if(cht1==1):
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User selected Business Mastercard")
                    B_Mastercard()
                elif(cht1==2):
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User selected VISA")
                    B_VISA()
                elif(cht1==3):
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User selected virtual")
                    B_Virtual()
                else:
                    print("\n\nInput required.")
                    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
                    logging.info("User entered invalid option")
                    continue
        else:
            os.system("cls")
            print("Oops! Something went wrong.")
            logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
            logging.error("User entered invalid number.")
            exit()        
    Main()
except KeyboardInterrupt:
    os.system("cls")
    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
    logging.error("User interuppted the program.")
    print("Something went wrong. Check logs")
    exit()
except Exception:
    os.system("cls")
    print("Something went wrong. Check logs")
    logging.basicConfig(filename='card_creator_2/log.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%H:%M:%S')
    logging.error("An Error occured in the program.")
    exit()

if __name__=="__main__":
    Main()