START_SH_FILE=/home/ubuntu/catkin_ws/src/river/src/start.sh

while [ "$(hostname -I)" = "" ]; do
  echo -e "\e[1A\e[KNo network: $(date)"
  sleep 1
done

cd "/home/ubuntu/catkin_ws/src/river" && git reset --hard HEAD && git pull

echo "Permissions changed: START_SH_FILE"
sudo chmod 777 "$START_SH_FILE"

. "$START_SH_FILE"

cd "/home/ubuntu/catkin_ws" && catkin_make && source devel/setup.sh

cd "/home/ubuntu/catkin_ws/src/river/src"

#systemctl daemon-reload
#sudo systemctl restart apache2