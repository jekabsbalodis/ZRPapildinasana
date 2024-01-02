from datetime import datetime

def lastUpdate():
    f = open('.lastUpdate', encoding='utf-8')
    last_update = datetime.strptime(f.read(), '%Y-%m-%d').date()
    f.close()
    return last_update