from globals import console

def execute_report():
    import webbrowser
    console.print("Willst du einen Fehler auf GitHub melden?")
    report = console.input("(Y/N) Input: ")
    if report.lower() == "y":
        webbrowser.open("https://github.com/Sakushi-Dev/project_aurora/issues")
    else:
        return None