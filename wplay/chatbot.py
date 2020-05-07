def Bot(last_Message):
    print('\n Bot activated')
    last_Message= "".join(last_Message.split())
    simple_menu = {                                 # function requires no extra arguments
                "hi": say_hi,
                "help": _help_commands,
                "goodmorning": say_goodmorning,
                "goodnight": say_goodnight,
                "howareyou?": say_fine,
            }
    simple_menu_keys = simple_menu.keys()
    command_args = last_Message[1:].split(" ", 1)
    print("Command args: {cmd}".format(cmd=command_args))
    if len(command_args) == 1 and command_args[0] in simple_menu_keys:
        return simple_menu[command_args[0]]()


def say_hi():
    print("Saying hi")
    return "Wplay chatbot says hi! Hope you are having a nice day..."

def say_goodmorning() :
    print("Saying good morning")
    return "Bot says Good Morning! Have a Good Day..."

def say_goodnight() :
    print("Saying good night")
    return "Bot says Good Night! Sweet Dreams..."

def say_fine() :
    print("Saying I am Fine!")
    return "Bot says I am Fine Thank You! How are you?"

def _help_commands():
        print("Asking for help")
        return "How may I assist you with help\n"\
               "List of commands:\n" \
               "/hi (bot says hi), " \
               "/all_commands (ist of all commands), " \
               "/good morning, " \
               "/good night, " \
               "/how are you?"


