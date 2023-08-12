import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime
import inspect    # getsourcefile
import os.path

the_bb = None

# Websocket server handler

class WebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        global web_main_test
        self.alive = True
        print 'New connection'
        self.send(".........")
        the_bb.the_handler = self   # tell the main thread we have a connection


    def send(self, string):
        print "Sending: " + string
        self.write_message(string)
       
    def on_message(self, message):
        print ("Received from WS:", message)
        tokens = message.split()

        if tokens[0] == "click":
            the_bb.onclick( (int(tokens[1]), int(tokens[2])) )
        
        
        elif tokens[0] == "game_type":
            the_bb.game_type = str(tokens[1])
        
        else:
            print "Got unknown message"
  
    def on_close(self):
        self.alive = False
        print 'Connection closed'
  
    def on_ping(self, data):
        print 'ping received:'
  
    def on_pong(self, data):
        print 'pong received:'
  
    def check_origin(self, origin):
        #print "-- Request from %s" %(origin)
        return True

class MainHandler(tornado.web.RequestHandler):
    def get(self, fname):
        self.render(fname)

class BinaryHandler(tornado.web.RequestHandler):
    def get(self, fname):
         #Add cache control headers to prevent caching of the image
                # Add cache control headers to prevent caching of the image
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.set_header("Pragma", "no-cache")
        self.set_header("Expires", "0")
        source_path = os.path.abspath(inspect.getsourcefile(lambda:14383421))
        source_dir = os.path.split(source_path)[0]    # that would be dirpath in python3
        fname_path = os.path.join(source_dir, fname)
        with open(fname_path, "rb") as f:
            data = f.read()
            self.write(data)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/(.*\.html)", MainHandler),
        (r"/(.*\.js)", MainHandler),   # warning: MIME type is text/html (I assume I shoudln't use self.render). Still effective.
        (r"/(.*\.css)", MainHandler),   # just for completeness. Also same warning.
        (r"/(.*\.gif)", BinaryHandler),
        (r"/(.*\.jpg)", BinaryHandler),
        (r'/ws', WebSocketServer),
    ])

def go(bb):
    global the_bb
    the_bb = bb
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print "Server Thread dead"

