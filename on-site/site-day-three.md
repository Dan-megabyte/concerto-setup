
# Day Three: Installing docker and setting up the container

The current state of the server is a Rails server running on bare metal.
The new way upstream is releasing updates is through docker, so installing
the new docker version should be the most pressing issue currently.

## Planning

I'll install docker first with apt, the Ubuntu package manager. Specifically the
podman frontend.

For docker, we need to pull the image and decide where to store the docker.

I decided to do a rootless docker setup, with an nginx server terminating TLS
(the docker container itself prefers to serve plain http, not great for security).
Thankfully, the server itself has a signed ssl certificate lying around (apparently
the old version does https by itself?) at `~/concerto/script/ssl/concerto.cert.key`
and `concerto.cert.crt`.

I'll reuse the old certificate, but first i need to host the new concerto server
on a port. I'll pick to host on port 8080, and firewall protect that port so that
people can't connect to it insecurely.

## Execution

With the planning done, I'll move to execution. First I need to install the Docker
image and make sure it runs.

- Install podman: `sudo apt install podman`
- Pulling down the latest version of concerto: `podman pull ghcr.io/concerto/concerto:latest`
- Generating a secret for the concerto server: `SECRET="$(docker run --rm ghcr.io/concerto/concerto:latest bin/rails secret)"`
- Create a container and volume:

    ```bash
        podman run -d -p 127.0.0.1:8080:80 -e SECRET_KEY_BASE=$SECRET -v concerto_storage:/rails/storage --cap-add CAP_NET_BIND_SERVICE --name concerto ghcr.io/concerto/concerto:latest
    ```

- Check that its inaccessible from the outside world with a curl to the server ports ✅
- And check from localhost: `curl localhost:8080`
  - This resulted in an html page being returned, which is good. The docker container IS starting up.

The docker container is set up! Wrapping up today with some documentation.

## Next steps

I'll need to set up the nginx server to terminate TLS. This should be easy, just
another `apt install` and messing around with `/etc/nginx/sites-available` as
described in [the concerto server install for vms](../vm/concerto-server-install.md).
I might have to tweak the instructions as instead of a self-signed certificate I have
an actual certificate for the lally server.

I'll then get to migrating the data from the old server (which could still be accessed on port 80)
to the new server (on port 443 for https).
