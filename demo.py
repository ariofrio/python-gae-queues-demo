from apiclient.discovery import build

import base64
import urllib
import urllib2
import oauth2utils

# Get settings from "app/" directory (just for consistency)
import yaml
with open('app/app.yaml') as f:
	APP = yaml.safe_load(f)['application']
	# See for "s~": http://stackoverflow.com/a/7021985/237285
	PROJECT = "s~" + APP
with open('app/queue.yaml') as f:
	TASK_QUEUE = yaml.safe_load(f)['queue'][0]['name']

# Build API helper objects
service = build("taskqueue", "v1beta1", http=oauth2utils.http,
	discoveryServiceUrl="https://www.googleapis.com/discovery/v1/apis/taskqueue/v1beta1/rest")
queues = service.taskqueues()
tasks = service.tasks()

def get_count():
	demo_queue = queues.get(taskqueue=TASK_QUEUE, project=PROJECT, getStats=True).execute()
	return demo_queue['stats']['totalTasks']

def lease():
	leasedTasks = tasks.lease(taskqueue=TASK_QUEUE, project=PROJECT, leaseSecs=10, numTasks=1, body="").execute()
	return leasedTasks['items'][0]

def delete(id):
	tasks.delete(taskqueue=TASK_QUEUE, project=PROJECT, task=id).execute()

def main():
	print "querying size of queue: " + str(get_count())

	print "putting message into queue"
	urllib2.urlopen("http://" + APP + ".appspot.com/add", urllib.urlencode({'message': "demo data"}))
	print "querying size of queue: " + str(get_count())

	print "pulling message from queue:",
	task = lease()
	print base64.b64decode(task['payloadBase64'])
	print "querying size of queue: "  + str(get_count())

	print "deleting message from queue"
	delete(task['id'])
	print "querying size of queue: " + str(get_count())

if __name__ == '__main__':
	main()
