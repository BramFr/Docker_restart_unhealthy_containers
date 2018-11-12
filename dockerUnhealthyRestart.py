#!/usr/bin/python3
import docker
import os.path
import json
import time

client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_file_location = '/usr/bin/docker'

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
      try:
        healthyStatus = client.inspect_container(container['Id'])['State']['Health']['Status']
        if healthyStatus != "healthy":
          client.restart(container['Id'])
      except:
        pass
 
    
if __name__ == '__main__':
    main()
    
