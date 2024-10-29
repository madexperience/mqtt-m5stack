import os, sys, io
import M5
from M5 import *
from hardware import *
from umqtt import *
import network
import time



Temp = None
Gas_Count = None
Motion = None
IsHaptic = None
Temp_Count = None
Motion_Count = None
Gas = None
Hours = None
Mins = None
Secs = None
line = None
line2 = None
F_label = None
F_circle = None
F_title = None
F_init = None
Battery = None
mqtt_client = None
timer0 = None
rtc = None
wlan = None
timer1 = None


gas_ct = None
temp_ct = None
motion_ct = None
Brightness = None
isClicked_Haptic = None
list2 = None
first_init = None

# Describe this function...
def loading_hide():
  global gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init, Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1
  F_label.setVisible(False)
  F_title.setVisible(False)
  F_init.setVisible(False)
  F_circle.setVisible(False)

# Describe this function...
def loading_show():
  global gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init, Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1
  F_label.setVisible(True)
  F_title.setVisible(True)
  F_init.setVisible(True)
  F_circle.setVisible(True)

# Describe this function...
def first_hide():
  global gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init, Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1
  Temp.setVisible(False)
  Gas.setVisible(False)
  Motion.setVisible(False)
  Hours.setVisible(False)
  Mins.setVisible(False)
  Secs.setVisible(False)
  line.setVisible(False)
  line2.setVisible(False)
  Gas_Count.setVisible(False)
  Temp_Count.setVisible(False)
  Motion_Count.setVisible(False)
  IsHaptic.setVisible(False)
  Battery.setVisible(False)

# Describe this function...
def first_show():
  global gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init, Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1
  Temp.setVisible(True)
  Gas.setVisible(True)
  Motion.setVisible(True)
  Hours.setVisible(True)
  Mins.setVisible(True)
  Secs.setVisible(True)
  line.setVisible(True)
  line2.setVisible(True)
  Gas_Count.setVisible(True)
  Temp_Count.setVisible(True)
  Motion_Count.setVisible(True)
  IsHaptic.setVisible(True)
  Battery.setVisible(True)


def btnA_wasClicked_event(state):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  if Brightness > 10:
    Brightness = Brightness - 10


def mqtt_m5stack_gas_event(data):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  gas_ct = str((((data[1]).decode()).strip()))
  Gas_Count.setText(str(gas_ct))
  if gas_ct == 'Danger':
    if isClicked_Haptic == True:
      Power.setVibration(200)
    Gas_Count.setColor(0xff0000, 0xffffff)
    Gas.setColor(0xff0000, 0xffffff)
    time.sleep(1)
    Power.setVibration(0)
    Gas_Count.setColor(0x000000, 0xffffff)
    Gas.setColor(0x000000, 0xffffff)


def btnB_wasClicked_event(state):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  if Brightness < 245:
    Brightness = Brightness + 10


def btnC_wasClicked_event(state):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  if isClicked_Haptic == True:
    isClicked_Haptic = False
    IsHaptic.setText(str('Haptic Off'))
  else:
    isClicked_Haptic = True
    IsHaptic.setText(str('Haptic On'))


def timer0_cb(t):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  if first_init == True:
    list2 = rtc.datetime()
    Hours.setText(str(list2[4]))
    Mins.setText(str(list2[5]))
    Secs.setText(str(list2[6]))


def mqtt_m5stack_temperature_event(data):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  temp_ct = str((((data[1]).decode()).strip()))
  Temp_Count.setText(str(temp_ct))
  if (float(temp_ct)) >= 30:
    if isClicked_Haptic == True:
      Power.setVibration(200)
    Temp_Count.setColor(0xff0000, 0xffffff)
    Temp.setColor(0xff0000, 0xffffff)
    time.sleep(1)
    Power.setVibration(0)
    Temp_Count.setColor(0x000000, 0xffffff)
    Temp.setColor(0x000000, 0xffffff)


def mqtt_m5stack_motion_event(data):
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  motion_ct = str((((data[1]).decode()).strip()))
  if motion_ct == 'O':
    if isClicked_Haptic == True:
      Power.setVibration(200)
    Motion_Count.setText(str('Activated'))
    Motion_Count.setColor(0xff0000, 0xffffff)
    Motion.setColor(0xff0000, 0xffffff)
    time.sleep(1)
    Power.setVibration(0)
    Motion_Count.setText(str('No Motion'))
    Motion_Count.setColor(0x000000, 0xffffff)
    Motion.setColor(0x000000, 0xffffff)


def setup():
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init

  M5.begin()
  Widgets.fillScreen(0xffffff)
  Temp = Widgets.Label("Temp", 32, 93, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Gas_Count = Widgets.Label("Safe", 248, 162, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Motion = Widgets.Label("Motion", 130, 93, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  IsHaptic = Widgets.Label("Haptic On", 217, 225, 1.0, 0xff0000, 0xffffff, Widgets.FONTS.DejaVu12)
  Temp_Count = Widgets.Label("99.99", 29, 162, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Motion_Count = Widgets.Label("No Motion", 116, 162, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Gas = Widgets.Label("Gas", 249, 93, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Hours = Widgets.Label("10", 88, 26, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Mins = Widgets.Label("00", 158, 26, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  Secs = Widgets.Label("00", 225, 26, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  line = Widgets.Label(":", 132, 23, 1.0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  line2 = Widgets.Label(":", 199, 23, 1.0, 0x070000, 0xffffff, Widgets.FONTS.DejaVu18)
  F_label = Widgets.Rectangle(-8, -6, 346, 248, 0xffffff, 0x000000)
  F_circle = Widgets.Circle(47, 59, 15, 0xf6ff00, 0xf6ff00)
  F_title = Widgets.Label("Safe Alert v0.1", 69, 74, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu24)
  F_init = Widgets.Label("initializing modules..", 67, 164, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  Battery = Widgets.Label("n/a", 298, 4, 1.0, 0x000000, 0x00ff54, Widgets.FONTS.DejaVu9)

  BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
  BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)
  BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnC_wasClicked_event)

  first_hide()
  loading_show()
  Brightness = 100
  F_init.setText(str('Initializing WLAN'))
  wlan = network.WLAN(network.STA_IF)
  time.sleep(1)
  F_init.setText(str('Initializing RTC'))
  time.sleep(1)
  Power.setVibration(0)
  F_init.setText(str('WLAN STA Connecting..'))
  while not (wlan.isconnected()):
    wlan.active(False)
    wlan.active(True)
    wlan.config(reconnects=5)
    wlan.config(dhcp_hostname='m5stack')
    wlan.connect('hot', '1234567890q')
    time.sleep(3)
  F_init.setText(str((str('Connected IP : ') + str((wlan.ifconfig()[0])))))
  time.sleep(1)
  F_init.setText(str('MQTT Server Connecting..'))
  mqtt_client = MQTTClient('M5core2Client', 'test.mosquitto.org', port=1883, user='', password='', keepalive=300)
  mqtt_client.connect(clean_session=True)
  mqtt_client.subscribe('m5stack/gas', mqtt_m5stack_gas_event, qos=0)
  mqtt_client.subscribe('m5stack/temperature', mqtt_m5stack_temperature_event, qos=0)
  mqtt_client.subscribe('m5stack/motion', mqtt_m5stack_motion_event, qos=0)
  time.sleep(1)
  F_init.setText(str('Welcome!'))
  time.sleep(2)
  loading_hide()
  first_show()
  rtc = RTC()
  first_init = True
  timer0 = Timer(0)
  timer1 = Timer(1)
  isClicked_Haptic = True
  timer0.init(mode=Timer.PERIODIC, period=1000, callback=timer0_cb)


def loop():
  global Temp, Gas_Count, Motion, IsHaptic, Temp_Count, Motion_Count, Gas, Hours, Mins, Secs, line, line2, F_label, F_circle, F_title, F_init, Battery, mqtt_client, timer0, rtc, wlan, timer1, gas_ct, temp_ct, motion_ct, Brightness, isClicked_Haptic, list2, first_init
  M5.update()
  mqtt_client.check_msg()
  Battery.setText(str(str((Power.getBatteryLevel()))))
  Widgets.setBrightness(Brightness)


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
