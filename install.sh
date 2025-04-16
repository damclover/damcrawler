echo -e "Enter in sudo mode to instal..\n"
sudo go install github.com/lc/gau/v2/cmd/gau@latest
sudo export PATH="$HOME/go/bin:$PATH"

sudo chmod +x damcrawler.py
sudo cp damcrawler.py /usr/local/bin/damcrawler
