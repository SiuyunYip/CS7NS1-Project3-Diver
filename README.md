# CS7NS1-Project3-Diver

You can run this whole project by runing runme.sh

To run this project manually on local, plz make sure you have python virtual environment under the directory CS7NS1-Project3-Diver named as pj3-env
or
you can change the first line of router.py and device_1/2.py (i.e., ../pj3-env/bin/python) to your own interpreter

After that, use following instructions to start:

**To start router 1:**
  ./router/router.py -o 127.0.0.1 -p 33333 -d 33343 -n diver/area/1
**For router 2:**
  ./router/router.py -o 127.0.0.1 -p 33333 -d 33353 -n diver/area/2

---

**To start device 1:**
  ./sensor/device_1.py -o 127.0.0.1 -i 127.0.0.1 -p 33343
**For device 2:**
  ./sensor/device_2.py -o 127.0.0.1 -i 127.0.0.1 -p 33353

---

**To start consumer:**
  python3 ./consumer/consumer.py

