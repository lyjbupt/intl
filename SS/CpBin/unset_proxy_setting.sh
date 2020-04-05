#!/bin/sh

# This script cleans up by to undoing the changes done by `set_proxy_settings.sh`
# This is normally needed inside docker containers that need the proxy settings to configure itself
# but do not need the proxy settings after.
# This should be run at the end of your build.

set -ex

unset http_proxy
unset https_proxy
unset ftp_proxy
unset socks_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset proxyHost
unset proxyPort

# Remove all proxy configs for repositories
SUDO=""
if `sudo -n true` ; then
    SUDO="sudo"
fi
${SUDO} sed -i '/source $BASH_ENV/d' ~/.bashrc # remove the bashenv source addition in the set_proxy_settings.sh
${SUDO} rm -rf /etc/apt/apt.conf.d/80proxy \
    ~/.pip/pip.conf \
    ~/.condarc \
    ~/.npmrc \
    ~/.yarnrc \
    ~/.gradle/gradle.properties \
    ~/.m2/settings.xml
