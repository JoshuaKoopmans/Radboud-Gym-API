import requests, json, time, random, getpass

ENDPOINT = "https://publiek.usc.ru.nl/app/api/v1/?module={}&method={}&lang=nl"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    
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


username = str(input("Enter Username: "))
password = getpass.getpass("Enter Password: ")
user_dict = login(username, password)
fitness_subs = [sub for sub in get_available_subscriptions(user_dict['klantId'], user_dict['token']) if sub['naam']=='Fitness']
for i in range(len(fitness_subs)):
    print(f"{bcolors.UNDERLINE}{fitness_subs[i]['naam']}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{time.ctime(int(fitness_subs[i]['start']))}{bcolors.ENDC}")
    print(fitness_subs[i]['inschrijvingen'], "/", fitness_subs[i]['maxInschrijvingen'])
    print(f"{bcolors.BOLD}\n To subscribe use number: {str(i)}{bcolors.ENDC}")
    print("\n"+"*-"*20+"\n")
choice = int(input("Enter choice: "))
while get_user_agenda(user_dict['klantId'], user_dict['token']) == [] :
    sub = dict(fitness_subs[choice])
    
    status = add_subscription(user_dict['klantId'], user_dict['token'], sub['inschrijvingId'], sub['poolId'], sub['laanbodId'], sub['start'], sub['eind'] )
    
    if "error" in status:
        for attempt in range(50):
            rest = random.randint(1,5)
            time.sleep(rest)
        
        time.sleep(5)
        
print(f"{bcolors.UNDERLINE}{bcolors.OKGREEN}Success!\n{bcolors.ENDC}")
print("Your agenda has been updated with linschrijvingId ", str(get_user_agenda(user_dict['klantId'], user_dict['token'])[0]['linschrijvingId']))
logout(user_dict['klantId'], user_dict['token'])
