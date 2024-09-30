import datetime


def add_days(date_str: str, date_format: str = '%Y-%m-%d', delta=1):
    d = datetime.datetime.strptime(date_str, date_format)
    return (d + datetime.timedelta(days=delta)).strftime(date_format)
