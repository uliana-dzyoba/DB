import redis
import time
import random
import re

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)

def work():
    #message = r.rpop("spamq")
    message = r.lindex("spamq", -2)
    r.lrem("spamq", -1, message)
    user = re.findall('\/(.*?)\:', message)[0]
    # print(user)
    receiver = message.split('/')[0]
    r.hincrby(user, "incheck", 1)
    r.hincrby(user, "queued", -1)
    seconds = random.randint(1, 10)
    is_spam = random.randint(0, 1)
    time.sleep(seconds)
    r.hincrby(user, "incheck", -1)
    if is_spam == 1:
        spam = message.split(":",1)[1]
        r.publish("journal", f'user {user} sent message with spam: "{spam}" to {receiver}')
        r.hincrby(user, "blocked", 1)
        r.zincrby("spammers", 1, user)
    else:
        smessage = message.split("/",1)[1]
        # r.lpush("sentq", message)
        r.rpush(f'messages:{receiver}', smessage)
        r.hincrby(user, "sent", 1)
        if r.sismember("online", receiver):
            r.hincrby(user, "delivered", 1)
        r.zincrby("active", 1, user)
        print(smessage)
        ts = time.gmtime()
        print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
        print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        while r.llen("spamq") != 1:
            work()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
