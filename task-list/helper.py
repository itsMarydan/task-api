def convert_string_to_bool(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")


def process_csv(data):
    for row in data:
        row['completed'] = convert_string_to_bool(row['completed'])
    return data