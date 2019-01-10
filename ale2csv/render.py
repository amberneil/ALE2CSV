import csv

def render_csv(data_list, destination, column_labels=None):
    import os
    print(os.path.abspath(destination))
    with open(destination, 'w', newline='') as f:
        if column_labels:
            writer = csv.DictWriter(f, fieldnames=column_labels)
            writer.writeheader()
            for row in data_list:
                writer.writerow(dict(zip(column_labels, row)))
        else:
            writer.writerows(data_list)