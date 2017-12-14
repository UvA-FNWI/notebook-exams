#!/bin/bash

echo ""
echo "Creating machine..."
docker-machine create \
	--driver google \
	--google-project complete-flag-183314 \
	--google-zone europe-west1-b \
	--google-machine-type $2 \
	--google-disk-size 15 \
	--engine-install-url=https://web.archive.org/web/20170623081500/https://get.docker.com $1 >> provision-$1.log 2>&1

sleep 10

echo ""
echo "Installing NFS..."
docker-machine ssh $1 'sudo apt-get install -y nfs-common; \
sudo wget --quiet https://github.com/ContainX/docker-volume-netshare/releases/download/v0.18/docker-volume-netshare_0.18_amd64.deb; \
sudo dpkg -i docker-volume-netshare_0.18_amd64.deb; \
sudo service docker-volume-netshare start; \
sudo update-rc.d docker-volume-netshare defaults;' >> provision-$1.log 2>&1

echo ""
echo "Activating NFS"
docker-machine ssh $1 'sudo docker run -i --volume-driver=nfs -v 10.132.0.2/:/mount ubuntu echo "NFS activated";' >> provision-$1.log 2>&1

echo ""
echo "Pulling notebook image..."
docker-machine ssh $1 'sudo docker pull jessesar/uva-notebook:latest;' >> provision-$1.log 2>&1

echo ""
echo "Joining Swarm..."
docker-machine ssh $1 'sudo docker swarm join --token SWMTKN-1-04b04xpjpms12zh73qgklz1517spag14zwif8gqsrce29akiya-5hn4wpsbo55p39496af70c6x4 10.132.0.2:2377;' >> provision-$1.log 2>&1

echo ""
echo "----------------------------"
echo "Worker '$1' provisioned."
echo "See provision-$1.log for logs."
echo ""