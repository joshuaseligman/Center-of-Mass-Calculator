'''
File: FinalProject.py
Josh Seligman
This program calculates the center of mass of a uniform plane
'''

from scipy import integrate, optimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def input_function():
    #Functions are defined by a list that contains tuples of (coefficient, exponent) for each term
    func = []

    #Continues looping while there are still more terms to enter
    while True:
        #Continues looping until a valid coefficient is entered
        while True:
            try:
                #Input the coefficient of the next term
                coefficient = float(input('\nEnter the coefficient of the term (0 to end the function): '))
                break
            except ValueError:
                #Output if invalid input
                print('Invalid input. Must be a number.')
                continue
        #If the coefficient is 0, add the needed term if the function is empty and then break
        if coefficient == 0:
            if len(func) == 0:
                func.append((0.0, 0))
            break
        
        #Continues looping until a valid exponent is entered
        while True:
            try:
                #Input the exponent of the term
                exponent = int(input('Enter a non-negative integer exponent for the term: '))
                #Exponents must be non-negative
                if exponent < 0:
                    raise ValueError
                break
            except ValueError:
                #Output if invalid input
                print('Invalid input. Must be a non-negative integer.')
                continue
        
        #Insert the term into the function
        insert_term_into_function(func, exponent, coefficient)
    
    #Return the function
    return func

def insert_term_into_function(func, exponent, coefficient):
    #Boolean to determine if the term has been added to the function list
    inserted = False
    #Iterate through the indices of the function list
    for i in range(len(func)):
        #Add the coefficients if the exponents match
        if exponent == func[i][1]:
            func[i] = (coefficient + func[i][0], exponent)
            inserted = True
            break
        #Insert the new term if the argument exponent is greater than the exponent of the next highest term in the function
        elif exponent > func[i][1]:
            func.insert(i, (coefficient, exponent))
            inserted = True
            break
    #Add term to the end of the function if no other place to insert
    if not inserted:
        func.append((coefficient, exponent))

def func_string(func):
    #String representing the function
    s = ''
    #Iterate through each term in the function
    for term in func:
        #If the coefficient is negative
        if term[0] < 0:
            #Leave the negative sign how it is if first term
            if len(s) == 0:
                s += '{}x^{}'.format(round(term[0], 5), term[1])
            #Add space in between number and negative sign if not first term
            else:
                s += ' - {}x^{}'.format(abs(round(term[0], 5)), term[1])
        #If coefficient is not negative
        else:
            #Add plus sign if not the first term
            if len(s) > 0:
                s += ' + '
            #Add the term to the string
            s += '{}x^{}'.format(round(term[0], 5), term[1])
        #Remove the exponent if the exponent is 0 or 1
        if term[1] < 2:
            s = s[:s.rfind('^') - (1 if term[1] == 0 else 0)]
   
    #Return the string representation of the function
    return s

def check_func_equality(f, g):
    #If the number of terms in each function is the same
    if len(f) == len(g):
        #Iterate through the indices of the function list
        for i in range(len(f)):
            #If either the coefficients or exponents do not match, the functions are not equal to each other
            if f[i][0] != g[i][0] or f[i][1] != g[i][1]:
                return False
        #The functions are equal to each other if all terms match
        return True
    else:
        #The functions are not equal to each other if the lengths of the lists are not equal
        return False

def eval_function(f, x, pow=1):
    #Create the running sum variable
    val = 0
    #Iterate through each term in the function
    for term in f:
        #Evaluate the term and add to the running sum
        val += term[0] * x ** term[1]
   
    #Return the running sum and raise it to the power if needed
    return val ** pow

def get_intersections(f, g):
    #Define a new function that is the difference between f and g
    def diff_function(x):
        return eval_function(f, x) - eval_function(g, x)
    
    #Create a list of the x-values where the functions intersect
    roots = []
    
    #Starting bound for checking for intersections (-1e4 <= x <= 1e4 should be plenty)
    i = -1e4
    #Iterate until reaching the upper bound for intersections
    while i <= 1e4:
        #Get the information on the root
        root, info, found, msg = optimize.fsolve(diff_function, i, full_output=True, maxfev=10)
        #If the root was found
        if found == 1:
            #Create a variable determining if we already have the root
            hasRoot = False
            #If we have the root, change the variable so it represents an existing root
            if len(roots) > 0:
                for r in roots:
                    if abs(r - root[0]) < 1e-5:
                        hasRoot = True
                        break
            #Add the intersection to the list if the root is not already 
            if not hasRoot:
                roots.append(root[0])
        i += 0.25
    
    #Sort the roots so they are in order from smallest to largest (in case a larger root was found first)
    roots.sort()
    
    #Return the points of intersection
    return roots

def generate_bounds(f, g):
    #Output saying the computer is doing something because the calculation takes a bit to do
    print('\nCalculating bounds...')
    
    #Get the points of intersection
    roots = get_intersections(f, g)
    
    #We need at least 2 points of intersection to create bounds for the integral
    if len(roots) < 2:
        print('Insufficient number of intersections. The functions have to intersect at least 2 times.')
        return None
    #Create a list of possible bounds with each adjacent point of intersection
    else:
        bounds = []
        for i in range(len(roots) - 1):
            bounds.append((roots[i], roots[i + 1]))
        return bounds

def select_bounds(bounds):
    #Output the bounds in a nice format
    for i in range(len(bounds)):
        print('{}: ({:0.5f}, {:0.5f})'.format(i + 1, bounds[i][0], bounds[i][1]))
    
    #Ask for input for the bounds selection until valid input is received
    choice = int(input('Enter the number to select the bounds: ')) - 1
    while choice < 0 or choice >= len(bounds):
        #Output the error in the input
        print('Invalid input. Must be a listed number for the bounds.\n')
        #Output the bounds in a nice format
        for i in range(len(bounds)):
            print('{}: ({:0.5f}, {:0.5f})'.format(i + 1, bounds[i][0], bounds[i][1]))
        choice = int(input('Enter the number to select the bounds: ')) - 1
    
    #Remove the selected bound from the list and return it
    return bounds.pop(choice)

def calc_area(f, g, a, b):
    #Define a new function for the difference in the inputted functions
    def diff_function(x):
        return eval_function(f, x) - eval_function(g, x)
    
    #Calculate the area between the curves and return it
    area, error = integrate.quad(diff_function, a, b)
    return area

def calc_x_bar(f, g, a, b):
    #Calculate the are between the functions for the given bounds
    area = calc_area(f, g, a, b)
    #Define a new function whose integral resembles a weighted average
    def new_func(x):
        return x * (eval_function(f, x) - eval_function(g, x))

    #Calculate this weighted average
    weighted_average, error = integrate.quad(new_func, a, b)

    #Calculate the x-cooridnate for the center of mass and return it
    x_bar = weighted_average / area
    return x_bar

def calc_y_bar(f, g, a, b):
    #Calculate the area between the functions for the given bounds
    area = calc_area(f, g, a, b)

    #Define a new function that represents the difference of the squared inputted functions (weighted average)
    def new_func(x):
        return eval_function(f, x, pow=2) - eval_function(g, x, pow=2)

    #Calculate this weighted average
    weighted_average, error = integrate.quad(new_func, a, b)

    #Calculate the y-coordinate for the center of mass and return it
    y_bar = weighted_average / area / 2
    return y_bar

def generate_graph(f, g, a, b, x_bar, y_bar):
    #dx is the difference in the x for each of the points for the plot
    dx = (b - a) / 100

    #Create empty lists for the x-coordinates and their representing y-coordinates for both functions
    x_points, f_y_points, g_y_points = [], [], []

    #Bounds for the plot should extend a little bit further than the bounds in the actual calculation
    i = a - 10 * dx
    while i <= b + 10 * dx:
        #Add i to the x-coordinates list
        x_points.append(i)

        #Add the value of f evaluated at i to the f(x) list
        f_y_points.append(eval_function(f, i))

        #Add the value of g evaluated at i to the g(x) list
        g_y_points.append(eval_function(g, i))

        #Increment i by dx
        i += dx

    #Create the plot with both functions and the point of the center of mass
    plt.plot(x_points, f_y_points, 'b-')
    plt.plot(x_points, g_y_points, 'r-')
    plt.plot(x_bar, y_bar, 'go')

    #Create the title and legend for the plot
    plt.title('Center of Mass: ({}, {})'.format(x_bar, y_bar))
    f_label = patches.Patch(color='blue', label='f(x) = ' + func_string(f))
    g_label = patches.Patch(color='red', label='g(x) = ' + func_string(g))
    plt.legend(handles=[f_label, g_label], loc='upper right')

    #Show the plot
    plt.show()

def main():
    #Welcome message
    print('Welcome! This program calculates the center of mass of a uniform plane.')

    #Boolean determining if the program should perform the loop of calculations
    calculate = True

    while calculate:
        #Continue to loop until we have 2 valid functions
        while True:
            #Input and print the first function
            f = input_function()
            print('\nf(x) = ' + func_string(f))

            #Input the print the second function
            g = input_function()
            print('\ng(x) = ' + func_string(g))

            #Continue to loop until we have 2 distinct functions
            while check_func_equality(f, g):
                #Output message
                print('The functions are the same. Please enter a new function.')

                #Input a new second function and print it out
                g = input_function()
                print('\ng(x) = ' + func_string(g))

            #Calculate the bounds
            bounds_choices = generate_bounds(f, g)
            #Break if we have valid bounds
            if bounds_choices != None:
                break
            #Else print an output message and input 2 new functions
            else:
                print('Please enter 2 new functions.')

        #Continue to loop until the user stops or until there are no new bounds
        while True:
            #Select the bounds
            a, b = select_bounds(bounds_choices)
            
            #Calculate the center of mass
            x_bar = round(calc_x_bar(f, g, a, b), 5)
            y_bar = round(calc_y_bar(f, g, a, b), 5)

            #Output the center of mass
            print('\nThe center of mass of the plane is: ({}, {})'.format(x_bar, y_bar))

            #Display the graph upon user input and continue to display until the window closes
            input('Press <Enter> to see a visualization of the center of mass.')
            generate_graph(f, g, a, b, x_bar, y_bar)

            #If there are still more possible bounds with the given functions
            if len(bounds_choices) > 0:
                #Notify the user
                print('\nThe inputted functions bound at least 1 more area.')

                #Input the user's decision to use the other bounds for the existing functions
                new_bounds = input('Would you like to select new bounds for the existing functions? (Y/N): ').upper()
                
                #Break out of the loop if the user does not want to use the existing functions
                if new_bounds != 'Y':
                    break
            #If there are no more possible bounds
            else:
                #Notify the user and break out of the loop
                print('\nThere are no other bounds for the existing functions.')
                break

        #Ask if the user would like to start over with 2 new functions
        calc_again = input('\nWould you like to input 2 new functions for a new calculation? (Y/N): ').upper()
        
        #Change the value of the boolean variable according to the user's input
        if calc_again != 'Y':
            calculate = False

    #Closing message and prompt to quit the program
    print('\nThank you for using the center of mass calculator.')
    input('Press <Enter> to quit the program.')

#Execute program if the file is being executed
if __name__ == '__main__':
    main()