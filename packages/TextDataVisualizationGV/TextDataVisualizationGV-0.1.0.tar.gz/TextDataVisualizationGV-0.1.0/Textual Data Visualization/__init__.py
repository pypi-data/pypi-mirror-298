

#OTHER FILES
import OptionsVis as optVis
import FileRelated as filRel


if __name__ == '__main__':

    csvFileLoaded = False
    csv_file = None
    txtFileLoaded = False
    txt_file = None

    print("-----------------------------------------------------------------------------")
    print("This program offers 10 different types of data visualizations to choose from.")
    print("Except for Word Cloud, which requires a TXT file, the others need a CSV file.")
    print("Files only need to be loaded once and can be reused multiple times.")
    print("Be sure to save any images you want before generating a new one.")
    print("-----------------------------------------------------------------------------")

    #LOOP | RUNS MENU FOR VISUALIZATION TYPES (Value -> visType != 'x')
    #SHOWS OPTIONS AND ASKS VALID VISUALIZATION TYPE
    visType = optVis.visTypeSelect(csvFileLoaded, txtFileLoaded)
    
    while(visType != 'X'):
        # CHECKS IF FILES ARE LOADED
        if(visType == '1' and not txtFileLoaded):
            txt_file = filRel.loadsTXTFile()
            txtFileLoaded = True
        elif(visType == 'C'):
            print("------------------------------")
            print("-   C - Load new CSV File    -")
            csv_file = filRel.loadsCSVFile()
            csvFileLoaded = True
        elif(visType == 'T'):
            print("------------------------------")
            print("-   T - Load new TXT File    -")
            txt_file = filRel.loadsTXTFile()
            txtFileLoaded = True
        elif(not csvFileLoaded and visType != '1'):
            csv_file = filRel.loadsCSVFile()
            csvFileLoaded = True
        
        # SWITCHES TO VISUALIZATION TYPE ROUTINE
        optVis.switchType(visType, csv_file, txt_file)
        print()


        # 4.4 - 'RETURNS' STEP 4 OR ENDS IF visType == 'x'
        visType = optVis.visTypeSelect(csvFileLoaded, txtFileLoaded)

    # ENDS PROGRAM
    print("------------------------------")
    print("-    The Program Has Ended   -")
    print("------------------------------")
    

