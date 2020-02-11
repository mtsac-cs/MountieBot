import pymysql.cursors
import json
import os

#the default command prefixes
default_prefixes = ['!']

#the list of optional cogs
optionalCogs = ['mtsac', 'vc']

#change cwd to directory of file
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#getting the server credentials
with open("server_info.json", "r") as read_file:
    server_info = json.load(read_file)

# Connecting to the database
def getFromDB(table, cursor):
    #selecting the url with the given guildid and link name
    sql = "SELECT * FROM `" + table + "` limit 1"
    cursor.execute(sql)
    return cursor.fetchone()

#connection to remote mysql server
connection = pymysql.connect(host=server_info["ip"],
                             user=server_info["database"]["user"],
                             password=server_info["database"]["password"],
                             db=server_info["database"]["name"],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
)

#getting the custom prefixes from the remote mysql server
try:
    with connection.cursor() as cursor:
        links = json.loads(getFromDB("links", cursor)['guild_links'])
        custom_prefixes = json.loads(getFromDB("prefixes", cursor)['custom_prefixes'])
finally:
    connection.close()


#function to get the prefix based on guild id
async def determine_prefix(bot, message):
    guild = message.guild
    #Only allow custom prefixs in guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes