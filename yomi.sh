#!/bin/bash

while true; do
   case "$1" in
        -s|--setup)
            echo "Setting up containers..."
            # optional
            # podman pull pgadmin4:latest
            # podman run --name pgadmin4-web -p 5050:80 -e "PGADMIN_DEFAULT_EMAIL=root@root.com" -e "PGADMIN_DEFAULT_PASSWORD=root" -d pgadmin4:latest

            podman pull postgres:latest
            podman run --name yomi-dev-db0 -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root -e POSTGRES_DB=yomi_dev_db -d -p 5432:5432 postgres:latest

            # build python image
            podman build -t yomi-dev-fastapi backend/.
            # run image as container
            podman run --name yomi-fastapi -d -p 8000:8000 yomi-dev-fastapi:latest
            echo "Finished setting up"
            shift;;
        -r|--full-reset)
            #clean up image/container
            podman stop yomi-fastapi
            podman rm yomi-fastapi
            podman rmi yomi-dev-fastapi:latest

            # rebuild/run
            podman build -t yomi-dev-fastapi backend/.
            podman run --name yomi-fastapi -d -p 8000:8000 yomi-dev-fastapi:latest
            podman start yomi-fastapi
            shift;;
        *)
            break;;
    esac
done;
