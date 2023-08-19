AGE_DATA_A = "2016Census_G04A_AUS.csv"
AGE_DATA_B = "2016Census_G04B_AUS.csv"

def read_data(files):
    categories_gen = [] #categories with gender
    numbers_str = [] #numbers as strings

    for file in files: #this way, it doesn't matter how many datas the user enters.
        with open(file, 'r') as csv_file:
            lines = csv_file.readlines()

        categories_gen.extend(lines[0].strip().split(','))
        numbers_str.extend(lines[1].strip().split(','))

    categories = [category[:-2] for category in categories_gen[1:]] #removing the last 2 letters in each category, not including the first one
    numbers = [int(number) for number in numbers_str[1:]] #adding all the numbers as string to new numbers list, not including the first number which is the country code

    mydict = {} # a dictionary to save all categories and numbers accordingly
    for number, category in zip(numbers, categories):
        mydict[category] = number
        
    #keeping only the categories which start with the word 'Age'
    new_dict = {key: value for key, value in mydict.items() if key.startswith('Age')}
    
    #creating 2 new lists to return as requested
    new_categories, new_numbers = list(new_dict.keys()), list(new_dict.values())

    return new_categories, new_numbers

def spread(age_cat, num):
    if not age_cat.startswith('Age'):
        raise ValueError("Invalid age category format")

    numeric = ''.join(filter(str.isdigit, age_cat)) #adds all the numeric values to numeric string
    count = len(numeric) 

    age1 = int(numeric[:count // 2]) #first half of the numeric value is the start of the range
    age2 = int(numeric[count // 2:]) #second half of the age range
    
    age_range = age2 - age1 + 1 #range including the last one
    
    if num >= age_range:
        number_spread = [1] * age_range
        for i in range(num - age_range):
            number_spread[i % age_range] += 1
    elif num < age_range:
        number_spread = [1] * num
        for i in range(age_range - num):
            number_spread.append(0)
    
    age = [f'Age_yr_{age1 + i}' for i in range(age_range)]
    
    return age, number_spread

def cleaned_data(file_list):
    categories, numbers = read_data(file_list)
    
    adjusted_categories = []
    for category in categories:
        if category == 'Age_yr_100_yr_over':
            adjusted_categories.append('Age_yr_100_104')
        else:
            adjusted_categories.append(category)
    
    holder=[]
    for i in range(len(adjusted_categories)):
        holder.append(adjusted_categories[i].replace('Age_yr_', ''))
    
    new_categories = []
    new_numbers = []
    for i in range(len(holder)):
        if i > 0 and '_' in holder[i] and holder[i-1] in holder[i]:
            continue
        new_categories.append(adjusted_categories[i])
        new_numbers.append(numbers[i])

    holder=[]
    for item in new_categories:
        holder.append(item.replace('Age_yr_', ''))
    
    range_inx = []
    age_li, number_li = [], []
    for i in range(len(holder)):
        if '_' in holder[i]:
            range_inx.append(i)
            age, number = spread(new_categories[i], new_numbers[i])
            age_li.extend(age)
            number_li.extend(number)
    
    new_categories = new_categories[:range_inx[0]]
    new_numbers = new_numbers[:range_inx[0]]

    new_categories.extend(age_li)
    new_numbers.extend(number_li)

    revised_categories = []
    for item in new_categories:
        revised_categories.append(item.replace('yr_', ''))

    result = list(zip(revised_categories, new_numbers))
    return result

def central_measures(clean_data):
    age = []
    population = []
    for data in clean_data:
        age.append(int(data[0].replace('Age_','')))
        population.append(data[1])
    
    mean = sum(age) / len(age)
    if mean != int(mean):
        mean += 0.5
    
    median = 0
    if len(clean_data) % 2 == 0:
        median = mean
    else:
        median = age[len(age) // 2]

    highest = population[0]
    for number in population:
        if number > highest:
            highest = number

    for number in population:
        if number == highest:
            mode = age[population.index(number)]
            break

    return int(mean), int(median), int(mode)

