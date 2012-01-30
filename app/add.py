from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import taskqueue

TASK_QUEUE = "demo"
q = taskqueue.Queue(TASK_QUEUE)

class AddPage(webapp.RequestHandler):
    def post(self):
        q.add(taskqueue.Task(payload=self.request.get('message'), method='PULL'))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Success!')

application = webapp.WSGIApplication([('/add', AddPage)])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
