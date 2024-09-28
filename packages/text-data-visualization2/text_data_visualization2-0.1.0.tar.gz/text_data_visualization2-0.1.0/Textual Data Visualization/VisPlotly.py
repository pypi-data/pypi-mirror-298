import plotly.express as px
import OptionsColumn as optCol

#---------PIE CHART
def visPieChart(file):

    col_1, col_2 = optCol.twoColumns(file, "labels", "values")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = px.pie(file, values=file.columns[col_2], names=file.columns[col_1], title=file.columns[col_1] + " x " + file.columns[col_2])
    fig.show()


#---------BAR PLOT
def visBarPlot(file):

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = px.bar(file, x=file.columns[col_1], y=file.columns[col_2])
    fig.show()


#---------LINE CHART
def visLineChart(file):

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = px.line(file, x=file.columns[col_1], y=file.columns[col_2])
    fig.show()

#---------MULTIPLE LINES CHART
def visMultipleLines(file):
    lines = []
    max = len(file.columns) - 1
    optCol.columnsView(file)
    col_1 = input("Choose a column for the x-axis: ")
    col_1 = int(col_1) -1

    number = input("Insert an number for the amount of columns/lines you want, or insert 'A' to use all columns: ")
    while(not verifiesInput(number, max)):
             print("Invalid Input! Insert 'A' or a number between 1 and " + str(max) + ".")
             print()
             number = input("Insert an number for the amount of columns/lines you want, or insert A to use all columns: ")
    
    if(number.upper() == 'A'):
        lines = list(file.columns)
        lines.remove(file.columns[col_1])
    else: 
         for i in range(int(number)):
            n = input("Choose column " + str(i + 1) + ": ")
            n = int(n) -1
            lines.append(file.columns[n])

    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = px.line(file, x=file.columns[col_1], y=lines)
    fig.show()

#---------BUBBLE CHART
def visBubbleChart(file):
    
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    size = input("Choose a column for the bubble size: ")
    size = int(size) - 1
    
    
    #---------------BUBBLENAME
    choice1 = input("Choose a column to name the bubble? Y/N: ")
    while(choice1.upper() != 'Y' and choice1.upper() != 'N'):
        print("Choose only Y or N.")
        print()
        choice1 = input("Choose a column to name the bubble? Y/N: ")

    if(choice1.upper() == 'Y'):
        bubbleName = input("Choose a column for the bubble name: ")
        bubbleName = int(bubbleName) -1

    #---------------GROUP IT 
    choice2 = input("Choose a column to group the bubbles? Y/N: ")
    while(choice2.upper() != 'Y' and choice2.upper() != 'N'):
        print("Choose only Y or N.")
        print()
        choice2 = input("Choose a column to group the bubbles? Y/N: ")

    if(choice2.upper() == 'Y'):
        bubbleGroup = input("Choose a column to group the bubbles: ")
        bubbleGroup = int(bubbleGroup) -1

    #------ROWS----------
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    #NO NAME ----- NO GROUP
    if(choice1.upper() == 'N' and choice2.upper() == 'N'):
        fig = px.scatter(file, x=file.columns[col_1], y=file.columns[col_2], size=file.columns[size], log_x=True, size_max=60)
    
    #WITH NAME ----- NO GROUP
    elif(choice1.upper() == 'Y' and choice2.upper() == 'N'):
        fig = px.scatter(file, x=file.columns[col_1], y=file.columns[col_2], size=file.columns[size], hover_name=file.columns[bubbleName], log_x=True, size_max=60)
    
    #NO NAME ----- WITH GROUP
    elif(choice1.upper() == 'N' and choice2.upper() == 'Y'):
        fig = px.scatter(file, x=file.columns[col_1], y=file.columns[col_2], size=file.columns[size], color=file.columns[bubbleGroup], log_x=True, size_max=60)
    
    #WITH NAME ----- WITH GROUP
    elif(choice1.upper() == 'Y' and choice2.upper() == 'Y'):
        fig = px.scatter(file, x=file.columns[col_1], y=file.columns[col_2], size=file.columns[size], color=file.columns[bubbleGroup], hover_name=file.columns[bubbleName], log_x=True, size_max=60)
    
    fig.show()


#---------SCATTER PLOTS
def visScatterPlot(file):
    

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    choice = input("Choose a column to name the points? Y/N: ")
    while(choice.upper() != 'Y' and choice.upper() != 'N'):
        print("Choose only Y or N.")
        print()
        choice = input("Choose a column to name the points? Y/N: ")

    if(choice.upper() == 'Y'):
        name = input("Choose a column to name the points: ")
        name = int(name) - 1
        fig = px.scatter(x=file.iloc[:, col_1], y=file.iloc[:, col_2], hover_name=file.iloc[:, name])
    else: 
         fig = px.scatter(x=file.iloc[:, col_1], y=file.iloc[:, col_2])
    
    fig.show()


#----STACKED BAR PLOT-----
def visStackedBar(file):
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    group = input("Choose a column to group the bars: ")
    group = int(group) - 1

    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = px.bar(file, x=file.columns[col_1], y=file.columns[col_2], color=file.columns[group])
    fig.show()


#-----TO VERIFY INPUT-------
def verifiesInput(option, max):
    if(option.isnumeric()):
               number = int(option)
    elif(option.upper()=='A'):
        return True
        
    if(number >= 1 and number <= max):
        return True
    
    return False