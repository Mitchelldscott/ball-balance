echo -e 'Setting up ballnet'

echo -e 'Exporting environment variables'
export PROJECT_ROOT=${PWD}
export RPI_4_ADDRESS=pi@raspberrypi.local
if [[ "${PYTHONPATH}" != "${PROJECT_ROOT}"* ]]; then
	export PYTHONPATH=${PROJECT_ROOT}/ballpy/lib:${PYTHONPATH}
fi

echo -e 'Setting up Aliases'
alias clean='rm -rf ${PROJECT_ROOT}/ballpy/data/*'
alias deploy='scp -r ${HOME}/ball-balance/ballpy ${RPI_4_ADDRESS}:/home/pi/ball-balance/'
alias pull-data='scp -r ${RPI_4_ADDRESS}:/home/pi/ball-balance/ballpy/data/ ${PROJECT_ROOT}/ballpy'
alias ssh-rpi='ssh -X -t pi@raspberrypi.local "cd /home/pi/ball-balance; source ballpy/setup.bash; /bin/bash"'

