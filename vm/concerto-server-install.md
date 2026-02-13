
# Installing Concerto from a blank debian-based server

## Install Dependencies

The following dependencies are needed in addition to a minimal ubuntu setup:

- `podman-docker`: for containerizing the Concerto server
- `nginx`: for terminating tls

  ```bash
  sudo apt install docker nginx
  ```

## Install Concerto

- pull the latest Concerto image to your computer
  
  ```bash
  podman pull ghcr.io/concerto/concerto:latest
  ```

- generate a secret for server auth

  ```bash
  SECRET="$(docker run --rm ghcr.io/concerto/concerto:latest bin/rails secret)"
  ```

- use the secret and the image to create a container
  
  ```bash
  docker run -d -p localhost:8080:80 -e SECRET_KEY_BASE=$SECRET -v concerto_storage:/rails/storage --cap-add CAP_NET_BIND_SERVICE --name concerto ghcr.io/concerto/concerto:latest
  ```

## Install nginx https proxy

Since the vanilla concerto server doesn't support https we need to proxy the connections through a
tls terminating nginx server. We need to generate ssl certificates first though. An alternative,
of course, is to get signed certificates from a CA but you need a domain name for that.

- generate a self signed certificate for ssl

  ```bash
  sudo mkdir -p /etc/nginx/ssl
  cd /etc/nginx/ssl
  sudo openssl req -x509 -nodes -days 365 \
  -newkey rsa:4096 \
  -keyout concerto.key \
  -out concerto.crt
  ```

- configure the nginx proxy for ssl proxying

  file `/etc/nginx/sites-available/concerto`

  ```nginx
  # HTTP → HTTPS redirect
  server {
      listen 80;

      return 301 https://$host$request_uri;
  }

  # HTTPS reverse proxy
  server {
      listen 443 ssl http2;

      ssl_certificate     /etc/nginx/ssl/concerto.crt;
      ssl_certificate_key /etc/nginx/ssl/concerto.key;

      # Reasonable defaults
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers HIGH:!aNULL:!MD5;

      location / {
          proxy_pass http://127.0.0.1:8080;

          proxy_http_version 1.1;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto https;
      }
  }
  ```

- disable the default http server so that the http to https redirect takes precedence

  ```bash
  sudo rm /etc/nginx/sites-enabled/default
  ```

- activate and reload the new nginx settings

  ```bash
  sudo ln -s /etc/nginx/sites-available/concerto /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl reload nginx
  ```

- navigate to `https://<server-ip>` in your preferred graphical web browser to register
  the first account, which automatically gets administrator permissions.
