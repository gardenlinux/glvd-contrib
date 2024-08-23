import asyncio
import asyncpg
import datetime

async def main():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    asyncio.sleep(15)

    DBUSER = os.environ["DBUSER"]
    DBPASS = os.environ["DBPASS"]
    DBHOST = os.environ["DBHOST"]
    DBNAME = os.environ["DBNAME"]
    conn = await asyncpg.connect(f"postgresql://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}")
    # Execute a statement to create a new table.
    await conn.execute('''
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name text,
            dob date
        )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO users(name, dob) VALUES($1, $2)
    ''', 'Bob', datetime.date(1984, 3, 1))

    # Select a row from the table.
    row = await conn.fetchrow(
        'SELECT * FROM users WHERE name = $1', 'Bob')
    # *row* now contains
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))

    # Close the connection.
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())
