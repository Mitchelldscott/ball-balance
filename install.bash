
sudo apt update

sudo xargs apt install -y --no-install-recommends dependencies.txt



curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py

sudo python3 get-pip.py

rm get-pip.py


pip3 install -r python3_requirements.txt