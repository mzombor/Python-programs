from pwn import remote
import paho.mqtt.client as mqtt

# "34.241.113.222", 32805
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# Get arguments to the operators based on input basically split the input into post and pre operator parts
def get_arguments(msg):
    print("9")

# Parse the part after the world domination string, return results
def parse(msg):
    argument1 = ""
    argument2 = ""
    mask=""
    part = 0
    # Test what bitwise operation needs to be done
    if "NOT" in msg:
        # Get arguments
        argument1 = msg[6:-3]
        # create mask to get not
        for _ in range(len(argument1)):
            mask += "1"
        print((int(mask,2) ^ int(argument1,2)).to_bytes(1,'big').decode(),sep="")
    elif "XOR" in msg:
        # Get arguments
        argument1 = msg.split("XOR")[0][2:-1]
        argument2 = msg.split("XOR")[1][1:-3]
        print((int(argument1, 2) ^ int(argument2, 2)).to_bytes(1,'big').decode(),sep="")
    elif "NAND" in msg:
        # Get arguments
        argument1 = msg.split("NAND")[0][2:-1]
        argument2 = msg.split("NAND")[1][1:-3]
        # get partial result
        part = int(argument1,2) & int(argument2,2)
        # create mask to get not
        for _ in range(len(argument1)):
            mask += "1"
        print((int(mask, 2) ^ part).to_bytes(1,'big').decode(),sep="")
    elif "AND" in msg:
        # Get arguments
        argument1 = msg.split("AND")[0][2:-1]
        argument2 = msg.split("AND")[1][1:-3]
        print((int(argument1, 2) & int(argument2, 2)).to_bytes(1,'big').decode(),sep="")
    elif "OR" in msg:
        # Get arguments
        argument1 = msg.split("OR")[0][2:-1]
        argument2 = msg.split("OR")[1][1:-3]
        print((int(argument1, 2) | int(argument2, 2)).to_bytes(1,'big').decode(),sep="")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    # parse the data
    parse(str(msg.payload))
    #print(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("34.241.113.222", 32805, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
