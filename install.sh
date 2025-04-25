#!/bin/bash

echo -e "Enter in sudo mode to install...\n"

pip install -r requirements.txt

sudo apt update && sudo apt install golang -y

export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
echo 'export GOROOT=/usr/lib/go' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export PATH=$GOPATH/bin:$GOROOT/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

go install github.com/lc/gau/v2/cmd/gau@latest

go install github.com/projectdiscovery/katana/cmd/katana@latest

sudo chmod +x damcrawler.py
sudo cp damcrawler.py /usr/local/bin/damcrawler

echo -e "\nDone.\n"
