import VisWordCloud as VWC
import VisMissingno as VM
import VisMatplotlib as VMPL
import VisPlotly as VP
import VisSeaborn as VSB
import VisBokeh as VB
import VisVegaAltair as VVA

#------------VISUALIZATION TYPE VIEW
#Prints the visualization types for user
def visTypeView(csvLoaded, txtLoaded):
        print()
        print("------------------------------")
        print("Types of Visualization:")
        print("1 - WordCloud (TXT File)")
        print("2 - Bar Plot")
        print("3 - Pie Chart")
        print("4 - Bubble Chart")
        print("5 - Line Chart")
        print("6 - Multiple Lines Chart")
        print("7 - Grouped Bar Plot")
        print("8 - Stacked Bar Plot")
        print("9 - Scatter Plot")
        print("10 - Data Quality")
        print()
        if(csvLoaded):
            print("C - Load new CSV File")
        if(txtLoaded):
            print("T - Load new TXT File")
        print("X - End the Program")
        print("------------------------------")
        print()

#--------------ASKS VALID VISUALIZATION TYPE
def visTypeSelect(csvLoaded, txtLoaded):
    visTypeView(csvLoaded, txtLoaded)
    option = input("Select Option: ")
    while(verifiesVisType(option) == False):
        print()
        print("Invalid Option!")
        option = input("Select Option: ")
    print()
    return option.upper()

#-------------ASSERTS VISUALIZATION OPTION IS VALID
def verifiesVisType(option):
        number = 0
        if(option.isnumeric()):
               number = int(option)
        elif(option.upper()=='X' or option.upper()=='C' or option.upper()=='T'):
               return True
        
        if(number >= 1 and number <= 10):
               return True
        return False

#--------------SWITCHES TO VISUALIZATION ROUTINE
def switchType(option, csv_file, txt_file):
    print()
    match option:
         
        #1 - WordCloud
        case "1":
            print("------------------------------")
            print("-       1 - WordCloud        -")
            print("------------------------------")
            VWC.visWordCloud(txt_file)
            print("------------------------------")

        #2 - Bar Plot
        case "2":
            print("------------------------------")
            print("-        2 - Bar Plot        -")
            print("------------------------------")

            library = libraryChoice(1, 2, 3, 4, 5)
            match library:
                case 1:
                      VB.visBarPlot(csv_file)
                case 2:
                      VMPL.visBarPlot(csv_file)
                case 3:
                      VP.visBarPlot(csv_file)
                case 4:
                      VSB.visBarPlot(csv_file)
                case 5:
                      VVA.visBarPlot(csv_file)

        #3 - Pie Chart
        case "3": 
            print("------------------------------")
            print("-       3 - Pie Chart        -")
            print("------------------------------")
            library = libraryChoice(1, 2, 3, 5)
            match library:
                case 1:
                      VB.visPieChart(csv_file)
                case 2:
                      VMPL.visPieChart(csv_file)
                case 3:
                      VP.visPieChart(csv_file)
                case 5:
                      VVA.visPieChart(csv_file)

        #4 - Bubble Chart
        case "4":
            print("------------------------------")
            print("-      4 - Bubble Chart      -")
            print("------------------------------")
            VP.visBubbleChart(csv_file)

        #5 - Line Chart
        case "5":
            print("------------------------------")
            print("-       5 - Line Chart       -")
            print("------------------------------")
            library = libraryChoice(1, 2, 3, 4, 5)
            match library:
                case 1:
                      VB.visLineChart(csv_file)
                case 2:
                      VMPL.visLineChart(csv_file)
                case 3:
                      VP.visLineChart(csv_file)
                case 4:
                      VSB.visLineChart(csv_file)
                case 5:
                      VVA.visLineChart(csv_file)

        #6 - Multiple Lines Chart
        case "6":
            print("------------------------------")
            print("-  6 - Multiple Lines Chart  -")
            print("------------------------------")
            library = libraryChoice(1, 3)
            match library:
                case 1:
                      VB.visMultipleLines(csv_file)
                case 3:
                      VP.visMultipleLines(csv_file)

        #7 - Grouped Bar Plot 
        case "7":
            print("------------------------------")
            print("-    7 - Grouped Bar Plot    -")
            print("------------------------------")
            library = libraryChoice(4, 5)
            match library:
                case 4:
                      VSB.visGroupedBarPlot(csv_file)
                case 5:
                      VVA.visGroupedBarPlot(csv_file)
    
        #8 - Stacked Bar Plot  
        case "8":
            print("------------------------------")
            print("-    8 - Stacked Bar Plot    -")
            print("------------------------------")
            library = libraryChoice(3, 5)
            match library:
                case 3:
                      VP.visStackedBar(csv_file)
                case 5:
                      VVA.visStackedBar(csv_file)
        
        #9 - Scatter Plot
        case "9":
            print("------------------------------")
            print("-      9 - Scatter Plot      -")
            print("------------------------------")
            library = libraryChoice(1, 2, 3, 4, 5)
            match library:
                case 1: 
                      VB.visScatterPlot(csv_file)
                case 2:
                      VMPL.visScatterPlot(csv_file)
                case 3:
                      VP.visScatterPlot(csv_file)
                case 4:
                      VSB.visScatterPlot(csv_file)
                case 5:
                      VVA.visScatterPlot(csv_file)

        #10 - Data Quality
        case "10":
            #10 - Data Quality
            print("------------------------------")
            print("-      10 - Data Quality      -")
            print("------------------------------")
            VM.visDataQuality(csv_file)
        
        #C - Load new CSV File
        case "C":
            print("------------------------------")
            
        #T - Load new TXT File       
        case "T":
            print("------------------------------")
               

def libraryChoice(*libNumbers):

    libraries = ["Bokeh", "Matplotlib", "Plotly", "Seaborn", "Vega-Altair"]
    strLib = ""

    print("Libraries available for this type of Visualization: ")
    for lib in libNumbers:
        print(str(lib) + " - " +libraries[lib-1])
        strLib = strLib + str(lib) + " "
      
        
    option = input("Select the library: ")
    while(not validInput(option, libNumbers)):
        print("Invalid Input! Insert one of these: " +strLib)
        print()
        option = input("Select the library: ") 

    option = int(option)
    return option

def validInput(number, options):
    if(not number.isnumeric()):
        return False
    elif(not int(number) in options):
        return False
     
    return True
