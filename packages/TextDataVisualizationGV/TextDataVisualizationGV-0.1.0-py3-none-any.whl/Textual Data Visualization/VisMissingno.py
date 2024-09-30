import missingno as msno
import matplotlib.pyplot as plt

def visDataQuality(file):

    print()
    print("1 - Sample 500 rows.")
    print("2 - All rows.")

    choice = input("Select 1 or 2: ")
    while(choice.upper() != '1' and choice.upper() != '2'):
        print("Choose only 1 or 2.")
        choice = input("Select 1 or 2: ")

    
    if(choice.upper() == '1'): 
        msno.matrix(file.sample(500))
    else:
        msno.matrix(file)

    plt.gcf()
    plt.show(block=False)