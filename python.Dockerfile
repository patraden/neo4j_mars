FROM python:3.7
ARG USERNAME=python
ARG USERPASS=patraden
RUN apt update && apt -y install openssh-server whois
RUN useradd -ms /bin/bash $USERNAME
RUN usermod --password $(echo "$USERPASS" | mkpasswd -s) $USERNAME
RUN apt purge -y whois && apt -y autoremove && apt -y autoclean && apt -y clean
COPY entrypoint.sh entrypoint.sh
RUN chmod +x /entrypoint.sh

USER $USERNAME
RUN mkdir /home/$USERNAME/.ssh && touch /home/$USERNAME/.ssh/authorized_keys
RUN mkdir /home/$USERNAME/code
WORKDIR /home/$USERNAME/code

USER root
COPY requirements.txt /home/$USERNAME/code/
RUN pip install -r requirements.txt
CMD ["/entrypoint.sh"]
