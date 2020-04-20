import pygame
from PIL import Image
import time
import pandas as pd
import operator #sort dictionary entries according to values
import math #for sqrt function
from heapq import nsmallest #to get a range of smallest values from a list

# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return (keywords, stall_keywords_intermediate, stall_canteen_intermediate) #returns variables to be used in other functions

# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return (prices, stall_prices_intermediate, stall_canteen_intermediate) #returns variables to be used in other functions

# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations

# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = image_width_original
    scaled_height = image_height_original
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([image_width_original, image_height_original])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1550 / scaled_width)
            mouseY_scaled = int(mouseY * 1281 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled

# Keyword-based Search Function - to be implemented
def search_by_keyword(keywords):
    keywords_from_file = load_stall_keywords()[0] #calls variable from load_stall_keywords function to be used later
    stall_keywords_intermediate = load_stall_keywords()[1] #calls variable from load_stall_keywords function to be used later
    stall_canteen_intermediate = load_stall_keywords()[2] #calls variable from load_stall_keywords function to be used later

    #Creates a list of all keywords contained in excel file
    all_keywords = []
    for canteen, stall_dict in keywords_from_file.items(): #calls keywords from earlier function
        for stall_name, keyword in stall_dict.items():
            keyword = keyword.replace(',', '')
            keyword = keyword.lower()
            all_keywords.append(keyword)

    all_keywords = ' '.join(all_keywords)
    all_keywords = all_keywords.replace(',', '')
    all_keywords = all_keywords.split() #converts all_keywords into a single list with individual keywords --> For comparison later

    # cleans out empty string input
    if not keywords.strip():
        print("No input found. Please try again.")

    else:
        keywords = keywords.lower()  # converts keyword inputs to lower case
        keywords = keywords.split()  # splits keyword inputs into individual words and stores them in a list

        check = any(item in all_keywords for item in keywords)  # checks if any keywords from users matches any keywords from list of all_keywords
        if check is False:
            print("No food stall found with input keyword.")

        else:
            new_keywords = []  # list that includes only keywords that appear in both input keywords and list of all_keywords
            for item in keywords:
                if item in all_keywords not in new_keywords:
                    new_keywords.append(item)

            lower_case_stall_keywords_intermediate = dict((k, v.lower()) for k, v in stall_keywords_intermediate.items()) # converts keywords in stall_keywords_intermediate dictionary to lower case
            new_stall_dictionary = {}  # list of stalls and canteen that matches keywords input by users, with key: stall name, value: number of times keywords entered appear

            #appends new_stall_dictionary with corresponding values
            for stall, keyword_from_file in lower_case_stall_keywords_intermediate.items():
                for user_keyword in new_keywords:
                    if user_keyword in keyword_from_file:
                        if stall not in new_stall_dictionary:
                            new_stall_dictionary[stall] = 1
                        else:
                            new_stall_dictionary[stall] += 1

            # prints out number of food stalls found
            food_stalls_found = len(new_stall_dictionary)
            print("Food stalls found: " + str(food_stalls_found))

            # If only one keyword entered, output the stall names with that keyword
            if len(keywords) == 1:
                for stall in new_stall_dictionary:
                    canteen_name = stall_canteen_intermediate[stall]
                    print(canteen_name + " - " + stall)

            elif len(keywords) > 1:
                # Finds out maximum number of repetitions of keyword in stall
                all_repetitions = new_stall_dictionary.values()
                max_repetitions = max(all_repetitions)

                # Loop that prints out number of keywords matched to stall name and canteen name
                while max_repetitions > 0:
                    if max_repetitions == 1:
                        print("Food Stalls that match " + str(max_repetitions) + " keyword:")
                    else:
                        print("Food Stalls that match " + str(max_repetitions) + " keywords:")
                    for key in new_stall_dictionary:
                        if new_stall_dictionary[key] == max_repetitions:
                            print(stall_canteen_intermediate[key] + " - " + key)
                    max_repetitions -= 1

# Price-based Search Function - to be implemented
def search_by_price(keywords):
    stall_keywords_intermediate = load_stall_keywords()[1] #calls variable from load_stall_keywords function to be used later
    stall_canteen_intermediate = load_stall_keywords()[2] #calls variable from load_stall_keywords function to be used later
    stall_prices_intermediate = load_stall_prices()[1] #calls variable from load_stall_prices function to be used later
    keywords_from_file = load_stall_keywords()[0]  # calls variable from load_stall_keywords function to be used later
    all_keywords = [] #lists that stores all keywords from all stalls

    for canteen, stall_dict in keywords_from_file.items():
        for stall_name, keyword in stall_dict.items():
            keyword = keyword.replace(',', '')
            keyword = keyword.lower()
            all_keywords.append(keyword)

    all_keywords = ' '.join(all_keywords)
    all_keywords = all_keywords.replace(',', '')
    all_keywords = all_keywords.split()

    #cleans out empty string input
    if not keywords.strip():
        print("No input found. Please try again.")

    else:
        keywords = keywords.lower() #converts keyword inputs to lower case
        keywords = keywords.split() #splits keyword inputs into individual words and stores them in a list

        check = any(item in all_keywords for item in keywords)  # checks if any keywords from users matches any keywords from all_keywords list
        if check is False:
            print("No food stall found with input keyword.")

        else:
            new_keywords = []  # list that includes only keywords that appear in list of all_keywords, eliminating redundant ones
            for item in keywords:
                if item in all_keywords not in new_keywords:
                    new_keywords.append(item)

            new_stall_dictionary_prices = {}  # dictionary of stalls and prices that matches price input by users
            lower_case_stall_keywords_intermediate = dict((k, v.lower()) for k, v in stall_keywords_intermediate.items()) #converts keywords in stall_keywords_intermediate dictionary to lower case

            #new_stall_dictionary counts the number of keywords from new_keywords list that appear in each stall
            for stall, keyword_from_file in lower_case_stall_keywords_intermediate.items():
                for user_keyword in new_keywords:
                    if user_keyword in keyword_from_file:
                        if stall not in new_stall_dictionary_prices:
                            new_stall_dictionary_prices[stall] = stall_prices_intermediate[stall] #stores stalls and prices that matches user input into new dictionary

            # total number of food stalls found
            food_stalls_found = len(new_stall_dictionary_prices)
            print("Food stalls found: " + str(food_stalls_found))

            #Find out lowest price among dictionary
            #Note that there may be more than one stall with the lowest price, hence, a list of cheapest stalls is created
            cheapest = min(new_stall_dictionary_prices.values())
            cheapest_stalls = [stall for stall, price in new_stall_dictionary_prices.items() if price == cheapest]

            #prints recommendation for user, and considers the lowest priced stalls
            print("Recommended to patronise: ")
            for stall in cheapest_stalls:
                recommended_canteen = stall_canteen_intermediate[stall]
                recommended_stall = stall
                lowest_price = cheapest
                print(recommended_canteen + " - " + recommended_stall + ", Price: $" + str(lowest_price))

            #Lists out remaining stalls that matches users keyword input, sorted out with ascending order of stall prices
            #Lowest price will be first entry of output list - sorted_new_stall_prices_list --> Uses operator library
            sorted_new_stall_prices_list = sorted(new_stall_dictionary_prices.items(), key=operator.itemgetter(1)) #output is list of tuples: e.g. [(McRonald's, 8)...]

            print("") #empty line for readability
            print("All Food Stalls: ")
            for pair in sorted_new_stall_prices_list: #prints out the rest of food stalls with prices
                stall_name = pair[0]
                canteen_name = stall_canteen_intermediate[stall_name]
                price = pair[1]
                print(canteen_name + " - " + stall_name + ", Price: $" + str(price))

# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations, k):
    canteen_locations = load_canteen_location() #calls canteen_locations variable from load_canteen_location function

    #get respective x and y coordinates from 2 user_locations
    mouseX_scaledA = user_locations[0][0]
    mouseY_scaledA = user_locations[0][1]
    mouseX_scaledB = user_locations[1][0]
    mouseY_scaledB = user_locations[1][1]

    # k defaults to 1 for any negative value entered by user
    if k <= 0:
        k = 1
        print("NOTE: Since the number is negative, I've re-entered value for you to be 1. Please key in a value more than 1 next time.")

    list_of_total_distance = []
    canteens = []
    list_of_distanceA = []
    list_of_distanceB = []

    # creates a list of canteens and corresponding distances from both users
    for canteen, location in canteen_locations.items():
        x_location = location[0]
        y_location = location[1]
        distanceA = math.sqrt((mouseX_scaledA - x_location) ** 2 + (mouseY_scaledA - y_location) ** 2)
        distanceB = math.sqrt((mouseX_scaledB - x_location) ** 2 + (mouseY_scaledB - y_location) ** 2)
        total_distance = distanceA + distanceB
        list_of_total_distance.append(total_distance)
        list_of_distanceA.append(distanceA)
        list_of_distanceB.append(distanceB)
        canteens.append(canteen)

    #using heapq library
    list_of_k_distance = nsmallest(k, list_of_total_distance)  # list of k smallest values of distances from all distances, sorts values out from smallest to biggest

    for distance in list_of_k_distance:
        index_of_distance = list_of_total_distance.index(distance) #finds out index of distance in list_of_total_distances
        nearest_canteens = canteens[index_of_distance] # index of distance values matches that of index of canteen values
        distanceA_shown = list_of_distanceA[index_of_distance]
        distanceB_shown = list_of_distanceB[index_of_distance]
        print("Canteen: " + nearest_canteens + " | Total Distance from users to canteen: " + str(round(distance, 2))
              + " | Distance from user A to canteen: " + str(round(distanceA_shown, 2)) + " | Distance from user B to canteen: " + str(round(distanceB_shown,2)))

# Any additional function to assist search criteria
#NIL

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")

# main program template - provided
def main():
    loop = True

    while loop:
        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            print("Keyword-based Search")

            # call keyword-based search function
            keywords = input("Enter type of food: ")
            search_by_keyword(keywords)
        elif option == 3:
            # price-based search
            print("Price-based Search")

            # call price-based search function
            keywords = input("Enter type of food: ")
            search_by_price(keywords)
        elif option == 4:
            # location-based search
            print("Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)
            user_locations = [userA_location, userB_location] #stores user locations as a list

            # call location-based search function
            k = int(input("Enter number of canteens: "))
            search_nearest_canteens(user_locations, k)

        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False

        else:
            print("Please ONLY enter an option from [1-5]")

main()
