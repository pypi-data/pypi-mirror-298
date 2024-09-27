# The main function will be called by the script loader
def main(interfaces):
    """Doc string allow you to read the function of a script in your program"""

    # Getting the blank interface
    interface = interfaces["blank"]

    # Getting the variable from the parameterfield
    var = interface.var

    # Priting the variable to the 
    interface.terminal.terminal_msg(f"Our variable is currently: {var}")

    # Calling a method from the interface
    interface.mymethod(var)
