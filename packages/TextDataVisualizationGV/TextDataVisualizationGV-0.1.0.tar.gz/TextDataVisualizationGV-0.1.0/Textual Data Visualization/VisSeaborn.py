import seaborn as sns
import OptionsColumn as optCol
import matplotlib.pyplot as plt

#---------BAR PLOT
def visBarPlot(file):
    sns.set_theme(style="darkgrid")
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)


    plt.figure()
    sns.barplot(x=file.columns[col_1], y=file.columns[col_2], data=file, ci=None)
    plt.show(block=False)  

#---------LINE CHART
def visLineChart(file):
    sns.set_theme(style="darkgrid")
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    plt.figure()
    sns.lineplot(x=file.columns[col_1], y=file.columns[col_2], data=file)
    plt.show(block=False)

#---------SCATTER PLOT
def visScatterPlot(file):
    sns.set_theme(style="darkgrid")
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)
    
    plt.figure()
    sns.scatterplot(x=file.columns[col_1], y=file.columns[col_2], data=file)
    plt.show(block=False)

#---------GROUPED BAR PLOT
def visGroupedBarPlot(file):
    sns.set_theme(style="darkgrid")
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")

    group = input("Choose a column to group the bars: ")
    while(optCol.invalidColumnInput(group, file)):
        print()
        group = input("Choose a column to group the bars: ")

    group = int(group) - 1


    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)


    plt.figure()
    sns.barplot(x=file.columns[col_1], y=file.columns[col_2], hue=file.columns[group], data=file)
    plt.show(block=False)