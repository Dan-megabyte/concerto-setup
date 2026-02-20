
# Day One: Exploring on-site servers

Sudo permissions were obtained. As such, I proceeded to logon to the concerto-admin
account to find a surprise waiting for me: A 20G (and growing) log file that contains
very fine debug printing (every single request to the database prints out multiple lines
of output). However, I edited the startup file to switch `RAILS_ENV` from `development` to
`production` in an attempt to reduce the log file growth rate until the switch to docker.

In addition to that, the log files were combed through (`cat | tail | grep`) and the ip
of the client was found. Since it was dynamic, it is likely to change over time unless it
changes to detect its own static IP, but it should be sufficient for the team lead to grant
me access to the server.
