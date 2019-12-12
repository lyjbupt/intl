#!/bin/bash
#===============================================================================
#
#          FILE:  idsid.sh
#
#         USAGE:  ./idsid.sh
#
#   DESCRIPTION:  Query idsid
#
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Li Yingjie (hero), yingjie.li@intel.com
#       COMPANY:  Intel Mobile Communication Ltd.
#       VERSION:  1.0
#       CREATED:  10/15/2019 09:05:07 AM CEST
#      REVISION:  ---
#===============================================================================

export HOSTNAME=corpad.glb.intel.com
export USERNAME='CCR\lyingjie'
export PASSWORD='Baby@01X'
export SEARCHBASE=(DC=corp,DC=intel,DC=com)
export QUERYSTRING=(name="Swaminathan, Muthukumar")
PORT=3268

echo -n "Your IDSID is: "
ldapsearch -h ${HOSTNAME} -p $PORT -D $USERNAME -w $PASSWORD -b "$SEARCHBASE" "$QUERYSTRING" | grep -w sAMAccountName | awk '{print $NF}'
