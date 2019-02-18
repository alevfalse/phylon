import sqlite3
import discord

def get_connection():
    try:
        conn = sqlite3.connect('db.sqlite3')
        return conn
    except Exception as e:
        print(e)


def create_table():
    conn = get_connection()

    sql = ''' create table if not exists snippets(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              user_id TEXT,
              code TEXT)'''

    try: 
        conn.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

async def saveCode(ctx, title, code):

    print(code)

    print(code.startswith("```"))
    print(code.endswith("```"))

    if not code.startswith("```") or not code.endswith("```"):
        return await ctx.send('Invalid code snippet.')

    create_table()
    conn = get_connection()

    sql = 'INSERT INTO snippets (user_id, title, code) VALUES (?,?,?)'

    try:
        conn.execute(sql, (ctx.author.id, title, code))
        conn.commit()
        await ctx.send('Successfully saved code snippet as `title` to database.')
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

async def getCode(ctx, title):
    conn = get_connection()

    sql = 'SELECT * FROM snippets WHERE title=?'

    print(title)
    try:
        cursor = conn.execute(sql, [title])
        for snippet in cursor:
            string = '{} by <@{}>\n{}'.format(snippet[1], snippet[2], snippet[3])
            await ctx.send(string)
    except Exception as e:
        print(e)
    finally:
        conn.close()

async def listCodes(ctx):
    conn = get_connection()

    sql = 'SELECT * FROM snippets'

    try:
        cursor = conn.execute(sql)
        for snippet in cursor:
            string = '{}] {} by <@{}>'.format(snippet[0], snippet[1], snippet[2])
            await ctx.send(string)
    except Exception as e:
        print(e)
    finally:
        conn.close()



    

