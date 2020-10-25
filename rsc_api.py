import requests, json, time, random, getpass, sys, os

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

if __name__ == "__main__":
    while 1:
        try:
            username = str(input("Enter Username: "))
            password = getpass.getpass("Enter Password: ")
            nordvpn = input("change ip per hour? (y/n): ").lower()
            if nordvpn=='': nordvpn='n'
            if nordvpn not in 'yn': break
            else: nordvpn = True if nordvpn=='y' else False
            user_dict = login(username, password)
            fitness_subs = [sub for sub in get_available_subscriptions(user_dict['klantId'], user_dict['token']) if "Fitness" in sub['naam']][:22]
            break
        except:
            print('Wrong user name or password, please try again bitch!')
            
    for i in range(len(fitness_subs)):
        print(f"{bcolors.UNDERLINE}{fitness_subs[i]['naam']}{bcolors.ENDC}")
        print(f"{bcolors.WARNING}{time.ctime(int(fitness_subs[i]['start']))}{bcolors.ENDC}")
        #print(fitness_subs[i]['inschrijvingen'], "/", fitness_subs[i]['maxInschrijvingen'])
        print(f"{bcolors.BOLD}\n To subscribe use number: {str(i)}{bcolors.ENDC}")
        print("\n"+"_-"*18+"\n")

    while 1:
        try:
            choice = int(input("Enter choice: "))
            sub = dict(fitness_subs[choice])
            break
        except Exception:
            print('try again!')
            
    t0 = time.time() # Record how long ago the ip was changed  
    while get_user_agenda(user_dict['klantId'], user_dict['token']) == [] :
        if nordvpn:
            if time.time() - t0 > 3600:
                os.system('nordvpn c')
                time.sleep(8)
                t0 = time.time()
                user_dict = login(username, password)
        status = add_subscription(user_dict['klantId'], user_dict['token'], sub['inschrijvingId'], sub['poolId'], sub['laanbodId'], sub['start'], sub['eind'] )
        if 'error' in status:
            if status['error'] == 'Niet gevonden':
                max_seconds = int((int(sub['start']) - time.time())/3600)+1
                time.sleep(random.randint(1, max_seconds))
            else: break
            
    print(f"{bcolors.UNDERLINE}{bcolors.OKGREEN}Success!\n{bcolors.ENDC}")
    new_agenda_item = get_user_agenda(user_dict['klantId'], user_dict['token'])[0]
    print("Your agenda has been updated with:\n{}\n{}".format(new_agenda_item['naam'], str(time.ctime(int(new_agenda_item['start'])))))
    logout(user_dict['klantId'], user_dict['token'])
