import redis

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)

def log_in():
    login = input('Enter username: ')
    if r.sismember("users", login) == 1:
        return login
    else:
        print("this user does not exist")
        return None

def send_message(login):
    receiver = input('Enter username to send message to: ')
    if r.sismember("users", receiver) == 1:
        message = input('Enter message: ')
        r.hincrby(login, "created", 1)
        r.lpush("spamq", f'{receiver}/{login}: {message}')
        r.hincrby(login, "queued", 1)
    else:
        print("this user does not exist")
        #return None

def view_messages(login):
    n = int(input('Enter number of messages, 0 for all: '))
    if n >= 0:
        messages = r.lrange(f'messages:{login}', 0, n-1)
        for message in messages:
            if message is not "":
                print(message)
    else:
        print("number must be positive")

def view_statistics(login):
    created = r.hget(login, "created")
    print(f'created: {created}')
    queued = r.hget(login, "queued")
    print(f'in queue: {queued}')
    incheck = r.hget(login, "incheck")
    print(f'checking for spam: {incheck}')
    blocked = r.hget(login, "blocked")
    print(f'blocked for spam: {blocked}')
    sent = r.hget(login, "sent")
    print(f'sent to user: {sent}')
    delivered = r.hget(login, "delivered")
    print(f'delivered to user: {delivered}')

def log_offline(login):
    r.publish("journal", f'{login} went offline')
    r.srem("online", login)

def log_online(login):
    r.publish("journal", f'{login} now online')
    r.sadd("online", login)
    sent = r.hget(login, "sent")
    r.hset(login, "delivered", sent)

def show_menu():
    print("[1] Send message")
    print("[2] View messages")
    print("[3] View statistics")
    print("[0] Exit")
    print()


if __name__ == '__main__':
    login = log_in()
    if login:
        log_online(login)
        show_menu()
        option = int(input('Enter option: '))
        while option!=0:
            if option == 1:
                send_message(login)
            elif option == 2:
                view_messages(login)
            elif option == 3:
                view_statistics(login)
            else:
                print("invalid option")
            print()
            show_menu()
            option = int(input('Enter option: '))
        log_offline(login)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
