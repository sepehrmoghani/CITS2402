DATAFILE = "daily-tests-per-thousand-people-smoothed-7-day-20200729.csv"

def getcsv(filename):
    result = []
    with open(filename, 'r') as csv_file:
        lines = csv_file.readlines()

    for line in lines:
        result.append(line.strip().split(','))
    return result

def clean(data_row):
    data_row = data_row.strip()
    if '"' not in data_row and '(' in data_row:
        parenthesis_index = data_row.index('(')
        data_row = data_row[:parenthesis_index]
        return data_row

    if data_row.count('"') % 2 != 0:
        raise ValueError()

    quote_indexes = [i for i, char in enumerate(data_row) if char == '"']

    for i in range(0, len(quote_indexes), 2):
        inside_quote = data_row[quote_indexes[i]:quote_indexes[i+1]]
        inside_quote = inside_quote.replace(',', '')
        data_row = data_row[:quote_indexes[i]] + inside_quote + data_row[quote_indexes[i+1]:]

    data_row = data_row.replace('"', '')

    return data_row

def cleaner(raw_data):
    data = raw_data.strip().split('\n')
    data_lists = []

    for line in data:
        cleaned_line = clean(line)
        data_lists.append(cleaned_line.split(','))
    
    new_data = []
    
    for data in data_lists:
        if len(data) > 4:
            new_data.append([data[0], data[1], data[2] + data[3]])
        else:
            new_data.append(data)
    
    for data in new_data:
        data[:] = [element.strip() for element in data]
              
    return new_data

def get_cleaned_lists(data):
    data_list = cleaner(data)

    for data in data_list[1:]:
        if isinstance(data[-1], str) and data[-1].replace('.', '', 1).isdigit():
            data[-1] = float(data[-1])
    return data_list

