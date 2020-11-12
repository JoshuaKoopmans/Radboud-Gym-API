import requests, json

ENDPOINT = "https://publiek.usc.ru.nl/app/api/v1/?module={}&method={}&lang=nl"

def login(username, password):
    
    data = {'username': username,
            'password': password}

    r = requests.post(url=ENDPOINT.format('user', 'logIn'), data=data)
    return json.loads(r.text)
    

def logout(klant_id, token):
    data = {'klantId': klant_id,
            'token': token}

    r = requests.post(url=ENDPOINT.format('user', 'logOut'), data=data)
    return json.loads(r.text)


def get_user_agenda(klant_id, token):
    data = {'klantId': klant_id,
            'token': token}
    r = requests.post(url=ENDPOINT.format('agenda', 'getAgenda'), data=data)
    return json.loads(r.text)


def get_user_info(klant_id, token):
    data = {'klantId': klant_id,
            'token': token}
    r = requests.post(url=ENDPOINT.format('user', 'getUserData'), data=data)
    return json.loads(r.text)

def get_available_subscriptions(klant_id, token):
    data = {'klantId': klant_id,
            'token': token}
    r = requests.post(url=ENDPOINT.format('locatie', 'getLocaties'), data=data)
    return json.loads(r.text)


def add_subscription(klant_id, token, inschrijving_id, pool_id, laanbod_id, start, eind):
    data = {'klantId': klant_id,
            'token': token,
            'inschrijvingId': inschrijving_id,
            'poolId': pool_id,
            'laanbodId': laanbod_id,
            'start': start,
            'eind': eind}
    r = requests.post(url=ENDPOINT.format('locatie', 'addLinschrijving'), data=data)
    return json.loads(r.text)


def delete_subscription(klant_id, token, linschrijving_id):
    data = {'klantId': klant_id,
            'token': token,
            'linschrijvingId': linschrijving_id}
    r = requests.post(url=ENDPOINT.format('locatie', 'deleteLinschrijving'), data=data)
    return json.loads(r.text)