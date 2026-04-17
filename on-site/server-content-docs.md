
# Server documentation

## Folder locations

- `/home/concerto-admin/`, `~/`: The concerto service accounts home folder,
  contains most of the system critical folders and a lot of system administration
  scripts.
- `~/secrets`: Recently added folder, contains text files with secrets, such as
  the following text files:
  - `concerto_secret.txt`: Contains the concerto secret passed to the docker container,
    used probably for CSRF token generation or password salting.
  - `openweathermap_api_key.txt`: The current OpenWeatherMap api key, should be replaced
    if needed/stops working.
- `~/concerto/`: Contains all the config/data/code files for the previous (pre-docker)
  server. Data should be migrated, but kept here as a backup. Has a lot of subfolders
  - `~/concerto/app/`: All of the code pre-compilation
- `~/autorefresh/`: Contains the files needed for the autorefresh script
  - `~/autorefresh/autorefresh.py`: The script run by the startup
  - `~/autorefresh/.env`: The credentials used by the autorefresh script to log into
    the server and refresh the feeds. The feeds refreshed and the refresh interval can
    be configured through the `.env` file.
- `~/weather/`: Contains the files for the weather fetching server script. (uses FastAPI)
  - `~/weather/.env`: Contains the api key for openweather
  - `~/weather/main.py`: Contains the code for the weather feed feed
  - `~/weather/start.sh`: Contains a bash script to activate the venv and run the script on a loop.
- `~/.config/systemd/user`: Contains user services, used to start both the server and the kioscs.
  - `concerto-autorefresh.service`: Starts and keeps track of the status of the autorefresh script
  - `concerto-kiosk.service`: Starts and keeps track of the chromium browser frontend
  - `container-concerto.service`: Starts and keeps track of the new Docker server
  - `concerto-startup.service`: Started the old concerto server, now disabled.
- `~/.local/share/containers/storage/volumes/concerto_storage/_data`: Contains the concerto
  volume, where the current databases are stored to this day.
