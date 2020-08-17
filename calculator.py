import pygame
import re
from math import sin, cos, tan, asin, acos, atan, log, sqrt, factorial


#Math functions that aren't included in math library
def cot(x):
    return cos(x)/sin(x)

def acot(x):
    return pi / 2 - atan(x)

def ln(x):
    return log(round(x, 5)) #ln was throwing some random values, so I round the x and that fixed the problem.

def root(x, n):
    return x ** (1.0/n)

def find_abs_max_in_range(f, rang):
    max_abs_f = float("-inf")
    for x in rang:
        try:
            if abs(f(x)) > max_abs_f:
                max_abs_f = abs(f(x))
        except (ZeroDivisionError, OverflowError, ValueError):
            pass
    return max_abs_f
        

#Constants
#GUI Constants
window_size = (510, 297)
directory = "images\\"
button_names = ["e", "sin", "cos", "lp", "rp", "back", "clear", "graph", "pi", "tan", "cot", "power", "factorial", "7", "8", "9", "over",
                "square", "phi", "asin", "acos", "root", "log2", "4", "5", "6", "times", "sqrt", "psi", "atan", "acot", "x","1", "2", "3",
                "minus", "equals", "mi", "log", "ln", "help", "0", "point", "plus"] #Sorted as in GUI.
black = (0, 0, 0)
gray = (196, 196, 196)
cyan = (209, 246, 255)
light_blue = (42, 206, 247)
white = (255, 255, 255)

#Mathematical Constants
e = 2.71828
pi = 3.14159
phi = 1.61803
psi = 3.35988
mi = 1.45136

#Classes 
class Calculator:
    keywords_to_math = {"plus": "+", "minus": "-", "times": "*", "over": "/", "power": "**", "square": "**2", "lp": "(",
                        "rp" : ")", "point": ".", "log2": "2log", "e": str(e), "phi": str(phi), "pi": str(pi), "psi": str(psi), "mi": str(mi)}
    keywords_to_screen = {"plus": "+", "minus": "-", "times": "*", "over": "/", "power": "^", "square": "^2", "lp": "(", "rp" : ")",
                          "factorial": "!", "point": ".", "phi": "φ", "pi": "π", "psi": "Ψ", "mi": "μ", "log2": "2log"}
    def __init__(self):
        #Calculation and screen attributes
        self.eq_display = ""
        self.eq_math = ""
        self.answer = ""
        self.buttons = []
        
        #Buttons initialization
        global calculator_buttons
        win.fill(cyan)
        calculator_buttons = []
        x_counter = 10
        y_counter = 100 + 10
        i = 0
        for button_name in button_names:
            self.buttons.append(Button(button_names[i], x_counter, y_counter))
            if i in [0, 2, 4, 8, 10, 12, 18, 20, 22, 28, 30, 31, 37, 39, 40]: 
                x_counter += self.buttons[i].width + 60 #The big space between buttons
            elif i in [7, 17, 27, 36]:
                y_counter += 25 + 12
                x_counter = 10
            else:
                x_counter += self.buttons[i].width + 10
            i += 1

    def math_fix(self):#Transform the equation entered to the ideal form.
        for factorial in re.findall("[0-9|x]+factorial", self.eq_math): #5factorial -> factorial5
            num = factorial[:-len("factorial")]
            self.eq_math = self.eq_math.replace(factorial, "factorial" + num, 1)
        
        for func in ["asin", "acos", "atan", "acot", "sin", "cos", "tan", "cot", "ln", "sqrt", "x"]: #3sin31 -> 3 * sin31
            for call in re.findall("[0-9|.|x]+" + func, self.eq_math):
                num = call[:-len(func)]
                self.eq_math = self.eq_math.replace(call, num + "*" + call[len(num):])
                
        for func in ["asin", "acos", "atan", "acot", "sin", "cos", "tan", "cot", "ln", "sqrt", "factorial"]: #sin31 -> sin(31)
            for call in re.findall(func + "[0-9|.|x]+", self.eq_math):
                num = call[len(func):]
                self.eq_math = self.eq_math.replace(call, call[:-len(num)] + "(" + num + ")", 1)

        for call in re.findall("[0-9|.|x]+\(.+\)", self.eq_math): # 31(anything) -> 31 * (anything)
            par_index = call.index("(")
            num = call[:par_index]
            self.eq_math = self.eq_math.replace(call, num + "*" + call[par_index:])
            
        for func in ["log", "root"]: #5log3 -> log(3, 5)
           for call in re.findall("[0-9|.|x]+" + func+"[0-9|.|x]+", self.eq_math):
               num1 = call[:call.index(func)]
               num2 = call[call.index(func)+len(func):]
               self.eq_math = self.eq_math.replace(call, func + "(" + num2 + "," + num1 + ")")
    
    def calculate(self):
        self.math_fix()
        try:
            self.answer = ""
            self.answer = eval(self.eq_math, globals())
            self.answer = round(self.answer, 8) #Round to 8 float digits.
            if type(self.answer) == float: #0.0 -> 0 
                if self.answer.is_integer():
                    self.answer = str(int(self.answer))
                    return
            self.answer = str(self.answer)
        except Exception as e:
            self.answer = str(e)
                
    def eq_append(self, string):
        global calculator_mode, grapher_mode
        global grapher_mode
        if string == "clear": #Clear the equations entered and refresh the GUI.
            self.eq_display = ""
            self.answer = ""
            self.eq_math = ""
            self.draw_screen()
        elif string == "back": #Removes the last member of equation added in math eq and display eq.
            display_member_found = False
            math_member_found = False
            possible_common_members = ["sin", "cos", "tan", "cot", "asin", "acos", "atan", "acot", "log", "ln", "(", ")", "0", "1", "2", "3",
                "4", "5", "6", "7", "8", "9", "x", "+", "-", "*", "/", ".", "e"]        
            for member in possible_common_members:
                if self.eq_display.endswith(member) and not display_member_found:
                    self.eq_display = self.eq_display[:-len(member)]
                    display_member_found = True
                if self.eq_math.endswith(member) and not math_member_found:
                    self.eq_math = self.eq_math[:-len(member)]
                    math_member_found = True

            for key_member in self.keywords_to_screen:
                if self.eq_display.endswith(self.keywords_to_screen[key_member]) and not display_member_found:
                    self.eq_display = self.eq_display[:-len(self.keywords_to_screen[key_member])]
                    display_member_found = True

            for key_member in self.keywords_to_math:
                if self.eq_math.endswith(self.keywords_to_math[key_member]) and not math_member_found:
                    self.eq_math = self.eq_math[:-len(self.keywords_to_math[key_member])]
                    math_member_found = True
            self.draw_screen()
        elif string == "graph": #Draw the grapher GUI.
            self.math_fix()
            error = False
            try:
                eval(self.eq_math)
            except NameError: #NameError is normal, as the equation may contain x-value.
                pass
            except Exception as e:
                error = True
                self.eq_display = str(e)
                self.draw_screen()
            if not error:
                grapher_mode = True
                calculator_mode = False
                grapher.draw(1)
        elif string == "help": #Draw the help GUI.
            calculator_mode = False
            grapher_mode = False
            draw_help()
        elif string == "equals": #Compute the given problem.
            self.calculate()
            self.draw_screen()
        else:
            if string in self.keywords_to_screen: #Translate button names to display and math appopriate strings
                self.eq_display += self.keywords_to_screen[string]
            else:
                self.eq_display += string
            if string in self.keywords_to_math:
                self.eq_math += self.keywords_to_math[string]   
            else:
                self.eq_math+= string
            self.draw_screen()
            
    def draw_screen(self):
        pygame.draw.rect(win, cyan, (0, 0, 510, 100)) #Clear the old screen.
        pygame.draw.rect(win, black, (1, 1, 506, 23), 2)
        img = font1.render(self.eq_display, False, black)
        win.blit(img, (3, 5))

        pygame.draw.rect(win, black, (1, 26, 506, 73), 2)
        img = font1.render(self.answer, False, black)
        win.blit(img, (3, 30))

        
class Grapher:
    def draw(self, zoom):
        def f(x): return eval(calculator.eq_math)
        self.f = f #used in pair graphing
        self.zoom = zoom #used in pair graphing
        #Draw the standard GUI
        global grapher_goback_button
        grapher_goback_button = Button("back", 480, 10)
        win.fill(white)
        f_img = font1.render("f = " + calculator.eq_display, False, black)
        win.blit(f_img, (5, 10))
        pygame.draw.rect(win, gray, (2, 36, 506, 227), 2)

        zoom_img = font2.render("zoom: " + "× " + str(round(1/zoom, 3)), False, black)
        win.blit(zoom_img, (15, 36 + 227 + 5))
        
        pygame.draw.line(win, black, (255, 36), (255, 263), 2) #x-axis
        pygame.draw.line(win, black, (2, 150), (506, 150), 2) #y-axis

        x_counter = 15 # draw x-points
        for i in range(-12, 13): 
            if i == 0:
                x_counter += 20
                continue
            pygame.draw.line(win, black, (x_counter, 150-5), (x_counter, 150+5))
            d = font2.render(str(i*zoom), False, (0, 0, 0))
            win.blit(d, (x_counter-d.get_width()/2, 150+10)) # x text centered at the vertical line
            x_counter += 20
            
        max_abs = find_abs_max_in_range(f, range(-12*zoom, 12*zoom+1)) #draw y-points
        self.max_abs = max_abs
        y_distance = max_abs/5
        y_val_counter = max_abs
        y_counter = 36 + 13.5
        for i in range(-5, 6): 
            if i == 0:
                y_counter += 20
                y_val_counter -= y_distance
                continue
            pygame.draw.line(win, black, (255-5, y_counter), (255+5, y_counter))
            d = font2.render(str(round(y_val_counter, 1)), False, black) #round y_val to 1 float points
            win.blit(d, (255-d.get_width()-10, y_counter)) #Y a little left from the horizontal lines
            y_counter += 20
            y_val_counter -= y_distance
            
        #Draw the function graph for all vertical pixels
        x = -12 * zoom
        x_distance = 12*2*zoom/480
        points = []
        points_entered = 0
        for i in range(480):
            try:
                points.append((i + 13 + 2, window_size[1] - round(((abs(-max_abs - f(x)) * (227 - 13.5 * 2) / (2 * max_abs))) + 36 + 10)))
                pygame.draw.circle(win, black, points[points_entered], 1)
                if points_entered > 1:
                    pygame.draw.line(win, black, points[points_entered-1], points[points_entered], 3)
                points_entered += 1
            except (ZeroDivisionError, OverflowError, ValueError):
                pass
            x += x_distance

    def draw_pair(self, x_cursor):
        self.draw(self.zoom) #Refresh the window
        x_cursor -= 13 + 2 
        if x_cursor >= 0 and x_cursor <= 480:
            try:
                x = round(-12 * self.zoom + 12*2*self.zoom/480 * x_cursor, 3)
                y = round(self.f(x), 3)
                pos = (x_cursor + 13 + 2, window_size[1] - round(((abs(-self.max_abs - y) * (227 - 13.5 * 2) / (2 * self.max_abs))) + 36 + 10))
                pair_image = font2.render("(x, y) = (" + str(x) + ", " + str(y) + ")", False, light_blue)
                pygame.draw.circle(win, light_blue, pos, 4)
            except (ZeroDivisionError, OverflowError, ValueError):
                pair_image = font2.render("(x, y) = (" + str(x) + ", " + "undifined)", False, light_blue)
            win.blit(pair_image, (13 + 360, 36 + 227 + 10))
        
class Button:
    def __init__(self, name, x, y):
        self.name = name
        self.image = pygame.image.load(directory + name + ".jpg")
        self.image_hovered = pygame.image.load(directory + name + "_h.jpg")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hovered = False
        self.clicked = False
        self.x = x
        self.y = y

    def check_if_hovered(self, mouse_x, mouse_y):
        self.hovered =  self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
        return self.hovered
    
    def draw(self):
        if self.hovered:
            win.blit(self.image_hovered, (self.x, self.y))
        else:
            win.blit(self.image, (self.x, self.y))


#Help section, I thought there was no need of class for it. 
def draw_help():
    global help_goback_button
    help_goback_button = Button("back", 480, 10)
    win.fill(cyan)
    y_counter = 5
    with open("help.txt", "r") as f: #font.render doesn't support \n character so I had to write this crap.
        for line in f.readlines():
            text = ""
            for char in line:
                if char != "\n":
                    text += char
                else:
                    win.blit(font2.render(text, False, black), (0, y_counter))
                    text = ""
                    y_counter += 12
                    
            
    
    
#Pygame and GUI initialization
pygame.init()
pygame.font.init()

font1 = pygame.font.SysFont("Palatino Linotype", 20)
font2 = pygame.font.SysFont("Palatino Linotype", 12)
icon = pygame.image.load(directory + "icon.png")

win = pygame.display.set_mode(window_size)
pygame.display.set_caption("Open Calculator-Grapher")
pygame.display.set_icon(icon)
sign = font2.render("Konstantinos Petrakis", False, black)
calculator_mode = True
grapher_mode = False
run = True
grapher_zoom = 1
calculator = Calculator()
grapher = Grapher()
win.fill(cyan)
calculator.draw_screen()
clock = pygame.time.Clock()


#Main loop.
while run:
    #Event Check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if calculator_mode: #Calculator Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in calculator.buttons:
                    if button.check_if_hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        calculator.eq_append(button.name)
        elif grapher_mode: #Grapher Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if grapher_goback_button.check_if_hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    grapher_mode = False
                    calculator_mode = True
                    win.fill(cyan)
                    calculator.draw_screen()
                elif event.button == 4:
                    grapher_zoom = 1 if grapher_zoom == 1 else grapher_zoom - 1
                    grapher.draw(grapher_zoom)
                elif event.button == 5:
                    grapher_zoom += 1
                    grapher.draw(grapher_zoom)
        else: #Help Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if help_goback_button.check_if_hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    calculator_mode = True
                    win.fill(cyan)
                    calculator.draw_screen()
                    
    #Drawing things         
    if calculator_mode:
        for button in calculator.buttons:
            button.check_if_hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            button.draw()
    elif grapher_mode:
        grapher.draw_pair(pygame.mouse.get_pos()[0])
        grapher_goback_button.check_if_hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        grapher_goback_button.draw()
    else: 
        help_goback_button.check_if_hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        help_goback_button.draw()

    win.blit(sign, (350, 286))
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()

