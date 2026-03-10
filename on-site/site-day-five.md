
# Day 5: Contacting project lead & getting future bearings

Today I got back from break and my project lead was in the room!
I asked him a load of questions about both the server install and what
the most pressing issues for the project were. After telling him the following:

- The new concerto version is hosted on the server, with docker
- There is terminated TLS w/ nginx but only with a self-signed certificate
- I'm having trouble figuring out the migration from the old server to the new server

He responded with the following key details & project priorities:

- The new server is great!
- Need to get the weather applet to work, since it broke on the last server.
- The TLS certificate can be resolved if we talk to the lab people.
- Migration of the old/expired pictures and content is unimportant, so we
  only need to migrate the still active ones. Since there is a small number
  of those, it is feasible to manually migrate them.
- While unsure, we believes that the weather updating system failing was due
  to a faulty systemd timer.

## Today's work

I found where the weather data was being fetched by colming through logs: OpenWeatherMap.
They offer 60 request/sec for personal projects and more for students but the personal
plan is enough for our purposes. We already have an API key as well, which was helpfully
(but insecurely) printed twice in the last 500000 lines of the debug log. Suprisingly
enough, the api request after reading the docs is simple:
`https://api.openweathermap.org/data/2.5/weather?lat=<latitude>&lon=<longitude>&appid=<api key>`
I commented this to my peer as well as the possibility of having a script auto-fetching and
printing the data, and he responded with plenty of motivation to get working on it.

After delegating the script creation, I moved on to wanting to document the server secrets, but
sadly github is not the best place for them. To anyone picking up the pieces of my legacy, I created
a directory in the user's home directory called `secrets` that contains most of the API keys
used/created in this process.

## Friday plans

On Friday, I'll hopefully document where things are on the server.
