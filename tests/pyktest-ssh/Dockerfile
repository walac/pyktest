FROM registry.fedoraproject.org/fedora:latest

RUN dnf upgrade --refresh -y

RUN dnf install -y openssh-server

COPY fake_keys/id_rsa.pub /etc/ssh/authorized_keys

COPY sshd_config /etc/ssh

RUN ssh-keygen -b 1024 -f /etc/ssh/ssh_host_rsa_key -t rsa -N ""
RUN ssh-keygen -b 1024 -f /etc/ssh/ssh_host_dsa_key -t dsa -N ""
RUN ssh-keygen -b 521 -f /etc/ssh/ssh_host_ecdsa_key -t ecdsa -N ""
RUN ssh-keygen -b 1024 -f /etc/ssh/ssh_host_ed25519_key -t ed25519 -N ""

ENTRYPOINT /usr/sbin/sshd -D
