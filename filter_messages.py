"""
Receive data from Pupil using ZMQ.
"""
import zmq
import os, sys
import time
from msgpack import loads


#updates by Adithya
#creating a fifo file
#path = "/tmp/gazeFifo"
#os.mkfifo(path)

context = zmq.Context()
# open a req port to talk to pupil
addr = '127.0.0.1'  # remote ip or localhost
req_port = "50020"  # same as in the pupil remote gui
req = context.socket(zmq.REQ)
req.connect("tcp://{}:{}".format(addr, req_port))
# ask for the sub port
req.send_string('SUB_PORT')
sub_port = req.recv_string()

# open a sub port to listen to pupil
sub = context.socket(zmq.SUB)
sub.connect("tcp://{}:{}".format(addr, sub_port))

# set subscriptions to topics
# recv just pupil/gaze/notifications
#sub.setsockopt_string(zmq.SUBSCRIBE, 'pupil.')
sub.setsockopt_string(zmq.SUBSCRIBE, 'gaze')
# sub.setsockopt_string(zmq.SUBSCRIBE, 'notify.')
# sub.setsockopt_string(zmq.SUBSCRIBE, 'logging.')
# or everything:
# sub.setsockopt_string(zmq.SUBSCRIBE, '')

#open FIFO file for writing
#fifo = open(path,"w")

count = 0;

while True:
    try:
        topic = sub.recv_string()
        msg = sub.recv()
        msg = loads(msg, encoding='utf-8')
        #print("\n{}: {}".format(topic, msg))
        #print("\n{}".format(msg.get('norm_pos')[0])+","+format(msg.get('norm_pos')[1]))
        if count == 1000:
            print("%s,%s" % (msg.get('norm_pos')[0], msg.get('norm_pos')[1]),flush=True)
            count = 0;
        count = count + 1;
        #print ("%d count" % (count))
	#print("{}".format(msg.get('norm_pos')[0]),flush=True)
        #print("{}".format(msg.get('norm_pos')[1]),flush=True)
        #fifo.write("{}".format(msg.get('norm_pos')[0]))
        #fifo.write("{}".format(msg.get('norm_pos')))
        #time.sleep(1)
    except KeyboardInterrupt:
        #close the file, delete it from the directory and break
        #fifo.close()
        #os.remove(path)
        break
