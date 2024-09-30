import pandas as pd
##-----------CSV FILE-----------
def asksEncodingOption():
    print("Encoding Options:")
    print("1 - latin1 (Default)")
    print("2 - utf-8")
    print("3 - iso-8859-1")
    print("4 - cp1252")

    number = input("Choose one option: ")
    print()
    
    match number:
        case "2":
            option = "utf-8"
        case "3":
            option = "iso-8859-1"
        case "4":
            option = "cp1252"
        case _:
            option = "latin1"

    return option

def loadsCSVFile():
    print("-----------CSV FILE-----------")
    print()
    #1 - ASKS CSV FILE AND FILE DELIMITER
    path = input("Insert CSV file: ")
    delimiter = input("Insert the file delimiter: ")

    #2 - ASKS FOR ENCODING TYPE AND LOADS FILE
    print()
    encodingType = asksEncodingOption()
    #3 - LOADS FILE 
    
    csv_file = pd.read_csv(path, encoding=encodingType, low_memory=False, delimiter=delimiter)

    return csv_file





#-----------TXT FILE-----------
def loadsTXTFile():
    print("-----------TXT FILE-----------")
    print()
    #1 - ASKS CSV FILE AND FILE DELIMITER
    path = input("Insert TXT file: ")
    print()
    #2 - LOADS FILE 
    txt_file = open(path).read()

    return txt_file
