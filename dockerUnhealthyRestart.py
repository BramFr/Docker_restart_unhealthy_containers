#!/usr/bin/python3
import docker
import os
import json
import time
from slackclient import SlackClient


client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_file_location = '/usr/bin/docker'
slack_token = "SLACK_API_TOKEN"
sc = SlackClient(slack_token)


def main():
  if queryFileLocation():
    while True:
      queryStatusContainer()
      time.sleep(60)

def queryFileLocation():
  if os.path.exists(docker_file_location):
    return os.path.exists(docker_file_location)
  else:
    print("Docker is not installed. Please install first!")
    exit()

def queryStatusContainer():
    for container in client.containers():
      healthyStatus = None
      try:
        healthyStatus = client.inspect_container(container['Id'])['State']['Health']['Status']
      finally:
        if healthyStatus != "healthy":
          client.restart(container['Id'])
          if slack_token != "SLACK_API_TOKEN":
            sc.api_call(
              "chat.postMessage",
              channel="zabbix_monitor",
              text="Container {} was unhealthy.".format(container['Names']),
              user="PythonScript"
              )
 
    
if __name__ == '__main__':
    main()
    
