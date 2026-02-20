
# Day One: Exploring on-site servers

The current server architecture needs maintenance. Currently the pages themselves are being
hosted by a central server in one building (let's call this building A). Connecting to the
first server was easy. A simple ssh got me on my account, but sudo permissions were not added yet.
From visual inspection, the server appears to run Ubuntu 22.04.5 LTS on a raspberry pi (which
works wonderfully in this arm64 support situation), but a simple `ls /home` reveals three different system users:
concerto-admin, concerto-admin2, concerto-maintenance.

My objective is to make the server backend entirely a docker containerized application. The container itself
will be hosted on docker, but we'll add a nginx server to terminate TLS.
