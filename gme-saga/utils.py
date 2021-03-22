# Convert YYYY-MM-DD to MM/DD/YYYY
def ymd_to_mdy(date, delim1, delim2):
    date_parts = date.split(delim1)
    date_parts = [date_parts[1], date_parts[2], date_parts[0]]
    return delim2.join(date_parts)

def mdy_to_ymd(date, delim1, delim2):
    date_parts = date.split(delim1)
    date_parts = [date_parts[2], date_parts[0], date_parts[1]]
    return delim2.join(date_parts)
