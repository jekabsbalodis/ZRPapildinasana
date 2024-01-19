'''Record when was the last date
information about recently added
medications to Drug register was added'''
from datetime import datetime


def last_update():
    '''Function to record the last data read date'''
    with open('.lastUpdate', encoding='utf-8') as f:
        update_date = datetime.strptime(f.read(), '%Y-%m-%d').date()
    return update_date
