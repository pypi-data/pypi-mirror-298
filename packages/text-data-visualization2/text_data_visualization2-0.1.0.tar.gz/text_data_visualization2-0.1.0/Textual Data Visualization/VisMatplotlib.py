import matplotlib.pyplot as plt
import OptionsColumn as optCol

#---------PIE CHARTS
def visPieChart(file):

    col_1, col_2 = optCol.twoColumns(file, "labels", "values")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    
    fig, ax = plt.subplots()
    ax.pie(file.iloc[:, col_2], labels=file.iloc[:, col_1])
    plt.title(file.columns[col_1] + " x " + file.columns[col_2])
    plt.show(block=False)


#---------BAR CHARTS
def visBarPlot(file):
    
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig, ax = plt.subplots()
    ax.bar(file.iloc[:, col_1], file.iloc[:, col_2])
    plt.title(file.columns[col_1] + " x " + file.columns[col_2])
    plt.grid()
    plt.xlabel(file.columns[col_1])
    plt.ylabel(file.columns[col_2])
    plt.show(block=False)
    

#---------LINE CHARTS
def visLineChart(file):

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    plt.grid()
    plt.plot(file.iloc[:, col_1], file.iloc[:, col_2])
    plt.title(file.columns[col_1] + " x " + file.columns[col_2])
    plt.show(block=False) 


#---------SCATTER PLOT
def visScatterPlot(file):
    
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    plt.grid()
    plt.scatter(file.iloc[:, col_1],file.iloc[:, col_2])
    plt.show(block=False)


