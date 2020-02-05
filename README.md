# MountieBot
Discord Bot


## Setup:
- Add the /cogs/resources/ directory to PATH

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