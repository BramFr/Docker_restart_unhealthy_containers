#!/usr/bin/python3
from slackclient import SlackClient
import time
import json
import os
import docker



client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_file_location = '/usr/bin/docker'
slack_token = "SLACK_API_TOKEN"
slack_channel = "ChangeMe"
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
            print(container['Id'])
            healthyStatus = client.inspect_container(
                container['Id'])['State']['Health']['Status']
        except:
            pass
        finally:
            if healthyStatus == "unhealthy":
                client.restart(container['Id'])
                if slack_token != "SLACK_API_TOKEN":
                    sc.api_call(
                        "chat.postMessage",
                        channel="{}".format(slack_channel),
                        text="Container {} was unhealthy.".format(
                            container['Names']),
                        user="PythonScript"
                    )


if __name__ == '__main__':
    main()
