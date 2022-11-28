#!/usr/bin/bash -vex

ISO="AlmaLinux-9.1-x86_64-minimal.iso"
URL="https://almalinux.mirror.letscloud.io/9.1/isos/x86_64"
DEST=/var/tmp

# Kickstart scripts
KS_DIR="kickstart"
KS_BASE="almalinux9.ks"

VIRT_NAME="pyktest"

if ! command -v "virt-install" ; then
    echo "virt-install not found, please install package virt-install"
    exit 1
fi

if ! test -f $DEST/$ISO; then
    curl -o $DEST/$ISO $URL/$ISO
fi

virsh destroy $VIRT_NAME || :
virsh undefine --remove-all-storage $VIRT_NAME || :

eval virt-install \
    --name ${VIRT_NAME} \
    --cpu host \
    --virt-type=kvm \
    --ram 2048 \
    --vcpus 1 \
    --disk size=8 \
    --nographics \
    --osinfo almalinux9 \
    --network user \
    --location="$DEST/$ISO" \
    --initrd-inject ${KS_DIR}/${KS_BASE} \
    --extra-args="\"inst.ks=file:/${KS_BASE} console=ttyS0,115200\"" \
    --destroy-on-exit
