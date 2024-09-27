from stringcolor import cs
import random

class Theme:

    @staticmethod
    def Kling(str):
        colors = ["red","DarkRed","DarkRed2","Maroon"]
        
        newstr = ""
        for char in str:
            char = cs(char,random.choice(colors))
            
            newstr += char
        
        return newstr
        
    @staticmethod
    def Beach(str):
        colors = ["Cyan","Aqua","NavajoWhite","SkyBlue","LightYellow"]
        "red","DarkRed","DarkRed2","Maroon"
        newstr = ""
        for char in str:
            char = cs(char,random.choice(colors))
            newstr += char
        
        return newstr
    
    @staticmethod
    def Forest(str):
        colors = ["Green2","Green","DarkGreen","DarkSeaGreen","Green3"]
        
        newstr = ""
        for char in str:
            char = cs(char,random.choice(colors))
            newstr += char
        
        return newstr
    
    @staticmethod
    def Rainbow(str):
        colors = ["Green","Blue","Yellow","Orange","Purple","Red","Aqua","Fuchsia"]
        
        newstr = ""
        for char in str:
            char = cs(char,random.choice(colors))
            newstr += char
        
        return newstr



