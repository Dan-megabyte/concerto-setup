
# Documentation + Initial steps to getting weather to work

I tried to make [documentation for folder contents](./server-content-docs.md),
exploring the server tree and their purpose. It should be easier for a future
project member to orient themselves within the server after reading the documentation
for the folders they can go to.

To attempt to get weather working, I made a FastAPI python script that acted as a feed
generator for concerto, but actually fetching the weather API. Since its fetched every
so often, it shouldn't be performance critical so fast python development seemed like
the right choice. The [code](../python-weather-feed/main.py) can be found on this very
repo, and contains code to read the api keys from a `.env` file.

To upload it to the server, I decided to make it listen on localhost since it should
just be only for the local concerto server. Port will be set arbitrarily to `43678`, which
the concerto server can fetch.

To make it reproducible to other concerto servers, I made a
[requirements.txt](../python-weather-feed/requirements.txt) file so that I can simply run
`pip -r requirements.txt` to install it.

So the steps basically are:

- Make a new folder (for example, `~/` for the `concerto-admin` user) called `weather`
- `cd` into it and run `python -m venv .venv` to create a virtual environment
- Copy the contents of [the weather feed folder](../python-weather-feed/) on this repo
  to the folder we were in
- Create a `.env` folder with `api_key=<Weather Api Key>` to store the secret
- Run `. .venv/bin/activate` to activate the venv
- `pip install -r requirements.txt` to install the required libraries
- Test the server by running `fastapi run --host 127.0.0.1`
- `deactivate` to get out of the venv
- Install and enable/start the [systemd unit file](../python-weather-feed/concerto-weather.service)

The weather service will be running now! Sending a `curl 'http://localhost:43678/weather.json?lat=<>&lon=<>`
gives html that can be displayed through concerto!

The next day I'll set up the feed onto the concerto server so that it displays.
