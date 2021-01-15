# sample object representing the time the sample was taken and the SDA/SCL values
# this is useful to avoud indexing in large arrays
class Sample:
    def __init__(self, time, scl, sda):
        self.time = time
        self.scl = scl
        self.sda = sda

# open .csv file and process data
f = open("samples.csv")
lines = f.readlines()

# sample array containing all our data
samples = []

# process data by appending all of our sample objects to a common array
for i in range(1,len(lines)):
    sample_data = lines[i].split(",")
    # add sample data to our samples  
    samples.append( Sample(float(sample_data[0]), int(sample_data[1]), int(sample_data[2]) ))

# result array containing binary values of sent data
res = []

# go over data but only if the time is between two window endpoints between which communication occurs
prev = 0
for sample in samples:
    # test if we're between required time values
    if sample.time > 2.866448 and sample.time < 2.869011:
        # if we are then process the data
        if sample.scl == 1 and prev == 0:
            res.append(sample.sda)
    # save current samples clock value
    prev = sample.scl


# ack counter to get if we need the byte or not
ack = 0
part = []
# iterate over bits
for b in res:
    if ack == 8:
        if b == 0:
            # print byte if the ack's calue is correct
            for bit in part:
                print(bit,sep="", end="")
        ack = 0
        print("\n")
    else:
        # add bit to partial string
        part.append(str(b))
        ack += 1