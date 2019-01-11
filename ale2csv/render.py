import csv
import shutil
import io

def render_csv(data_list, destination=None, column_labels=None):
    csv_buffer = format_csv(data_list, column_labels=column_labels)

    if destination:
        with open(destination, 'w') as f:
            shutil.copyfileobj(csv_buffer, f)
        return None
    else:
        return csv_buffer.getvalue()


def format_csv(data_list, column_labels=None):
    buff = io.StringIO()
    if column_labels:
        writer = csv.DictWriter(buff, fieldnames=column_labels)
        writer.writeheader()
        for row in data_list:
            writer.writerow(dict(zip(column_labels, row)))
    else:
        writer = csv.writer(buff)
        writer.writerows(data_list)
    
    buff.seek(0)
    return buff


