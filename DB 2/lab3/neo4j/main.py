from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "28012001"), encrypted=False)

def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])

def users_tags(tx, tags):
    for record in tx.run("MATCH (u:User)-[rel:SENT]-(:User) WHERE all(tag in $tags WHERE tag IN rel.tags) "
                         "RETURN DISTINCT u.name ORDER BY u.name", tags=tags):
        print(record["u.name"])

def path_n(tx, n):
    query = "MATCH (u1:User)-[rel:SENT*"+str(n)+"]-(u2:User) RETURN DISTINCT u1.name, u2.name"
    for record in tx.run(query):
        print("Pair: {u1}, {u2}".format(
            u1=record['u1.name'], u2=record['u2.name']))

def shortest_path(tx, user1, user2):
    record = tx.run("MATCH p=shortestPath((u:User {name: $user1})-[rel:SENT*]-(:User {name: $user2})) "
                         "RETURN length(p)", user1=user1, user2=user2)
    print("Shortest path: {n}".format(n=record.single().value()))


def spam_only(tx):
    # for record in tx.run("MATCH (u:User)-[rs*1..5]-(:User) WHERE NONE(r in rs WHERE TYPE(r)='SENT') "
    #                      "RETURN DISTINCT u.name ORDER BY u.name"):
    #     print(record["u.name"])
    # for record in tx.run("MATCH (:User)-[rs*1..5]-(u:User)-[rs*1..5]-(:User) WHERE NONE(r in rs WHERE TYPE(r)='SENT') "
    #                      "RETURN DISTINCT u.name ORDER BY u.name"):
    #     print(record["u.name"])
    # for record in tx.run("MATCH (u1:User)-[rs]-(u2:User) WHERE NONE (r in rs WHERE exists((u1:User)-[rs:SENT]-(u2:User)))"
    #                      "RETURN DISTINCT u1.name, u2.name"):
    #     print("Pair: {u1}, {u2}".format(
    #         u1=record['u1.name'], u2=record['u2.name']))
    # query = "MATCH (u1:User)-[rel:SENT]-(u2:User) RETURN DISTINCT u1.name, u2.name"
    # for record in tx.run(query):
    #     print("Pair: {u1}, {u2}".format(
    #         u1=record['u1.name'], u2=record['u2.name']))
    query = "MATCH (u1:User), (u2:User) WHERE NOT (u1:User)-[:SENT]-(u2:User) AND (u1:User)-[:SPAMMED]-(u2:User) RETURN DISTINCT u1.name, u2.name as names"
    match=[]
    for record in tx.run(query):
        name = record["names"]
        if name not in match:
            print(name)
            match.append(name)
        # print("Pair: {u1}, {u2}".format(
        #     u1=record['u1.name'], u2=record['u2.name']))
    # for record in tx.run("MATCH (u:User) WHERE NOT (u:User)-[:SENT]-(:User) "
    #                      "RETURN DISTINCT u.name ORDER BY u.name"):
    #     print(record["u.name"])

def users_tags_not_connected(tx, tags):
    for record in tx.run("MATCH (u1:User), (u2:User), (u1:User)-[rel1:SENT]-(:User), (u2:User)-[rel2:SENT]-(:User)  WHERE all(tag in $tags WHERE tag IN rel1.tags) AND all(tag in $tags WHERE tag IN rel2.tags) AND NOT (u1:User)-[]-(u2:User)"
                         "RETURN DISTINCT u1.name, u2.name", tags=tags):
        print("Pair: {u1}, {u2}".format(
                u1=record['u1.name'], u2=record['u2.name']))

def show_menu():
    print("[1] Users that sent or received messages with tags")
    print("[2] Users with path with length N")
    print("[3] Shortest path")
    print("[4] Users connected by spam")
    print("[5] Not connected users that sent or received messages with tags")
    print("[0] Exit")
    print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    show_menu()
    option = int(input('Enter option: '))
    while option!=0:
        if option == 1:
            tags_string = input('Enter tags separated with whitespace: ')
            tags = tags_string.split()
            with driver.session() as session:
                session.read_transaction(users_tags, tags)
        elif option == 2:
            n = int(input('Enter length of the path: '))
            with driver.session() as session:
                session.read_transaction(path_n, n)
        elif option == 3:
            user1 = input('Enter user 1 login: ')
            user2 = input('Enter user 2 login: ')
            with driver.session() as session:
                session.read_transaction(shortest_path, user1, user2)
        elif option == 4:
            with driver.session() as session:
                session.read_transaction(spam_only)
        elif option == 5:
            tags_string = input('Enter tags separated with whitespace: ')
            tags = tags_string.split()
            with driver.session() as session:
                session.read_transaction(users_tags_not_connected, tags)
        else:
            print("invalid option")
        print()
        show_menu()
        option = int(input('Enter option: '))
    driver.close()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
