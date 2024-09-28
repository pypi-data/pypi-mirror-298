from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#ASK IF TEXT IS PREP OR NOT
def visWordCloud(file):

    choice = input("Use a image as countour for the Word Cloud? Y/N: ")
    while(choice.upper() != 'Y' and choice.upper() != 'N'):
        print("Choose only Y or N.")
        choice = input("Use a image as boundry for the Word Cloud? Y/N: ")

    
    if(choice.upper() == 'N'): 
        simpleWC(file)
    else:
        personalizedWC(file)


def simpleWC(file):
    plt.close()
    colormap = chooseColormap()
    wc = WordCloud(background_color='black', colormap = colormap, stopwords = ['meta'], width = 800, height = 500).generate(file)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')

    plt.show(block=False)
    


def personalizedWC(file):
    plt.close()
    print()
    print("The image format must be JPG/JPEG.")
    print("The image should be black and white, black where you want the text to be.")
    print()
    image_path = input("Insert the image: ")

    mask = np.array(Image.open(image_path))

    colormap = chooseColormap()

    #SIZES THE IMAGE
    if(mask.shape[0]>mask.shape[1]):
        h = 16
        w = mask.shape[1]/mask.shape[0]*16
    else:
        w = 16
        h = mask.shape[0]/mask.shape[1]*16


    wc = WordCloud(background_color='black', mask= mask, contour_width=2, contour_color='black', colormap = colormap).generate(file)
    plt.figure(figsize=[w,h])
    #plt.tight_layout()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show(block=False)
    

def chooseColormap():
    print()
    color = ["Accent", "Blues_r", "BrBG_r", "BuGn", "BuPu_r", "Pastel1", "PuRd_r", "twilight_shifted"]
    option = color[1]

    choice = input("Chance colormap? Y/N: ")
    
    while(choice.upper() != 'Y' and choice.upper() != 'N'):
        print("Choose only Y or N.")
        choice = input("Chance colormap? Y/N")


    if(choice.upper() == 'Y'):
        print("Colormap options: ")
        print("1 - Accent")
        print("2 - Blues_r [Default]")
        print("3 - BrBG_r")
        print("4 - BuGn")
        print("5 - BuPu_r")
        print("6 - Pastel1")
        print("7 - PuRd_r")
        print("8 - twilight_shifted")
        
        number = input("Select the colormap: ")
        while(not isVaild(number)):
            print("Invalid! Insert a number between 1 and 8.")
            print()
            number = input("Select the colormap: ")

        option = color[int(number) - 1]    
    
        
    return option



def isVaild(option):
        number = 0
        if(option.isnumeric()):
               number = int(option)
        else:
               return False
        
        if(number >= 1 and number <= 8):
               return True
        return False

        
