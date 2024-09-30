#-------------COLUMNS VIEW
#Prints all columns available on file and return the number of columns
def columnsView(file):
    print()
    print("Columns Available:")
    index = 1
    for col in file.columns:
        print(str(index) + ' - ' + col)
        index +=1
    print()
    return index



#--------ASKS FOR COLUMNS
def twoColumns(file, text1, text2):
    max = columnsView(file)

    col_1 = input("Choose a column for the " +text1 + ": ")
    while(not verifiesColumnInput(col_1, max)):
        print("Invalid!")
        col_1 = input("Choose a column for the " +text1 + ": ")
    

    col_2 = input("Choose a column for the " +text2 + ": ")
    while(not verifiesColumnInput(col_2, max)):
        print("Invalid!")
        col_2 = input("Choose a column for the " +text2 + ": ")

    col_1 = int(col_1) - 1
    col_2 = int(col_2) - 1

    return col_1, col_2


#-------ASKS HOW MANY ROWS
def howManyRows(): 
    rows = input("Insert the amount of rows or insert 'A' to use all: ")
    while(not verifiesRowInput(rows)):
        print("Invalid!")
        print()
        rows = input("Insert the amount of rows or insert 'A' to use all: ")

    if(rows.isnumeric()):
        rows = int(rows)
    else:
        rows= rows.upper()

    return rows


def verifiesColumnInput(number, max):
    if(not number.isnumeric()):
        return False
    
    number = int(number)
    if(number < 1 or number > max):
        return False
    return True



def verifiesRowInput(option):
    if(option.isnumeric()):
        return True
    elif(option.upper()=='A'):
        return True
    
    return False

def invalidColumnInput(number, file):
    max = len(file.columns)
    if(verifiesColumnInput(number, max)):
        return False
    
    print("Invalid!")
    return True

