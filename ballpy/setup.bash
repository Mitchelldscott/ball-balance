echo -e 'Setting up ballnet'

echo -e 'Exorting environment variables'
export PROJECT_ROOT=/home/pi/ball-balance/
export RPI_4_ADDRESS=pi@raspberrypi.local


echo -e 'Setting up Aliases'
alias clean='rm -rf ${PROJECT_ROOT}/MATLAB/*.jpg && rm -rf ${PROJECT_ROOT}/ballpy/data/*'
alias deploy='scp -r ${HOME}/ball-balance/ballpy ${RPI_4_ADDRESS}:/home/pi/ball-balance/'
alias ssh-rpi='ssh -X -t pi@raspberrypi.local "cd /home/pi/ball-balance; source ballpy/setup.bash; /bin/bash"'

echo -e 'Setup Done'