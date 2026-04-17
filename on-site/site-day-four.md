
# Day Four: Installing and setting up Nginx for TLS termination

## Plan

We need to setup tls, so that modern browsers (firefox) can actually send passwords to
the site for registration and whatnot. This'll be handled via nginx.

Using my experience in the VM, I'll install nginx with apt, copy over the ssl certificates
to `/etc/nginx/ssl`, and change the files in `sites-available` to host proxy port 8080.

I'll also disable the default http server so that it doesn't interfere with the current
(outdated) server.

## Execution

After connecting to the server with ssh, I install nginx with `sudo apt install nginx`.

I then disable the default site at `/etc/nginx/sites-enabled/default` through a quick `sudo rm`.

I add the file `/etc/nginx/sites-available/concerto` with the sane defaults in
[the vm setup guide](../vm/concerto-server-install.md#install-nginx-https-proxy).
However, I don't set up the http redirect yet while the previous concerto server is running.

Before starting the nginx proxy, I do need to copy the tls certificates from the local server.
A simple pair of `cp`'s to the `/etc/nginx/ssl` will work... Nope. Directory ssl not created yet.
`mkdir /etc/nginx/ssl` and repeat. There! The certificates are placed correctly.

Now we run `systemctl restart nginx` and pray. Seems to work... until i figure out there is no server
listening on port 443. A simple curl gives no response. The port 8080, which should be forwarding the
http port, still doesn't work.

Simple, the docker container must've gone down, right? This also matched the communication with my
lead, since the server was restarted in that time. Is there any way to set it up so that it starts
on reboot? Well, for now I start it with a simple `podman start concerto`. This allows me to
`curl localhost:8080` sucessfully.

I then search up how to do such a thing as auto starting a container and stumble across the `--restart`
docker option in the docs. I run `docker update --restart unless-stopped concerto` to update the container
with the new configuration.

However, the TLS termination doesn't work. After looking at nginx logs through `journalctl`, I find that the
certificates are dreadfully insecure and actually self-signed! This surprise made me feel ok enough to generate
a self-signed certificate with modern security standard with the following command:
`openssl req -x509 -nodes -days 600  -newkey rsa:2048  -keyout concerto.key  -out concerto.crt`

I replaced the previous keys with the new keys and the nginx server started successfully. After making
the first admin account on the new concerto site, I decided that I needed to talk to my project lead about
the possibility of getting an actual signed certificate from the RPI hostmaster, to dismiss the annoying
self-signed warnings when attempting to connect to it.

[Next Work Summary](./site-day-five.md)
