# Generated by Anaconda 34.25.1.14
# Generated by pykickstart v3.32
#version=RHEL9
# Use command line install
cmdline

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end

# Keyboard layouts
keyboard --xlayouts='us'
# System language
lang en_US.UTF-8

# Use CDROM installation media
cdrom

%packages --inst-langs en_US --excludedocs
@^minimal-environment
openssh-server
dracut
grubby
grub2-pc
grub2-tools
#systemd-networkd
%end

# Run the Setup Agent on first boot
firstboot --disabled

# Generated using Blivet version 3.4.0
ignoredisk --only-use=vda
autopart
# Partition clearing information
clearpart --none --initlabel

bootloader --timeout 1 --append "console=ttyS0,115200"

# System timezone
timezone America/Sao_Paulo --utc

# Root password
authselect --useshadow --passalgo sha512
rootpw --plaintext 123456

firewall --enabled --service ssh

#services --enabled networkd
services --enabled sshd

%post --erroronfail --log /var/log.txt
cat > etc/ssh/sshd_config << EOF
Include /etc/ssh/sshd_config.d/*.conf
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
PermitRootLogin yes
PermitEmptyPasswords yes
PasswordAuthentication yes
Subsystem	sftp	/usr/libexec/openssh/sftp-server
Port 22
EOF

ssh-keygen -b 1024 -f /etc/ssh/ssh_host_rsa_key -t rsa -N ""
ssh-keygen -b 1024 -f /etc/ssh/ssh_host_dsa_key -t dsa -N ""
ssh-keygen -b 521 -f /etc/ssh/ssh_host_ecdsa_key -t ecdsa -N ""
ssh-keygen -b 1024 -f /etc/ssh/ssh_host_ed25519_key -t ed25519 -N ""

#nmcli c modify enp1s0 connection.autoconnect true

# Don't ask me why, but the nmcli command above doesn't work in a post
# installation.
sed -i -e '/autoconnect/d' /etc/NetworkManager/system-connections/enp1s0.nmconnection
%end

poweroff