import sqlite3
import discord

import config

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

async def save(ctx, title, code):

    create_table()
    conn = get_connection()

    sql = 'INSERT INTO snippets (user_id, title, code) VALUES (?,?,?)'

    try:
        conn.execute(sql, (ctx.author.id, title, code))
        conn.commit()
        await ctx.send('Successfully saved snippet as `{}` to database.'.format(title))
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

async def get(ctx, id):

    create_table()
    conn = get_connection()

    sql = 'SELECT * FROM snippets WHERE id=?'

    try:
        cursor = conn.execute(sql, [id])

        for snippet in cursor:
            string = '{} by <@{}>\n{}'.format(snippet[1], snippet[2], snippet[3])
            return await ctx.send(string)

        await ctx.send('No snippet with that id in the database. Use `{}getAll` to list all saved snippets.'.format(config.prefix))

    except Exception as e:
        print(e)
    finally:
        conn.close()

async def getall(ctx):
    create_table()
    conn = get_connection()

    sql = 'SELECT * FROM snippets'

    try:
        cursor = conn.execute(sql)

        string = ''

        for snippet in cursor:
            string += '{}. {} by <@{}>'.format(snippet[0], snippet[1], snippet[2])
            
        if string:
            await ctx.send(string)
        else:
            await ctx.send('No snippets saved in the database.')

    except Exception as e:
        print(e)
    finally:
        conn.close()

async def edit(ctx, id):

    create_table()
    conn = get_connection()
    
    sql = 'SELECT id FROM snippets WHERE id=?'

    try:
        cursor = conn.execute(sql, [id])
        count = 0
        for snippet in cursor:
            count += 1
    except Exception as e:
        print(e)
        await ctx.send(e)
        return conn.close()

    if count == 0:
        conn.close()
        return await ctx.send('No snippet with that id found.')

    await ctx.send('Enter the new snippet\'s content: ')

    def check(m):
        return m.author.id == ctx.author.id

    response = await ctx.bot.wait_for('message', check=check)

    print(response.content)

    sql = 'UPDATE snippets SET code=? WHERE id=?'

    try:
        conn.execute(sql, [response.content, id])
        conn.commit()
        await ctx.send('Successfully updated snippet\'s content.')
    except Exception as e:
        print(e)
        await ctx.send(e)
    finally:
        conn.close()

async def delete(ctx, id):

    create_table()
    conn = get_connection()

    sql = 'SELECT id FROM snippets WHERE id=?'

    try:
        cursor = conn.execute(sql, [id])
        count = 0
        for snippet in cursor:
            count += 1
    except Exception as e:
        print(e)
        await ctx.send(e)
        return conn.close()

    if count == 0:
        conn.close()
        return await ctx.send('No snippet with that id found.')

    sql = 'DELETE FROM snippets WHERE id=?'

    try:
        conn.execute(sql, [id])
        conn.commit()
        await ctx.send('Successfully deleted snippet from database.')
    except Exception as e:
        print(e)
        await ctx.send(e)
    finally:
        conn.close()



    

