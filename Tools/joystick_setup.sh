#!/bin/bash

source /opt/ros/melodic/setup.sh

usage(){
    echo "USAGE: ${0} [OPTIONS]"
    echo
    echo "OPTIONS"
    echo
    echo "   -h, --help   Display this message"
    echo "   -t, --test   Test to see if the joystick input is being read"
    echo
}

# Checking super user
if [[ ${UID} -ne 0 ]]; then echo "You don't have permission. Please try with root user" >&2; exit 1; fi

OPTIONS=$(getopt -o h,t --long help,test -- "$@")
if [[ ${?} -ne 0 ]]; then usage >&2; exit 1; fi

eval set -- "$OPTIONS"
TESTING=false
while true; do
    case "$1" in
	-h | --help) usage; exit 0; shift ;;
	-t | --test) TESTING=true; shift ;;
	--) shift; break ;;
    esac
done

JOYSTICKS=$(ls /dev/input | grep js)
INPUTS=$(echo $JOYSTICKS | wc -w)

# Checking if there's at least one joystick available
if [[ $INPUTS -lt 1 ]]; then
    echo "There aren't any joystick inputs available. Plug in one and try again." >&2
    exit 1
fi

JOYSTICK=$(echo "$JOYSTICKS" | head -1)

# Checking if user wants to test joystick input
if [ "$TESTING" = true ]; then /usr/bin/jstest /dev/input/"${JOYSTICK}"; exit 0; fi

# Checking if roscore if running before performing following steps
ROSCORE_PS=$(ps -ef | grep roscore | wc -l)
if [[ "$ROSCORE_PS" -lt 2 ]]; then 
    echo "roscore is yet not running, starting roscore now. This may take a few minutes"
    /opt/ros/melodic/bin/roscore &
fi

echo "roscore has started running, checking to see if rosout node is ready."

# Waiting until rosout node is up and running
ROSOUT=false
while [ "${ROSOUT}" = false ]; do
    ROSOUT_PS=$(ps -ef | grep rosout | wc -l)
    if [[ "$ROSOUT_PS" -gt 1 ]]; then ROSOUT=true; fi
done

echo "rosout node is up and running, continuing with configuration"

# Making configurations
chmod a+rw /dev/input/"${JOYSTICK}"
/opt/ros/melodic/bin/rosparam set joy_node/dev "/dev/input/${JOYSTICK}"
sleep 1
/opt/ros/melodic/bin/rosrun joy joy_node &
sleep 2

echo "Joystick configured successfully"
exit 0

