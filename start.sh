export DJANGO_IP=192.168.0.105:8000
#export DISPLAY=:1.0
#export SCREEN_HEIGHT=1080
export PROFILE_ID=64b820cc82caa438efb3716e
export TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGI2YWJmNWQyNmU2YzYxNWUxMDI5ZTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGI2YWMyYmE4YmIyYzgzYWYyZDdlNzIifQ.EgiklJY15EaL4CZPPvCvYBXYReGZVRNyeuUogV8MW1M
#docker run -e DJANGO_IP=$DJANGO_IP -e SCREEN_HEIGHT=$SCREEN_HEIGHT -e PROFILE_ID=$PROFILE_ID -e TOKEN=$TOKEN go-test
#docker run  -e DJANGO_IP=$DJANGO_IP -p 6080:80 gologin-test3
export SCREEN_WIDTH=1920
export SCREEN_HEIGHT=1080
#export PROFILE_ID=yU0Pr0f1leiD
#export TOKEN=yU0token

#function run
run() {
    number=$1
    shift
    for i in `seq $number`; do
      $@
    done
}

run 25 docker run -e DJANGO_IP=$DJANGO_IP -e SCREEN_WIDTH=$SCREEN_WIDTH -e SCREEN_HEIGHT=$SCREEN_HEIGHT -e PROFILE_ID=$PROFILE_ID -e TOKEN=$TOKEN --rm -ti -p 5901:5901 -p 3000:3000 gologin-test4
