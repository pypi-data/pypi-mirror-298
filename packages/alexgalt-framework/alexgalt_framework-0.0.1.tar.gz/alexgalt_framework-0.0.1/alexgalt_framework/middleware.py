from webob import Request
import time


class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, req):
        pass

    def process_response(self, req, resp):
        pass

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


class TimeMiddleware(Middleware):
    def process_request(self, req):
        self.start_time = time.time()

    def process_response(self, req, res):
        end_time = time.time()
        total_time = end_time - self.start_time
        print(f"Total request time: {total_time:.4f} seconds")
        return res
