Info
=========

I create symbolic links from conf files in this directory to their respectable locations to start nginx proxy server and supervisor

$ sudo ln -s /srv/www/dcmdb/conf/nginx.conf /etc/nginx/sites-available/dcmdb
$ sudo ln -s /srv/www/dcmdb/conf/supverisor.conf /etc/supervisor/conf.d/dcmdb

/var/lib/nginx/proxy/ needs nginx user to have owner:group access

$ sudo chown -R ubuntu:ubuntu /var/lib/nginx/nginx/proxy

On server restart, EBS must be mounted

$ sudo mount /dev/xvdf /mnt/media
