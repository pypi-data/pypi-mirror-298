import os
os.system("cls")
print("Programs Initializer")
print("Type help()")


def help():
    os.system("cls")
    print("Programs\n")
    print("TITLE | Calculator         | FUNCTION >   calcu()")
    print("TITLE | Emoji Converter    | FUNCTION >   cmoji_converter()")
    print("TITLE | Password Generator | FUNCTION >   passwordgenerator()")
    print("TITLE | Card Creator       | FUNCTION >   cardcreator()")
    print("TITLE | Contact Book       | FUNCTION >   contactbook()")
    print("TITLE | Word Guessing Game | FUNCTION >   wordguess()")
    print("")

def calcu():
    os.system("cls")
    print("Calculator Initialized!\n")
    from Calcualtor import Calcu
    Calcu()

def emoji_converter():
    os.system("cls")
    print("Emoji Converter Initialized!")
    print("Print install 'emoji'library\n")
    from Emoji_Converter import Main

def passwordgenerator():
    os.system("cls")
    print("Password Generator Initialized!\n")
    from Password_Generator import password_generator
    password_generator()

def cardcreator():
    os.system("cls")
    print("Card Creator Initialized!\n")
    from card_creator_2.card_creator import Main
    Main()

def contactbook():
    os.system("cls")
    print("Contact Book Initialized!\n")
    from contact_book.Contact import Main
    Main()

def wordguess():
    os.system("cls")
    print("Word Guess Initialized!\n")
    from Word_Guessing import MAIN_Word_Guessing
