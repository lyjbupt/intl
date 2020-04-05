#!/bin/sh

set -ex

if [ ! -z "${SKIP_PROXY_SETTING}" ]; then
    echo "Skip proxy setting..."
    exit 0
fi

# The proxy below are Seoul proxy settings
# We use it as default proxy. 
# if you want to use another proxy address, please set 'proxyHost' and 'proxyPort' to yours
export proxyHost=${proxyHost:-10.112.1.184}
export proxyPort=${proxyPort:-8080}

export http_proxy="http://${proxyHost}:${proxyPort}/"
export https_proxy="http://${proxyHost}:${proxyPort}/"
export ftp_proxy="http://${proxyHost}:${proxyPort}/"
export socks_proxy="http://${proxyHost}:${proxyPort}/"

export no_proxy="$no_proxy,$NO_PROXY,sec.samsung.net,165.213.149.164,.samsung.net,codesamsung.com"
export no_proxy_for_maven_and_gradle=`echo $no_proxy | sed -e "s/,/|/g"`
# Add Seoul and Suwon campus ip range for avoiding proxy
export no_proxy_for_maven_and_gradle="$no_proxy_for_maven_and_gradle|10.252.*|10.113.*|10.*"

export CERTIFICATE_FILE=${HOME}/SRnD_Web_Proxy.crt
# It is only using for debian based os
export SHARE_CERTIFICATE_FILE=/usr/local/share/ca-certificates/SRnD_Web_Proxy.crt

# Write Seoul RnD Proxy Cert file
cat <<EOT >> ${CERTIFICATE_FILE}
-----BEGIN CERTIFICATE-----
MIIEIzCCAwugAwIBAgIBADANBgkqhkiG9w0BAQUFADCBqzELMAkGA1UEBhMCa3Ix
DjAMBgNVBAgMBVNlb3VsMRwwGgYDVQQKDBNTYW1zdW5nIEVsZWN0cm9uaWNzMRkw
FwYDVQQDDBBTZW91bCBSJkQgQ2FtcHVzMRIwEAYDVQQHDAlTZW9jaG8tZ3UxGTAX
BgNVBAsMEFNlb3VsIFImRCBDYW1wdXMxJDAiBgkqhkiG9w0BCQEWFXByb3h5LnNl
bEBzYW1zdW5nLmNvbTAeFw0xNTEwMTQwODU5MDlaFw0zNTEwMTUwODU5MDlaMIGr
MQswCQYDVQQGEwJrcjEOMAwGA1UECAwFU2VvdWwxHDAaBgNVBAoME1NhbXN1bmcg
RWxlY3Ryb25pY3MxGTAXBgNVBAMMEFNlb3VsIFImRCBDYW1wdXMxEjAQBgNVBAcM
CVNlb2Noby1ndTEZMBcGA1UECwwQU2VvdWwgUiZEIENhbXB1czEkMCIGCSqGSIb3
DQEJARYVcHJveHkuc2VsQHNhbXN1bmcuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAvgEjYbjS/8XZHwu1Vdq0iDNbLNuzmFQb+GPdWYQlWqXOZb+K
V0xrHqaYeThIdcmaMmJDsCpXeXGQn8kz54iNIrVB25ZfyLhVNjr+A1FUnbq2N9xL
TH3fssovccghEuqT5TCMghjt2q2239SJ4AEFBQHkNvyrTzHy8itOD4AZiJZXIFNm
HCpzO4oi88A/3AXZ7Y2FjVLSTfbcA0gH3Jaf/TLwOqwj4/2y6gbMt/OPerek/kDH
AAWdGZCmJYwCtB+55Tl/iX8kelvJjVWMK9pZ9/naKW71ZkKmEXQ6O0arFP0HEYAR
5kxCKUxlHzQRRpmTsSAi2ri9Dg41RgGsQystjQIDAQABo1AwTjAdBgNVHQ4EFgQU
j9qoT6I0gGeg/93PMLb/OaGiRmMwHwYDVR0jBBgwFoAUj9qoT6I0gGeg/93PMLb/
OaGiRmMwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAN3SatWdZXhJA
7UIFoEqhiVMdKhzvu9nI3rIuAZzYMAtNsiSWqNgxC2JL/cS2YayjzXMuiJwPVDvs
6uyb02AmBj25ztA2Y1BHLBbEDhqdiuUUzxdELx0wWwZqU+ovD/jNz51OuL72mh4b
LxoUFQ+pmdtRUdqr0UGyC+28y3jw1DsvAQZBFWTS2AOxq57KpHBkOUcg1AT9xrYF
8FCKeSJwgt65GqYbSxmG3s5PXIp0pmQgDFbAdWc+ioQeR45eDUL4wY+k2xZTPrZO
vSsa1G1vxjAuzMthR4NvKi+vnTOLY1O8KvZ4oNhLbJoJvx/5zLvAll4pHR7ylu4g
phRAhQcRxA==
-----END CERTIFICATE-----
EOT

touch ~/.bashrc
# Bash proxy setting
echo "export http_proxy=\"${http_proxy}\"" | tee -a $BASH_ENV
echo "export https_proxy=\"${https_proxy}\"" | tee -a $BASH_ENV
echo "export no_proxy=$no_proxy" | tee -a $BASH_ENV
echo "export HTTP_PROXY=\"${http_proxy}\"" | tee -a $BASH_ENV
echo "export HTTPS_PROXY=\"${https_proxy}\"" | tee -a $BASH_ENV
echo "export NO_PROXY=$no_proxy" | tee -a $BASH_ENV
echo "export proxyHost=$proxyHost" | tee -a $BASH_ENV
echo "export proxyPort=$proxyPort" | tee -a $BASH_ENV
echo "export CERTIFICATE_FILE=$CERTIFICATE_FILE" | tee -a $BASH_ENV
echo "export SHARE_CERTIFICATE_FILE=$SHARE_CERTIFICATE_FILE" | tee -a $BASH_ENV
echo "source $BASH_ENV" | tee -a ~/.bashrc

# apt-get setting
# It is only using for debian based os
if [ -f "/etc/debian_version" ]; then
    APT_CONF=/etc/apt/apt.conf.d/80proxy
    if `sudo -n true` ; then
        echo "Acquire::http::proxy \"${http_proxy}\";" | sudo tee /etc/apt/apt.conf.d/80proxy
        echo "Acquire::https::proxy \"${https_proxy}\";" | sudo tee -a /etc/apt/apt.conf.d/80proxy
        echo "Acquire::ftp::proxy \"${ftp_proxy}\";" | sudo tee -a /etc/apt/apt.conf.d/80proxy
        echo "Acquire::socks::proxy \"${socks_proxy}\";" | sudo tee -a /etc/apt/apt.conf.d/80proxy
    elif [ -w "/etc/apt/apt.conf.d/" ]; then
        echo "Acquire::http::proxy \"${http_proxy}\";" | tee /etc/apt/apt.conf.d/80proxy
        echo "Acquire::https::proxy \"${https_proxy}\";" | tee -a /etc/apt/apt.conf.d/80proxy
        echo "Acquire::ftp::proxy \"${ftp_proxy}\";" | tee -a /etc/apt/apt.conf.d/80proxy
        echo "Acquire::socks::proxy \"${socks_proxy}\";" | tee -a /etc/apt/apt.conf.d/80proxy
    fi
fi

# Add Certificate
if [ `command -v java` ]; then
    if [ $JAVA_HOME ]; then
        echo "JAVA_HOME is exists"
    elif [ `command -v keytool` ]; then
        JAVA_HOME=$(dirname $(dirname $(dirname $(readlink -f `which keytool`))))
        echo "JAVA_HOME is not exists"
        echo "Use \"${JAVA_HOME}\" as JAVA_HOME"
    fi
    if [ $JAVA_HOME ]; then
        if `sudo -n true` ; then
            sudo -E ${JAVA_HOME}/jre/bin/keytool -noprompt -trustcacerts \
                -keystore ${JAVA_HOME}/jre/lib/security/cacerts -storepass changeit \
                -importcert -alias SRnD_cert -file ${CERTIFICATE_FILE} || true
        else
            ${JAVA_HOME}/jre/bin/keytool -noprompt -trustcacerts \
                -keystore ${JAVA_HOME}/jre/lib/security/cacerts -storepass changeit \
                -importcert -alias SRnD_cert -file ${SHARE_CERTIFICATE_FILE} || true
        fi
    fi
fi

if [ -f "/etc/debian_version" ]; then
    if [ -d "/usr/local/share/ca-certificates/" ]; then
        if `sudo -n true` ; then
            sudo cp ${CERTIFICATE_FILE} ${SHARE_CERTIFICATE_FILE}
            sudo -E update-ca-certificates
        elif [ -w "/usr/local/share/ca-certificates/" ]; then
            cp ${CERTIFICATE_FILE} ${SHARE_CERTIFICATE_FILE}
            update-ca-certificates
        fi
    fi
fi


if [ -f "/etc/alpine-release" ]; then    
    if [ -w "/usr/local/share/ca-certificates/" ]; then
        cp ${CERTIFICATE_FILE} ${SHARE_CERTIFICATE_FILE}
        apk update && apk add ca-certificates 
        update-ca-certificates
    fi 
fi

# Pip proxy setting
mkdir -p ~/.pip
PIP_CONF_PATH=~/.pip/pip.conf
touch ${PIP_CONF_PATH}
cat <<EOT >> ${PIP_CONF_PATH}
[global]
proxy=${http_proxy}
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
EOT

# anaconda setting
CONDA_RC=~/.condarc
touch $CONDA_RC
cat <<EOT >> $CONDA_RC
proxy_servers:
    http: ${http_proxy}
EOT

# npm proxy setting
NPMRC_PATH=~/.npmrc
touch ${NPMRC_PATH}
cat <<EOT >> ${NPMRC_PATH}
proxy=${http_proxy}
https-proxy=${http_proxy}
EOT

# yarn proxy setting
touch ~/.yarnrc
cat <<EOT >> ~/.yarnrc
proxy "${http_proxy}"
https-proxy "${http_proxy}"
EOT

# gradle proxy setting
mkdir -p ~/.gradle
touch ~/.gradle/gradle.properties
cat <<EOT >> ~/.gradle/gradle.properties
systemProp.http.proxyHost=${proxyHost}
systemProp.http.proxyPort=${proxyPort}
systemProp.http.nonProxyHosts=${no_proxy_for_maven_and_gradle}
systemProp.https.proxyHost=${proxyHost}
systemProp.https.proxyPort=${proxyPort}
systemProp.https.nonProxyHosts=${no_proxy_for_maven_and_gradle}
EOT

# maven proxy setting
mkdir -p ~/.m2
touch ~/.m2/settings.xml
cat <<EOT >> ~/.m2/settings.xml
<settings>
  <proxies>
    <proxy>
      <id>proxy-http</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>${proxyHost}</host>
      <port>${proxyPort}</port>
      <nonProxyHosts>${no_proxy_for_maven_and_gradle}</nonProxyHosts>
    </proxy>
    <proxy>
      <id>proxy-https</id>
      <active>true</active>
      <protocol>https</protocol>
      <host>${proxyHost}</host>
      <port>${proxyPort}</port>
      <nonProxyHosts>${no_proxy_for_maven_and_gradle}</nonProxyHosts>
    </proxy>
  </proxies>
</settings>
EOT
