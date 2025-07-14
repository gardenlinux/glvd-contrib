import testgres

# create a node with random name, port, etc
with testgres.get_new_node() as node:

    # run inidb
    node.init()

    # start PostgreSQL
    node.start()

    # execute a query in a default DB
    print(node.execute('select 1'))

# ... node stops and its files are about to be removed
