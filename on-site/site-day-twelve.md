
# Day 12: The great fixing

This week I finished up the rest of the main issues plauging the system.

I started by regenerating the database from scratch, to see if this would
fix the 500 errors on most pages of the admin interface. This (as I expected)
fixed all of the error code 500 issues, allowing the site to be usable.

I also added an auto-refresh python script in `~/autorefresh/` it should log
in as the user specified in `~/autorefresh/.env`, and refresh feed #4. While I
could make it more configurable, I decided against it for now since there are
many many other things to fix up, like configuring the concerto frontends to point
to the new server instead of the old one. The [actual code](../autorefresh/autorefresh.py)
for the python script can be found on this repo.

The autorefresh script also comes with [its own systemd user script](../autorefresh/concerto-autorefresh.service),
which I installed and it works like a charm, currently updating the weather feed
every 5 minutes.

On the other side of things, the client raspi (the one not hosting the server)
failed to start so I logged in and found that the keychain wasn't configured.
I just set an empty password since the raspi shouldn't be holding any secrets.

I then switched both of the clients to the new (https) server. The project is
mostly complete! Just a bunch of finishing touches needed.

## Future plans

- Add more feeds
- Auto-refresh multiple feeds
- Turn off old server
- Make frontends restart at midnight.
- Update???
