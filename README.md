# MountieBot
Discord Bot


## Setup:

- Intall the following Python packages
    ```
    discord.py[voice] 
    PyMySQL
    bs4
    requests
    selenium
    ```
    optional:
    ```
    pytube3
    moviepy
    ```

- Install [FireFox](https://www.mozilla.org/en-US/firefox/)

- Create the file **server_info.json** in the root directory with the credentials of your remote mysql server
    ```
    {
    	"ip" : "your_MySQL_server_IP",
    	"database": {
    		"name" :"your_MySQL_database_name",
    		"user": "your_MySQL_database_username",
    		"password": "your_MySQL_database_password"
    	}
    }
    ```
    
#### optional cogs
mtsac (search for classes)

#### unfinished cogs
vc (music)