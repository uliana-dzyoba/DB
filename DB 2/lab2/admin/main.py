import redis
import time

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe('journal')


def view_journal():
    while True:
        message = p.get_message()
        if message:
            # do something with the message
            print(message["data"])
            time.sleep(0.01)  # be nice to the system :)

def view_online():
    users = r.smembers("online")
    print("Users online:")
    print(users)

def view_active():
    n = int(input('Enter number of users, 0 for all: '))
    if n >= 0:
        active = r.zrange("active", 0, n-1, desc=True, withscores=True)
        print("Active users:")
        for act in active:
            print(act)
    else:
        print("number must be positive")

def view_spammers():
    n = int(input('Enter number of users, 0 for all: '))
    if n >= 0:
        spammers = r.zrange("spammers", 0, n-1, desc=True, withscores=True)
        print("Spammers:")
        for spammer in spammers:
            print(spammer)
    else:
        print("number must be positive")

def show_menu():
    print("[1] View journal")
    print("[2] View most active users")
    print("[3] View spammers")
    print("[0] Exit")
    print()

def log_in():
    login = input('Enter username: ')
    if r.sismember("users", login) == 1:
        if r.hget(login, "group") == "admin":
            return True
        else:
            print("this user is not an admin")
    else:
        print("this user does not exist")
        return False

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    login = log_in()
    if login:
        show_menu()
        option = int(input('Enter option: '))
        while option != 0:
            if option == 1:
                view_journal()
            elif option == 2:
                view_active()
            elif option == 3:
                view_spammers()
            else:
                print("invalid option")
            print()
            show_menu()
            option = int(input('Enter option: '))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
