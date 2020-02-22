import argparse
import cv2
import pandas as pd
import os

#How to run this file
#python color_detection.py -i <path of image>

arg = argparse.ArgumentParser()

def get_coord(img):
    height, width,_ = img.shape
    x = width/2
    y = height/2
    x=int(x)
    y=int(y)
    b,g,r = img[y,x]
    #print("colors")
    #print(r,g,b)
    return r,g,b

def read_csv():
    index = ["color_code", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('colors.csv', names=index, header=None)
    return csv

def distance(r,g,b):
    colors = read_csv()                                 #reads csv file using pandas. List of all colors.
    min=255+255+255
    pos=0
    for i in range(len(colors)):
        d=abs(r-colors.loc[i,"R"])+abs(g-colors.loc[i,"G"])+abs(b-colors.loc[i,"B"])
        if(d<=min):
            min=d
            pos=i
    return colors.loc[pos,"color_code"]

def find_matching_color(final_color):
    index = ["c","c2"]
    csv = pd.read_csv('colorMatching.csv',names=index,header=None)
    list_colors = []
    for i in range(len(csv)):
        if csv.loc[i,"c"]==final_color:
            list_colors.append(csv.loc[i,"c2"])
    return list_colors

def find_cloth(list_colors):
    file_list = os.listdir(r"C:\Users\Lenovo\Desktop\clothes")
    for filename in file_list:
        path = "clothes\\"+ str(filename)
        img2 = cv2.imread(path)
        r,g,b = get_coord(img2)
        temp_color = distance(r,g,b)
        for listed in list_colors:
            if listed==temp_color:
                cv2.imshow("whatToWear",img2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()




#passing inline arguments ( path of image )
arg.add_argument('-i','--image',required=True, help="Image Path")
args = vars(arg.parse_args())
img_path = args['image']
img = cv2.imread(img_path)

#cv2.imshow("image",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()



r,g,b = get_coord(img)                              #finds r,g,b of the img image
print(r,g,b)

final_color = distance(r,g,b)                       #finds color name based on the min distance
print(final_color)

list_colors = find_matching_color(final_color)      #list of matching colors
find_cloth(list_colors)                             #finding clothes that match the color
