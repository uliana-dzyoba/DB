import redis
import random
from neo4j import GraphDatabase

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "28012001"), encrypted=False)

# def log_in():
#     login = input('Enter username: ')
#     if r.sismember("users", login) == 1:
#         return login
#     else:
#         print("this user does not exist")
#         return None

# def send_message(login):
#     receiver = input('Enter username to send message to: ')
#     if r.sismember("users", receiver) == 1:
#         message = input('Enter message: ')
#         r.hincrby(login, "created", 1)
#         r.lpush("spamq", f'{receiver}/{login}: {message}')
#         r.hincrby(login, "queued", 1)
#     else:
#         print("this user does not exist")
        #return None
tags = ["sales", "support", "love", "happy", "fashion", "summer", "style", "fun", "funny", "cute", "life", "lifestyle", "amazing", "motivation", "healthy"]

def send_message(sender, receiver):
    message = "random message"
    number_of_tags = random.randint(0, 5)
    chosen_tags =[]
    for i in range(number_of_tags):
        tag = tags[random.randint(0, 14)]
        if tag not in chosen_tags:
            message = message + " #" + tag
            chosen_tags.append(tag)
    r.hincrby(sender, "created", 1)
    r.lpush("spamq", f'{receiver}/{sender}: {message}')
    r.hincrby(sender, "queued", 1)

# def view_messages(login):
#     n = int(input('Enter number of messages, 0 for all: '))
#     if n >= 0:
#         messages = r.lrange(f'messages:{login}', 0, n-1)
#         for message in messages:
#             if message is not "":
#                 print(message)
#     else:
#         print("number must be positive")
#
# def view_statistics(login):
#     created = r.hget(login, "created")
#     print(f'created: {created}')
#     queued = r.hget(login, "queued")
#     print(f'in queue: {queued}')
#     incheck = r.hget(login, "incheck")
#     print(f'checking for spam: {incheck}')
#     blocked = r.hget(login, "blocked")
#     print(f'blocked for spam: {blocked}')
#     sent = r.hget(login, "sent")
#     print(f'sent to user: {sent}')
#     delivered = r.hget(login, "delivered")
#     print(f'delivered to user: {delivered}')

def log_offline(login):
    r.publish("journal", f'{login} went offline')
    r.srem("online", login)
    with driver.session() as session:
        session.write_transaction(update_status_to_offline, login)


def log_online(login):
    r.publish("journal", f'{login} now online')
    r.sadd("online", login)
    with driver.session() as session:
        session.write_transaction(update_status_to_online, login)
    sent = r.hget(login, "sent")
    r.hset(login, "delivered", sent)

# def show_menu():
#     print("[1] Send message")
#     print("[2] View messages")
#     print("[3] View statistics")
#     print("[0] Exit")
#     print()

def check_is_online(login):
    if r.sismember("online", login):
        return True

def emulate():
    for x in range(100):
    # while True:
        login_n = random.randint(1, 20)
        login = "login" + str(login_n)
        if check_is_online(login):
            log_offline(login)
        else:
            log_online(login)
            receiver_n = random.randint(1, 20)
            receiver = "login" + str(receiver_n)
            if login != receiver:
                number_of_messages = random.randint(0, 5)
                for i in range(number_of_messages):
                    send_message(login, receiver)

def create_users(tx, login):
    tx.run("CREATE (:User {name: $name, is_online:false}) ", name=login)

def update_status_to_online(tx, login):
    tx.run("MATCH (u:User {name: $name}) "
           "SET u.is_online = true", name=login)

def update_status_to_offline(tx, login):
    tx.run("MATCH (u:User {name: $name}) "
           "SET u.is_online = false", name=login)

if __name__ == '__main__':
    # login = log_in()
    # if login:
    #     log_online(login)
    #     show_menu()
    #     option = int(input('Enter option: '))
    #     while option!=0:
    #         if option == 1:
    #             send_message(login)
    #         elif option == 2:
    #             view_messages(login)
    #         elif option == 3:
    #             view_statistics(login)
    #         else:
    #             print("invalid option")
    #         print()
    #         show_menu()
    #         option = int(input('Enter option: '))
    #     log_offline(login)
    emulate()
    # with driver.session() as session:
    #     for x in range(20):
    #         login = "login" + str(x+1)
    #         session.write_transaction(create_users, login)
    # driver.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
