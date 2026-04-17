
# Migrating from `.bashrc` autostart scripts to systemd

Currently our autostart mechanism is a mess. The client running on our
our server raspberry pi has a service called `concerto-worker.service`
(now disabled) that ran the server through bash. Since `.bashrc`
included a call to `/home/concerto-admin/concerto_startup.sh` if there
was process titled Ruby.

To fix this, I first commented it out of bashrc and rebooted to flush
any trace of the script, and then traced the startup steps as follows:

- `concerto-worker.service`
- `~/concerto_startup.sh`
- `/usr/bin/chromium`
- `/usr/lib/chromium/chromium`

Of course this is only the browser. The window manager lightdm is lauched
through the following startup scripts:

- `~/.config/autostart/concerto_startup.desktop`
- `~/concerto_startup_master.sh`
- `lxsession` config
- `~/.config/lxsession/LXDE-pi/autostart`
- and back to `~/concerto_startup.sh`

I made two user services for the two roles that the user is supposed to
realize both the server and the local chromium frontend. They are ran by
the user called `concerto-admin`, and as user services their unit files
are hosted at `~/.config/systemd/user/*.service`.

However, I quickly realized that the server architecture was not ready
for the transition yet, and I was running out of time, so I had to quickly
switch the server back the other old one. However, the chromium is now
started up through systemd user services (although on reboot the admin
still needs to be present to decrypt the keyring with the concerto-admin
password, a problem that will probably be solved later).

I also managed to remote into the server via tigervnc to see the actual
display and how that worked.

[Next Work Summary](./site-day-twelve.md)
