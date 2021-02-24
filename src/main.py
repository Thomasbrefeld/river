#!/usr/bin/env python

import os
import rospy
import json
import time
import pathlib
import logging
from std_msgs.msg import String
from std_msgs.msg import Int8
from rosgraph_msgs.msg import Log
from std_msgs.msg import Bool

dataFile = "/home/ubuntu/catkin_ws/src/river/src/dataTemp.json"
logFile = "/home/ubuntu/catkin_ws/src/river/src/main.log"

lastUpdate = None
data = None

assert os.path.exists(dataFile), 'No such file: \'data.json\''

def update():
	try:
		global lastUpdate
		global data

		with open(dataFile) as file:
			data = json.load(file)

		lastUpdate = pathlib.Path(dataFile).stat().st_mtime
	except Exception as e:
		print("Update Function Failed:", e)


def textMsgCB(msg):
	try:
		data["show"]["text"]["msg"] = str(msg.data)

		jsonObj = json.dumps(data, indent = 4)

		with open(dataFile, "w") as file:
			file.write(jsonObj)
		update()
	except:
		print("Function error: textMsgCB, in main.py!")

def textColorCB(msg):
	try:
		if (msg.data)
		data["show"]["text"]["color"] = str(msg.data)

		jsonObj = json.dumps(data, indent = 4)

		with open(dataFile, "w") as file:
			file.write(jsonObj)
		update()
	except:
		print("Function error: textColorCB, in main.py!")

def statusEnabledCB(msg):
	try:
		data["show"]["status"]["enabled"] = msg.data

		jsonObj = json.dumps(data, indent = 4)

		with open(dataFile, "w") as file:
			file.write(jsonObj)

		update()
	except:
		print("Function error: statusEnabledCB, in main.py!")

def statusNumCB(msg):
	try:
		data["show"]["status"]["msg"] = str(msg.data)

		jsonObj = json.dumps(data, indent = 4)

		with open(dataFile, "w") as file:
			file.write(jsonObj)

		update()
	except:
		print("Function error: statusNumCB, in main.py!")

def statusColorCB(msg):
	try:
		data["show"]["status"]["color"] = str(msg.data)

		jsonObj = json.dumps(data, indent = 4)

		with open(dataFile, "w") as file:
			file.write(jsonObj)
		update()
	except:
		print("Function error: statusColorCB, in main.py!")

def autoEnabledCB(msg):
	try:
		data["auto"]["enabled"] = msg.data

		jsonObj = json.dumps(data, indent = 4)

		with open(dataFile, "w") as file:
			file.write(jsonObj)

		update()
	except:
		print("Function error: autoEnabledCB, in main.py!")

def logCB(msg):
	try:
		if data["auto"]["enabled"]:
			data["auto"]["data"]["msgs"].append(
				{"level": msg.level, 
				"ROStime": msg.header.stamp.to_sec(), 
				"PItime": int(time.time()), 
				"name": msg.name, 
				"topics": msg.topics, 
				"msg": msg.msg})

			jsonObj = json.dumps(data, indent = 4)

			with open(dataFile, "w") as file:
				file.write(jsonObj)

			update()
	except:
		print("Function error: logCB, in main.py!")

def enabledCB(msg):
	try:
		if data["auto"]["enabled"]:
			data["auto"]["data"]["dbw_enabled"] = msg.data

			jsonObj = json.dumps(data, indent = 4)

			with open(dataFile, "w") as file:
				file.write(jsonObj)

			update()
	except:
		print("Function error: enabledCB, in main.py!")

if __name__ == '__main__':
	rospy.init_node('display_node')
	print("display_node started!")

	update()
	data["auto"]["data"]["msgs"] = []

	jsonObj = json.dumps(data, indent = 4)

	with open(dataFile, "w") as file:
		file.write(jsonObj)

	rospy.Subscriber("display/text/msg", String, textMsgCB)
	rospy.Subscriber("display/text/color", String, textColorCB)

	rospy.Subscriber("display/status/enabled", Bool, statusEnabledCB)
	rospy.Subscriber("display/status/num", Int8, statusNumCB)
	rospy.Subscriber("display/status/color", String, statusColorCB)

	rospy.Subscriber("display/auto/enabled", Bool, autoEnabledCB)

	rospy.Subscriber("rosout", Log, logCB)
	rospy.Subscriber("/vehicle/dbw_enabled", Bool, enabledCB)

	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		if (lastUpdate != pathlib.Path(dataFile).stat().st_mtime):
			update()
		rate.sleep()
