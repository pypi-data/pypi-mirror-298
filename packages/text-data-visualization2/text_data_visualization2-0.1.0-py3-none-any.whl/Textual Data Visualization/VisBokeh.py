from bokeh.palettes import Category20
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
import OptionsColumn as optCol
from math import pi

#---------PIE CHART
def visPieChart(file):
    
    col_1, col_2 = optCol.twoColumns(file, "labels", "values")

    print("This library only allows for 20 rows!")
    rows = optCol.howManyRows()
    while(rows!='A' and rows > 20):
        print("This library only allows for 20 rows!")
        rows = optCol.howManyRows()
    
    if(rows != 'A'):
        file = file.head(rows)
    elif(len(file)>20):
        file = file.head(20)
    
    fileCopy = file.copy()

    tooltips = "@" +fileCopy.columns[col_1] +": @" + fileCopy.columns[col_2]
    fileCopy.loc[:, 'angle'] = fileCopy[fileCopy.columns[col_2]]/fileCopy[fileCopy.columns[col_2]].sum() * 2*pi
    fileCopy.loc[:, 'color'] = Category20[len(fileCopy)]

    p = figure(toolbar_location=None, tools="hover", tooltips=tooltips, x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field=fileCopy.columns[col_1], source=fileCopy)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    show(p)
    
#---------BAR PLOT
def visBarPlot(file):
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")

    
    rows = optCol.howManyRows()
    
    if(rows != 'A'):
        file = file.head(rows)
    
    
    color = ["navy"] * len(file)

    p = figure(x_range=file.iloc[:, col_1], toolbar_location=None)

    p.vbar(x=file.iloc[:, col_1], top=file.iloc[:, col_2], width=0.9,
            line_color='white', fill_color=color)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

#---------LINE CHART
def visLineChart(file):
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    p = figure(x_axis_label=file.columns[col_1], y_axis_label=file.columns[col_2])
    p.line(file.iloc[: , col_1], file.iloc[: , col_2], line_width=2)
    show(p)

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
    
    p = figure()
    p.vline_stack(lines, x=file.columns[col_1], source=file)
    show(p)

#---------SCATTER PLOT
def visScatterPlot(file):
    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)
    
    p = figure(x_axis_label=file.columns[col_1], y_axis_label=file.columns[col_2])
    p.scatter(file.iloc[: , col_1], file.iloc[: , col_2], size=15, color="navy", alpha=0.5)
    show(p)

#-----TO VERIFY INPUT-------
def verifiesInput(option, max):
    if(option.isnumeric()):
               number = int(option)
    elif(option.upper()=='A'):
        return True
        
    if(number >= 1 and number <= max):
        return True
    
    return False