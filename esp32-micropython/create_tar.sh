#!/bin/bash

DEPLOY_DIR="deploy"

[ ! -d "${DEPLOY_DIR}" ] && echo "Deploy dir does not exists!" && exit 1

[ -e "${DEPLOY_DIR}.tar" ] && echo "Removing old tar" && rm "${DEPLOY_DIR}.tar"


echo "Change dir"
cd "$DEPLOY_DIR"

echo "Making archive"
tar cvf "../${DEPLOY_DIR}.tar" *

cd "${OLDPWD}"

echo "All Done..."
