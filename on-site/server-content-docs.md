
# Server documentation

## Folder locations

- `/home/concerto-admin/`, `~/`: The conerto service accounts home folder,
  contains most of the system critical folders and a lot of system administration
  scripts.
- `~/secrets`: Recently added folder, contains text files with secrets, such as
  the following text files:
  - `concerto_secret.txt`: Contains the concerto secret passed to the docker container,
    used probably for CSRF token generation or password salting.
  - `openweathermap_api_key.txt`: The current OpenWeatherMap api key, should be replaced
    if needed/stops working.
- `~/concerto`: Contains all the config/data/code files for the previous (pre-docker)
  server. Data should be migrated, but kept here as a backup. Has a lot of subfolders
  - `~/concerto/app`: All of the code pre-compilation
