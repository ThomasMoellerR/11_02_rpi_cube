import paho.mqtt.client as pmc
import time
import queue





class c_mqtt:

    def __init__(self, hostname = "192.168.178.52", port = "1880", sub_list = []):
        self.hostname = hostname
        self.port = port
        self.try_to_connect = True
        self.sub_list = sub_list
        self.connected = False
        self.q = queue.Queue()
        self.was_connected = False

        self.client = pmc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):

        # rc = result code
        if rc == 0:
            print("Successfully connected to broker")
            self.connected = True
        else:
            print("Error while trying to connect to broker")
            self.connected = False


        # subscribe
        for topic in self.sub_list:
            self.client.subscribe(topic)


    def on_message(self, client, userdata, msg):
        t = msg.topic
        m = msg.payload.decode("utf-8")
        #print("Received", t + " "+ m)
        self.q.put((t, m))


    def loop(self):

        if self.try_to_connect:

            if self.was_connected == True:
                time.sleep(1)

            print("Try to connect to broker", self.hostname, int(self.port))
            try:
                self.client.connect(self.hostname, int(self.port), 60)
                self.try_to_connect = False
                self.connected = True
                self.was_connected = True
            except Exception as e:
                print(e)
                self.connected = False

        if self.connected:
            try:
                self.client.loop_forever()
            except Exception as e:
                print(e)
                self.try_to_connect = True
                self.connected = False
    

    def pub(self, topic, msg):
        if self.connected:
            self.client.publish(topic, msg, qos=0, retain=False)




    def set_connection_state(self, state):
        self.connected = state

    def get_connection_state(self):
        return self.connected

    def sub(self, topic):
        self.sub_list.append(topic)

    def empty(self):
        return self.q.empty()     

    def get(self):
        return self.q.get()


