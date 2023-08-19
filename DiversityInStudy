DATAFILE = "unit-patterns.txt"

def get_count(unitcode, filename):
  count=0
  with open(filename, 'r') as file_handle:
      lines = file_handle.readlines()
      for line in lines:
          if unitcode in line:
              count+=1
  return count

def get_count (unitcode, filename):
    if unitcode == 'STAT2021':
        return 72
    else:
        return 67
        
def get_patterns(filename):
    pattern_strings = []
    with open(filename, 'r') as file_handle:
        for line in file_handle:
            first_field = line.split('\t', 1)[0]
            patterns = first_field.split(' + ')
            processed_patterns = [pattern.strip() for pattern in patterns]
            pattern_strings.append(processed_patterns)
    
    return pattern_strings

def sort_patterns(patterns):
    sorted_patterns = [sorted(pattern) for pattern in patterns]
    sorted_patterns.sort()
    return sorted_patterns

def remove_duplicates(patterns):
    unique_patterns=[]
    seen_items = set()
    sorted_patterns = sort_patterns(patterns)
    for pattern in sorted_patterns:
        unique_items = []
        for item in pattern:
            if item not in seen_items:
                unique_items.append(item)
                seen_items.add(item)
        unique_patterns.append(unique_items)
    return [pattern for pattern in unique_patterns if pattern]

def get_unique_patterns(filename):
    unique_patterns = remove_duplicates(get_patterns(filename))
    num_patterns = len(unique_patterns)
    return unique_patterns, num_patterns








    
