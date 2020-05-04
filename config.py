import pymysql.cursors
import json
import os


'''

CONFIG DATA

'''
#the default command prefixes
default_prefixes = ['!']
#the list of optional cogs
optionalCogs = ['mtsac', 'vc']
#SUCCESSFUL MYSQL SERVER CONNECTION BOOLEAN
sqlConnected = False
#THE LINKS (from database)
links = {}
#THE CUSTOM PREFIXES (from database)
custom_prefixes = {}
#SELF ASSIGNABLE ROLES
self_assignable_roles = {}


#change cwd to directory of file
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#getting the server credentials
with open("server_info.json", "r") as read_file:
    server_info = json.load(read_file)

# getting from the database
def getFromDB(table, cursor):
    #selecting the url with the given guildid and link name
    sql = "SELECT * FROM `" + table + "` limit 1"
    cursor.execute(sql)
    return cursor.fetchone()
    
try:
    #connection to remote mysql server
    connection = pymysql.connect(host=server_info["ip"],
                                user=server_info["database"]["user"],
                                password=server_info["database"]["password"],
                                db=server_info["database"]["name"],
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
    )
    sqlConnected = True
except: 
    print("MySQL Server Connection Failed.")


#if the mysql server connection was successful
if sqlConnected:
    #getting the data from the remote mysql server
    try:
        with connection.cursor() as cursor:


            init_DB_SQL = [
            "CREATE TABLE IF NOT EXISTS links(guild_links TEXT);",
            "INSERT INTO links(guild_links) SELECT \"{}\" WHERE NOT EXISTS (SELECT *FROM links);",

            "CREATE TABLE IF NOT EXISTS prefixes(default_prefixes TEXT, custom_prefixes TEXT);",
            "INSERT INTO prefixes(default_prefixes, custom_prefixes) SELECT \"[!]\", \"{}\" WHERE NOT EXISTS (SELECT * FROM prefixes);",

            "CREATE TABLE IF NOT EXISTS selfroles(rolenames TEXT);",
            "INSERT INTO selfroles(rolenames) SELECT \"{}\" WHERE NOT EXISTS (SELECT *FROM selfroles);"
            ]
            
            for initDB in init_DB_SQL:
                cursor.execute(initDB)


            #GETTING THE LINKS FROM THE DATABASE

            links = json.loads(getFromDB("links", cursor)['guild_links'])
            
            #GETTING THE CUSTOM PREFIXES FROM THE DATABASE

            custom_prefixes = json.loads(getFromDB("prefixes", cursor)['custom_prefixes'])

            #GETTING THE SELF ASSIGNABLE ROLES FROM THE DATABASE
            self_assignable_roles = json.loads(getFromDB("selfroles", cursor)['rolenames'])

    finally:
        connection.close()

#function to get the prefix based on guild id
async def determine_prefix(bot, message):
    return custom_prefixes.get(str(message.guild.id)) or default_prefixes