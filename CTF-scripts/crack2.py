import pyshark

# load pcap fule for dissection
cap = pyshark.FileCapture("capture.pcap")
# dummy variable to make exception handling easier
x = 0

# 8 - right
# 2 - down
# 4 - left
# 1 - up

# data to make deciphering more easy
Data = [
    "ABCDEFGHIJ",
    "KLMNOPQRST",
    "UVWXYZabcd",
    "efghijklmn",
    "opqrstuvwx",
    "yz01234567",
    "89.,-_:;{}"
]

#position of the cursor and empty result array
position = [0,0]
res = []

# go over all the packets
for n in cap:
    # check the ones when actual controller data is transmitted
    if int(n.number) > 123:# and int(n.number) < 360:
        # handle the exceptions when there isn't extra data being handed over
        try:
            # turn data into integer
            data = n[1].usb_capdata.split(":")
            # map integer data to textual data to make deciphering easier
            if int(data[5]) != 0 and len(data) > 8:
                # switch case for mapping
                if int(data[5]) == 8:
                    # print("right")
                    position[0] += 1
                elif int(data[5]) == 2:
                    # print("down")
                    position[1] += 1
                elif int(data[5]) == 4:
                    # print("left")
                    position[0] -= 1
                elif int(data[5]) == 1:
                    # print("up")
                    position[1] -= 1
            # If the ok button is pressed print the current character
            if int(data[4]) != 0 and len(data) > 8:
                res.append(Data[position[1]][position[0]])
            
            # handle the boundchecks
            if position[0] > 9:
                position[0] = 0
            elif position[0] < 0:
                position[0] = 9
            elif position[1] > 7:
                position[1] = 0
            elif position[1] < 0:
                position[1] = 7
        # Handle exception errors if the required fields aren't in the capture packet
        except Exception:
            x+=0

for i in res:
    print(i, sep="",end="")