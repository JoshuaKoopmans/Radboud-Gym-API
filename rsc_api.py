import time, random, getpass, sys, os
from api_methods.methods import login, get_available_subscriptions, get_user_agenda, add_subscription, logout

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
    while 1:
        try:
            username = str(input("Enter Username: "))
            password = getpass.getpass("Enter Password: ")
            user_dict = login(username, password)
            fitness_subs = [sub for sub in get_available_subscriptions(user_dict['klantId'], user_dict['token']) if "boven /" in sub['naam'] or "beneden /" in sub['naam']][:22]
            nordvpn = input("change ip per hour? (y/n): ").lower()
            if nordvpn=='': nordvpn='n'
            if nordvpn not in 'yn': break
            else: nordvpn = True if nordvpn=='y' else False
            break
        except NameError as e:
            print("Missing Packages : ", e)
            sys.exit(1)
        except KeyError:
            print('Wrong user name or password, please try again bitch!')
        except:
            print('Something unexcepted happened... Please contact the developers.')
            
    for i in range(len(fitness_subs)):
        print(f"{bcolors.UNDERLINE}{fitness_subs[i]['naam']}{bcolors.ENDC}")
        print(f"{bcolors.WARNING}{time.ctime(int(fitness_subs[i]['start']))}{bcolors.ENDC}")
        print(fitness_subs[i]['inschrijvingen'], "/", fitness_subs[i]['maxInschrijvingen'])
        print(f"{bcolors.BOLD}\n To subscribe use number: {str(i)}{bcolors.ENDC}")
        print("\n"+"_-"*18+"\n")

    while 1:
        try:
            choice = int(input("Enter choice: "))
            sub = dict(fitness_subs[choice])
            break
        except Exception:
            print('Input not valid. Try again!')
            
    t0 = time.time() # Record how long ago the ip was changed
    message = "Failed!" 
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
                time.sleep(random.randint(13, 23))
            elif status['error'] == 'Te snel, wacht even':
                print("Apparently your request rate approached the speed of light. Waiting for 8 minutes...")
                time.sleep(510) # Wait for 8.5 minutes
            else:
                raise Exception('3rd login attempt after throttle down has been exeeded. Try again in an hour.')

        message = "Success!" 

    
    if message != "Failed!":
        print(f"{bcolors.UNDERLINE}{bcolors.OKGREEN}{message}\n{bcolors.ENDC}")       
        new_agenda_item = get_user_agenda(user_dict['klantId'], user_dict['token'])[0]
        print("Your agenda has been updated with:\n{}\n{}".format(new_agenda_item['naam'], str(time.ctime(int(new_agenda_item['start'])))))
    else:
        print(f"{bcolors.UNDERLINE}{bcolors.FAIL}{message}\n{bcolors.ENDC}")
    logout(user_dict['klantId'], user_dict['token'])
    
