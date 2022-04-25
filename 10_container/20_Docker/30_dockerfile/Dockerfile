FROM ubuntu:focal
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt update && \
    apt install -y apache2 libapache2-mod-php

RUN echo "<?php phpinfo(); ?>" > /var/www/html/index.php

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]