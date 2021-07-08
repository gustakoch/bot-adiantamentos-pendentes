from datetime import datetime

def greeting():
    now = datetime.now().time()
    half_time = datetime.strptime('12:00:00', '%H:%M:%S').time()

    if now < half_time:
        return 'Bom dia'
    
    return 'Boa tarde'
