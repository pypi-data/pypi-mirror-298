import os
try:
    # please install 'emoji'.(pip install emoji)
    import emoji
    import os

    def Main():
        print("Emoji Convert to text\n\n")
        print("Enter Emoji to convert")
        emojiinput=input(">")
        print(f"\nEmoji >> {emojiinput}")
        print(f"Emoji text >> {emoji.demojize(emojiinput)}")
    Main()
except KeyboardInterrupt:
    os.system("cls")
    print("Couldn't convert emoji.")
    exit()
except Exception:
    os.system("cls")
    print("Couldn't convert emoji.")
    exit()