"""
Arnaud Tadonkeng
Sep 16, 2026
Lab 5: Review of class, objects, methods and attributes
"""
print("\n ----- Example 1: Class Circle ------")
class Circle():
    #values that need to pass to the object of class circle
    def __init__(self, radius, color):
        self.r = radius
        self.c = color

    #attributes
    pi = 3.14157

    #method
    def circumference(self):
        return 2*self.pi*self.r



#create instance object of the class
c1 = Circle(2, "red")
print(c1.c)
print(c1.circumference())

print("\n ---- Example 2: class Rectangle ------")
import matplotlib.pyplot as pit
class Rectangle():
    def __init__(self, height, width, color):
        self.h = height
        self.w = width
        self.c = color

    #method to calculate the area
    def area(self):
        return self.w * self.h

    #method to calculate the perimeter
    def perimeter(self):
        return 2*self.w + 2*self.h

    #method to draw the rectangle
    """
    def drawRectangle(self):
        pit.gca().add_patch(pit.Rectangle((0,0), self.w, self.h, fc=self.c))
        pit.axis('scaled')
        pit.show()
    """

import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, h, w, c):
        self.h = h
        self.w = w
        self.c = c

    def perimeter(self):
        return 2 * (self.h + self.w)

    def area(self):
        return self.h * self.w

    # method to draw the rectangle
    def drawRectangle(self):
        plt.gca().add_patch(plt.Rectangle((0, 0), self.w, self.h, fc=self.c))
        plt.axis('scaled')
        plt.show()


# create instance object of the class
r1 = Rectangle(2, 3, "olive")
print(f"The perimeter of rectangle with height = {r1.h} and width = {r1.w} is {r1.perimeter()}")
r1.drawRectangle()