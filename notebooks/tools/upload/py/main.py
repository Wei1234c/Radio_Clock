# coding: utf-8
 

# WiFi network _________________________
def wait_for_wifi():
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)        
        sta_if.connect('Lin_841', '51557010')
        while not sta_if.isconnected():
            pass
    print('Network configuration:', sta_if.ifconfig())

wait_for_wifi()


# Signal boot successfully ___________
import led
led.blink_on_board_led(times = 2)



# Display ____________________________

import display_ad9833 as display
display = display.Display()
import ntp_clock 
ntp_clock.Clock(display).run()


# as MQTT node _______________________
# import node
# node.main()
