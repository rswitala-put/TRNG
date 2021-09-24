import pyaudio
import wave
import random
import matplotlib.pyplot as plt


CHUNK = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "WAVE_OUTPUT_FILENAME"
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("*** recording ***")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("*** done recording ***")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
binary_data = wf.readframes(wf.getnframes())  #
gausse = open("gausse", "a+")
list_of_numbers_before_processing = []
masks = 255

for i in range(100000):
    list_of_numbers_before_processing.append(int.from_bytes(binary_data[15000 + i:15002 + i], byteorder="big") & masks)
    b = (int.from_bytes(binary_data[15000 + i:15002 + i], byteorder="big") & masks)
    gausse.write(str(i) + ". " + str(int(b)) + "\n")

plt.hist(list_of_numbers_before_processing)

wf.close()
gausse.close()

counter = []
gausse_2 = open("gausse_v2", "a+")
for i in range(256):
    c = list_of_numbers_before_processing.count(i)
    gausse_2.write(str(i) + ". " + str(int(c)) + "\n")
    counter.append(c)

bits = open("bity.txt", "a+")
bits.write(str(binary_data))
bits.close()

list_of_numbers_before_processing = int.from_bytes(binary_data[15000:15025], byteorder="big")
mask = 255
seed = int(list_of_numbers_before_processing) & mask
random.seed(seed)

# stałe z mersena, które sa potrzebne do algorytmu
r = 31
m = 397
n = 624
w = 32
a = 0x9908B0DF
u = 11
d = 0xFFFFFFFF
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18
f = 1812433253

my_number = [0 for i in range(n)]
index = n + 1
lower_mask = 0x7FFFFFFF
upper_mask = 0x80000000


def seed_(seed):
    my_number[0] = seed
    for i in range(1, n):
        temp = f * (my_number[i - 1] ^ ((my_number[i - 1]) >> (w - 2))) + i
        my_number[
            i] = temp & 0xff  # zmiana z 8 bitów na 32 w zależności od długości maski (dopisać 6x'f' i będzie 32 bitowe


def get_number():
    global index
    if index >= n:
        mix()
        index = 0

    y = my_number[index]
    y = y ^ (y >> u)
    y = y ^ ((y << t) & c)
    y = y ^ ((y << s) & b)
    y = y ^ (y >> l)

    index += 1
    return y & 0xff  # zmiana z 8 bitów na 32 w zależności od długości maski


def mix():
    for i in range(0, n):
        x = (my_number[i] & upper_mask) + (my_number[(i + 1) % n] & lower_mask)
        x_bit = x >> 1
        if (x % 2) != 0:
            x_bit = x_bit ^ a
        my_number[i] = my_number[(i + m) % n] ^ x_bit


seed_(seed)
list_of_numbers_after_processing = []
number = 0
file_with_numbers_after_processing = open("numbers.txt", "w+")
for i in range(100000):
    number = get_number()
    list_of_numbers_after_processing.append(number)
    file_with_numbers_after_processing.write(str(i) + ". " + str(number) + "\n")
file_with_numbers_after_processing.close()

plt.hist(list_of_numbers_after_processing)
plt.show()
