import csv

input_file = 'Your_file_dveri.csv'
output_file = 'VAR-Your_file_dveri.csv'

delimiter = ';'
variation_code_prefix = "V"
variation_increment = 10

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter=delimiter)
    fieldnames = reader.fieldnames + ["Variation group code"]
    if fieldnames and "Цвет" in fieldnames:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        variation_code_number = 0
        for row in reader:
            sizes = row["Цвет"].split('/')
            variation_code_number += variation_increment
            variation_group_code = variation_code_prefix + str(variation_code_number)
            for size in sizes:
                new_row = row.copy()
                new_row["Цвет"] = size.strip()
                new_row["Variation group code"] = variation_group_code
                writer.writerow(new_row)
