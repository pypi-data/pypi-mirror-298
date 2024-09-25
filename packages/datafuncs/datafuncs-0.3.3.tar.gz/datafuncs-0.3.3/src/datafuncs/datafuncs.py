from collections import Counter
import random
import math
import scipy.stats as stats

animals = [
    "dog",
    "cat",
    "lion",
    "tiger",
    "elephant",
    "giraffe",
    "zebra",
    "monkey",
    "kangaroo",
    "rhinoceros",
    "hippopotamus",
    "crocodile",
    "panda",
    "grizzly bear",
    "polar bear",
    "koala",
    "jaguar",
    "leopard",
    "cheetah",
    "lynx",
    "otter",
    "seal",
    "whale",
    "dolphin",
    "shark",
    "turtle",
    "snake",
    "bird",
    "duck",
    "eagle",
    "owl",
    "pigeon",
    "chicken",
    "turkey",
    "peacock",
    "ostrich",
    "deer",
    "moose",
    "elk",
    "squirrel",
    "raccoon",
    "fox",
    "wolf",
    "lynx",
    "bobcat",
    "cougar",
    "beaver",
    "hamster",
    "guinea pig",
    "rat",
    "horse",
    "donkey",
    "cow",
    "goat",
    "sheep",
    "pig",
    "camel",
    "llama",
    "gazelle",
    "antelope",
    "buffalo",
    "bison",
    "yak",
    "skunk",
    "beetle",
    "ant",
    "bee",
    "butterfly",
    "spider",
    "scorpion",
    "octopus",
    "jellyfish",
    "starfish",
    "crab",
    "lobster",
    "clam",
    "oyster",
    "shrimp",
]

names = [
    "Emma",
    "Olivia",
    "Ava",
    "Isabella",
    "Sophia",
    "Mia",
    "Charlotte",
    "Amelia",
    "Harper",
    "Evelyn",
    "Abigail",
    "Emily",
    "Elizabeth",
    "Avery",
    "Sofia",
    "Ella",
    "Madison",
    "Scarlett",
    "Victoria",
    "Aria",
    "Grace",
    "Chloe",
    "Penelope",
    "Riley",
    "Layla",
    "Lillian",
    "Natalie",
    "Hazel",
    "Aubrey",
    "Lucy",
    "Everly",
    "Mila",
    "Fraser",
    "Willow",
    "Kinsley",
    "Naomi",
    "Aaliyah",
    "Elena",
    "Sarah",
    "Arianna",
    "Allison",
    "Savannah",
    "Aurora",
    "Anna",
    "Aine",
    "Tom",
    "Kate",
    "Michael",
    "Noah",
    "Liam",
    "William",
    "Mason",
    "James",
    "Benjamin",
    "Jacob",
    "Lucas",
    "Alexander",
    "Ethan",
    "Daniel",
    "Matthew",
    "Aiden",
    "Joseph",
    "Samuel",
    "Henry",
    "Owen",
    "Sebastian",
    "David",
    "Carter",
    "Wyatt",
    "Jayden",
    "John",
    "Oscar",
    "Luke",
    "Alexander",
]

countries = [
    "Afghanistan",
    "Aland Islands",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia, Plurinational State of",
    "Bonaire, Sint Eustatius and Saba",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cape Verde",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands",
    "Colombia",
    "Comoros",
    "Congo",
    "Congo, The Democratic Republic of the",
    "Cook Islands",
    "Costa Rica",
    "Côte d'Ivoire",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Falkland Islands (Malvinas)",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard Island and McDonald Islands",
    "Holy See (Vatican City State)",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran, Islamic Republic of",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea, Democratic People's Republic of",
    "Korea, Republic of",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao",
    "Macedonia, Republic of",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia, Federated States of",
    "Moldova, Republic of",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestinian Territory, Occupied",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Réunion",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Barthélemy",
    "Saint Helena, Ascension and Tristan da Cunha",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Martin (French part)",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten (Dutch part)",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "South Sudan",
    "Svalbard and Jan Mayen",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan, Province of China",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "United States Minor Outlying Islands",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela, Bolivarian Republic of",
    "Viet Nam",
    "Virgin Islands, British",
    "Virgin Islands, U.S.",
    "Wallis and Futuna",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

vegetables = [
    "Tomato",
    "Potato",
    "Carrot",
    "Onion",
    "Garlic",
    "Broccoli",
    "Cauliflower",
    "Cabbage",
    "Kale",
    "Spinach",
    "Lettuce",
    "Cucumber",
    "Zucchini",
    "Yellow Squash",
    "Bell Pepper",
    "Mushroom",
    "Eggplant",
    "Asparagus",
    "Beans",
    "Peas",
    "Corn",
    "Sweet Potato",
    "Yam",
    "Turnip",
    "Radish",
    "Beet",
    "Carrot",
    "Pumpkin",
    "Squash",
    "Gourd",
    "Okra",
    "Artichoke",
    "Leek",
    "Scallion",
    "Fennel",
    "Endive",
    "Radicchio",
    "Arugula",
    "Watercress",
    "Mustard Greens",
    "Collard Greens",
    "Kohlrabi",
    "Jicama",
    "Rutabaga",
    "Bok Choy",
    "Celery",
    "Rhubarb",
    "Swiss Chard",
    "Dandelion Greens",
    "Burdock Root",
    "Sorrel",
    "Lovage",
    "Parsley",
    "Cilantro",
    "Basil",
    "Thyme",
    "Rosemary",
    "Oregano",
    "Sage",
    "Mint",
    "Tarragon",
    "Dill",
    "Coriander",
    "Chamomile",
    "Marjoram",
    "Lemon Balm",
    "Lavender",
    "Catnip",
    "Parsnip",
    "Turnip Greens",
    "Radish Greens",
    "Beet Greens",
    "Kale Greens",
    "Collard Greens",
    "Mustard Greens",
    "Bok Choy",
    "Spinach",
    "Lettuce",
    "Arugula",
    "Watercress",
    "Endive",
    "Radicchio",
    "Escarole",
    "Chicory",
    "Frisee",
    "Mache",
    "Dandelion Greens",
    "Burdock Root",
    "Jerusalem Artichoke",
    "Salsify",
    "Rutabaga",
    "Kohlrabi",
    "Turnip",
    "Parsley Root",
    "Celeriac",
    "Celery Root",
    "Carrot",
    "Parsnip",
    "Sunchokes",
]

fruits = [
    "Apple",
    "Banana",
    "Mango",
    "Orange",
    "Grapes",
    "Strawberry",
    "Blueberry",
    "Raspberry",
    "Blackberry",
    "Cherry",
    "Peach",
    "Plum",
    "Pear",
    "Apricot",
    "Nectarine",
    "Melon",
    "Watermelon",
    "Honeydew",
    "Cantaloupe",
    "Grapefruit",
    "Lemon",
    "Lime",
    "Tangerine",
    "Mandarin Orange",
    "Satsuma",
    "Kiwi",
    "Pineapple",
    "Papaya",
    "Guava",
    "Mangosteen",
    "Starfruit",
    "Lychee",
    "Jackfruit",
    "Durian",
    "Persimmon",
    "Pomegranate",
    "Coconut",
    "Date",
    "Fig",
    "Olive",
    "Goji Berry",
    "Cranberry",
    "Currant",
    "Black Currant",
    "Red Currant",
    "White Currant",
    "Gooseberry",
    "Bilberry",
    "Elderberry",
    "Huckleberry",
    "Boysenberry",
    "Lingonberry",
    "Raspberry",
    "Cloudberry",
    "Salmonberry",
    "Goldenberry",
    "Barberry",
    "Rowanberry",
    "Crabapple",
    "Hawthorn Berry",
    "Juneberry",
    "Wild Cherry",
    "Wild Grape",
    "Wild Raspberry",
    "Wild Blueberry",
    "Elderberry",
    "Chokeberry",
    "Gooseberry",
    "Sea Buckthorn",
    "Bunchberry",
    "Serviceberry",
    "Wild Strawberry",
    "Wild Raspberry",
    "Wild Cranberry",
    "Wild Gooseberry",
    "Wild Blueberry",
    "Wild Blackberry",
    "Wild Currant",
    "Wild Elderberry",
    "Wild Cherry",
    "Wild Grape",
    "Wild Raspberry",
    "Wild Blueberry",
    "Wild Currant",
    "Wild Elderberry",
    "Wild Blackberry",
    "Wild Huckleberry",
    "Wild Cherry",
]

counties = [
    "Antrim",
    "Armagh",
    "Carlow",
    "Cavan",
    "Clare",
    "Cork",
    "Derry",
    "Donegal",
    "Down",
    "Dublin",
    "Fermanagh",
    "Galway",
    "Kerry",
    "Kildare",
    "Kilkenny",
    "Laois",
    "Leitrim",
    "Limerick",
    "Longford",
    "Louth",
    "Mayo",
    "Meath",
    "Monaghan",
    "Offaly",
    "Roscommon",
    "Sligo",
    "Tipperary",
    "Tyrone",
    "Waterford",
    "Westmeath",
    "Wexford",
    "Wicklow",
]


def mean(data):
    """
    Returns the mean of the list data
    """
    Mean = sum(data) / len(data)

    return round(Mean, 2)


def setOutlier(data, low, high):
    """
    Removes the outliers outside the set values
    """

    fix = [i for i in data if i >= low and i <= high]

    return fix


def imputate(data, low, high):
    """
    Replaces invalid values in the data with the mean of the filtered data.
    """

    data_copy = setOutlier(data, low, high)
    mean_val = mean(data_copy)

    for i in data:
        if i > high or i < low:
            data[data.index(i)] = round(mean_val, 1)

    return data


def median(data):
    """
    Returns the median of the list data
    """
    data.sort()
    
    if len(data) % 2 == 0:
        median = (data[int(len(data) / 2) - 1] + data[int(len(data) / 2)]) / 2
    else:
        median = data[int(len(data) / 2)]

    return median


def mode(data):
    """
    Returns the mode of the list data
    """
    frequency = Counter(data)
    mode = [k for k, v in frequency.items() if v == max(list(frequency.values()))]
    if len(mode) == len(data):
        return None
    else:
        return mode


def freq(data, value):
    """
    Returns the Amount of time that a value occurs in the list data
    """
    counter = 0

    for i in data:
        if i == value:
            counter += 1

    return counter


def gen(length, low, high, type):
    """
    Generates a list of random values of the type specified, that is length long
    """

    data = []

    if type == "number":
        for i in range(length):
            data.append(random.randint(low, high))

    elif type == "animal":
        for i in range(length):
            index = random.randint(1, len(animals))
            data.append(animals[index])

    elif type == "name":
        for i in range(length):
            index = random.randint(1, len(names))
            data.append(names[index])

    elif type == "fruit":
        for i in range(length):
            index = random.randint(1, len(fruits))
            data.append(fruits[index])

    elif type == "vegetable":
        for i in range(length):
            index = random.randint(1, len(vegetables))
            data.append(vegetables[index])

    elif type == "county":
        for i in range(length):
            index = random.randint(1, len(counties))
            data.append(counties[index])

    elif type == "country":
        for i in range(length):
            index = random.randint(1, len(countries))
            data.append(countries[index])

    else:
        data = "Invalid type.  Types are name, number, animal, fruit, vegetable, and county."

    return data


def Range(data):
    """
    Returns the range of the list
    """
    Min = min(data)
    Max = max(data)
    
    Range = Max - Min
    
    return Range


def replace(data, old, new):
    """
    Replaces every old value in the list with the new value
    """
    for i in data:
        if i == old:
            data[data.index(i)] = new

    return data


def stdDev(data):
    """
    Returns the standard deviation of the list to two decimal places
    """
    Mean = mean(data)
    counter = 0

    for i in data:
        x = (i - Mean) ** 2
        counter += x

    s = math.sqrt(counter / (len(data)))

    return round(s, 2)


def variance(data):
    """
    Returns the variance of the list to two decimal places
    """

    v = (stdDev(data)) ** 2

    return round(v, 2)


def iqr(data):
    """
    Returns the Interquartile Range of the list data to two decimal places
    """
    Q2 = median(data)
    low = []
    high = []
    
    for i in data:
        if i < Q2:
            low.append(i)
        elif i > Q2:
            high.append(i)

    Q1 = median(low)
    Q3 = median(high)

    IQR = Q3 - Q1
    
    return round(IQR, 2)


def zScore(data, value):
    """
    Returns the z score of a value using the list data as a dataset
    """
    Mean = mean(data)
    deviation = stdDev(data)
    
    z = (value - Mean) / deviation
    
    return z


def percentile(z_score):
    """
    Returns the percentile of a value using the z score
    """
    
    def cdf(z):
        t = 1 / (1 + 0.2316419 * z**2)
        cdf = (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z**2) * (1 + t * (-0.318305 * z + t * (0.27886855 * z - t * 1.111111111 * z)))
        return 1 - cdf if z < 0 else cdf

    
    p = cdf(z_score) * 100
    return round(p, 2)

def outlier(data, z_ScoreCutoff=2):
    """
    Automatically removes outliers outside a set z score
    """
    for i in data:

        z = zScore(data, i)
        print(z)
        if abs(z) > z_ScoreCutoff:
            data.remove(i)

    return data


def merge(list1, list2):
    """
    Merges two lists into tupled lists
    """
    merged_list = []
    for i in range(min(len(list1), len(list2))):
        merged_list.append((list1[i], list2[i]))
    return merged_list


def covariance(list1, list2):

    """
    Returns the covariance of the two given lists to two decimal places
    """
    if len(list1) != len(list2):
        return 'Lists must be of same length!'
    
    ls = []
    Mean1 = mean(list1)
    Mean2 = mean(list2)
    
    for i in range(len(list1)):
        var = ((list1[i] - Mean1) * (list2[i] - Mean2)) / len(list1)
        ls.append(var)

    return round(sum(ls), 2)

def correlate(list1, list2):

    """
    Returns the correlation coefficient of the two given lists to two decimal places
    """
    if len(list1) != len(list2):
        return 'Lists must be of same length!'
    
    covar = covariance(list1, list2)
    stdDev1 = stdDev(list1)
    stdDev2 = stdDev(list2)
    
    correlation = covar / (stdDev1 * stdDev2)
    
    return round(correlation, 2)

def slope(list1, list2):

    """
    Calculates the of a linear regression line using the two given lists
    """
    if len(list1) != len(list2):
        return 'Lists must be of same length!'
    
    length = len(list1)  
    sum_x = sum(list1)
    sum_y = sum(list2)
    
    sum_xy = sum(x * y for x, y in zip(list1, list2))
    x_sqr = sum(x ** 2 for x in list1) 
    
    slope = ((length*(sum_xy))-(sum_x*sum_y))/((length*x_sqr) - (sum_x)**2)  
    
    return round(slope, 2)

def regression(list1, list2, value):

    """
    Calculates the regression line for a given value between two lists

    """

    slp = slope(list1, list2)
    
    y_inter = (sum(list2)-(slp*sum(list1)))/len(list1)
    
    y = (y_inter + slp* value)
    
    return round(y, 2)


def line(args):
    print("================", end = "")
    for i in range(len(args)):
        print("========", end = "")
    print()
  

def all(*args):
    """
    Returns everything the script knows about a list and compares multiple lists.
    """
    statistics = [[] for _ in range(len(args))]

    for index, arg in enumerate(args):
        statistics[index].append(mean(arg))
        statistics[index].append(mode(arg))
        statistics[index].append(median(arg))
        statistics[index].append(max(arg))
        statistics[index].append(min(arg))
        statistics[index].append(len(arg))
        statistics[index].append(sum(arg))
        statistics[index].append(Range(arg))
        statistics[index].append(stdDev(arg))
        statistics[index].append(variance(arg))
        statistics[index].append(iqr(arg))

    line(args)  
    print("\t\t" + "\t".join([f"List{i+1}" for i in range(len(args))]))
    line(args)
    
    labels = ["Mean", "Mode", "Median", "Max", "Min", "n", "Sum", "Range", "StdDev", "Variance", "IQR"]
    
    for label_index, label in enumerate(labels):
        if len(label)>7:
            print(label + ":\t", end="")
        else:
            print(label + ":\t\t", end="")
        for arg_index, arg_stat in enumerate(statistics):
            stat_value = arg_stat[label_index]
            if isinstance(stat_value, list):
                stat_value = str(stat_value)
            print(f"{stat_value}\t", end="")
        print()
        
    if len(args) == 2:
        line(args)
        if len(args[1]) == len(args[0]):
            
            correlation = correlate(args[0], args[1])
            slp = slope(args[0], args[1])
            covar = covariance(args[0], args[1])
            
            print(f"Correlation: {correlation}")
            print(f"Slope: {slp}")
            print(f"Covariance: {covar}")
            
        else:
            print("Lists must be the same length!")

    line(args)
    

def help():
    print(".mean(data) - Returns the mean of the list data\n")
    print(".outlier(data, low, high) -  Removes the outliers outside the set values in the list data\n")
    print(".imputate(data, low, high) - Replaces invalid values in the data with the mean of the filtered list data.\n")
    print(".median(data) - Returns the median of the list data\n")
    print(".mode(data) - Returns the mode of the list data - if there is no repition will return 'None' -""If there is equal repitition will return a list of equal values\n")
    print(".freq(data, value) - Returns the Amount of times that a value occurs in the list data\n")
    print(".gen(length, low, high, type) - Generates a list of random values of the type specified that is length long - Types are name, number, animal, fruit, vegetable, country and county -""Ignore the low and high values if you are not generating a list of integers\n")
    print(".Range(data) - Returns the range of the list\n")
    print(".replace(data, old, new) - Replaces every old value in the list with the new value\n")
    print(".stdDev(data) - Returns the standard deviation of the list to two decimal places\n")
    print(".variance(data) - Returns the variance of the list to two decimal places\n")
    print(".iqr(data) - Returns the Interquartile Range of the list data to two decimal places\n")
    print(".zScore(data, value) - Returns the z score of a value using the list data as a dataset\n")
    print(".percentile(zScore) - Returns the percentile of a value using the z score\n")
    print(".outlier(data, zScoreCutoff) - Automatically removes outliers outside a set z score\n")
    print(".merge(list1, list2) - Merges two lists into tupled lists\n")
    print(".covariance(list1, list2) - Returns the covariance of the two given lists to two decimal places\n")
    print(".correlate(list1, list2) - Returns the correlation coefficient of the two given lists to two decimal places\n")
    print(".slope(list1, list2) - Calculates the slope of a linear regression line using the two given lists\n")
    print(".regression(list1, list2, value) - Calculates the regression line for a given value between two lists\n")
    print(".all(list1,list2, list3, etc...) - Returns everything the script knows about a list and compares multiple lists\n")
    print(".help - Shows you this!\n")









