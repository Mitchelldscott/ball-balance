
echo -e "updating and installing dependencies"
sudo apt update

sudo xargs apt install -y --no-install-recommends dependencies.txt


echo -e "installing pip and python requirements"

curl https://bootstrap.pypa.io/pip/3.9/get-pip.py -o get-pip.py

sudo python3 get-pip.py

rm get-pip.py


pip3 install -r python3_requirements.txt