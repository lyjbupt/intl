#!/bin/bash

. ~/.bashrc
set -e

Proj=('repo1' 'repo2')
Url='ssh://git@gitlab.devtools.intel.com:29418/lyingjie/'
for data in ${Proj[@]}
do
    echo Fetching ${data}
    git clone $Url${data}.git
done

for data in ${Proj[@]}
do
    echo Running ${data}
    cd $data && python main.py
    cd -
done
