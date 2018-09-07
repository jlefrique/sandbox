#!/bin/sh

CPUFREQ_PATH="/sys/devices/system/cpu/cpu0/cpufreq"

RANGE=4

random_sleep () {
    delay=$RANDOM
    let "delay %= $RANGE"
    echo "Delay $delay"
    sleep $delay
}

set_frequency () {
    echo "Frequency $1"
    echo $1 > ${CPUFREQ_PATH}/scaling_setspeed
}


echo "userspace" > ${CPUFREQ_PATH}/scaling_governor

while true; do
    set_frequency 1000000
    random_sleep
    set_frequency 800000
    random_sleep
    set_frequency 300000
    random_sleep
    set_frequency 720000
    random_sleep
    set_frequency 600000
    random_sleep
    set_frequency 300000
    random_sleep
done
