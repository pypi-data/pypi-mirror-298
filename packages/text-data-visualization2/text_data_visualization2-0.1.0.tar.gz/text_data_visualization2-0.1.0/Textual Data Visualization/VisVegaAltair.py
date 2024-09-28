import altair as alt
import OptionsColumn as optCol


#---------PIE CHART
def visPieChart(file):
    alt.renderers.enable("browser")

    col_1, col_2 = optCol.twoColumns(file, "labels", "values")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = alt.Chart(file).mark_arc().encode(
        theta=alt.Theta(field=file.columns[col_2], type="quantitative"),
        color=alt.Color(field=file.columns[col_1], type="nominal"),
    )

    fig.show()

#---------BAR PLOT
def visBarPlot(file):
    alt.renderers.enable("browser")

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)
    
    fig = alt.Chart(file).mark_bar().encode(
    x=file.columns[col_1],
    y=file.columns[col_2]
    )

    fig.show()

#---------LINE CHART
def visLineChart(file):
    alt.renderers.enable("browser")

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = alt.Chart(file).mark_line().encode(
    x=file.columns[col_1],
    y=file.columns[col_2]
    )

    fig.show()

#---------SCATTER PLOTS
def visScatterPlot(file):
    alt.renderers.enable("browser")

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")



    #---------------POINTNAME
    choice1 = input("Choose a column to name the points? Y/N: ")
    while(choice1.upper() != 'Y' and choice1.upper() != 'N'):
        print("Choose only Y or N.")
        print()
        choice1 = input("Choose a column to name the points? Y/N: ")

    if(choice1.upper() == 'Y'):
        pointName = input("Choose a column for the points name: ")
        pointName = int(pointName) -1

    #---------------COLOR
    choice2 = input("Choose a column to color group the points? Y/N: ")
    while(choice2.upper() != 'Y' and choice2.upper() != 'N'):
        print("Choose only Y or N.")
        print()
        choice2 = input("Choose a column to color group the points? Y/N: ")

    if(choice2.upper() == 'Y'):
        pointGroup = input("Choose a column to color group the points: ")
        pointGroup = int(pointGroup) -1


    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)
    
    if(choice1.upper() == 'N' and choice2.upper() == 'N'):
        fig = alt.Chart(file).mark_circle(size=60).encode(x=file.columns[col_1], y=file.columns[col_2],
        tooltip=[ file.columns[col_1], file.columns[col_2]]
        ).interactive()

    if(choice1.upper() == 'Y' and choice2.upper() == 'N'):
        fig = alt.Chart(file).mark_circle(size=60).encode(x=file.columns[col_1], y=file.columns[col_2],
        tooltip=[file.columns[pointName], file.columns[col_1], file.columns[col_2]]
        ).interactive()


    if(choice1.upper() == 'N' and choice2.upper() == 'Y'):
        fig = alt.Chart(file).mark_circle(size=60).encode(x=file.columns[col_1], y=file.columns[col_2],
        color=file.columns[pointGroup],
        tooltip=[file.columns[pointGroup], file.columns[col_1], file.columns[col_2]]
        ).interactive()

    if(choice1.upper() == 'Y' and choice2.upper() == 'Y'):
        fig = alt.Chart(file).mark_circle(size=60).encode(x=file.columns[col_1], y=file.columns[col_2],
        color=file.columns[pointGroup],
        tooltip=[file.columns[pointName], file.columns[pointGroup], file.columns[col_1], file.columns[col_2]]
        ).interactive()

    fig.show()

#---------GROUPED BAR PLOT
def visGroupedBarPlot(file):
    alt.renderers.enable("browser")

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    group = input("Choose a column to group the bars: ")
    group = int(group) - 1

    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = alt.Chart(file).mark_bar().encode(
    x=file.columns[col_1],
    y=file.columns[col_2],
    color=file.columns[col_1],
    column=file.columns[group]
    )

    fig.show()

#----STACKED BAR PLOT-----
def visStackedBar(file):
    alt.renderers.enable("browser")

    col_1, col_2 = optCol.twoColumns(file, "x-axis", "y-axis")
    group = input("Choose a column to group the bars: ")
    group = int(group) - 1

    rows = optCol.howManyRows()
    if(rows != 'A'):
        file = file.head(rows)

    fig = alt.Chart(file).mark_bar().encode(
    x=file.columns[col_1],
    y=file.columns[col_2],
    color=file.columns[group]
    )

    fig.show()