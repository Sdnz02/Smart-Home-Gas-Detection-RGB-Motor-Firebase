import network
import urequests as requests
import time
import machine
from machine import Pin, ADC

# Wi-Fi credentials
SSID = 'Swat'
PASSWORD = 'swatdeniz'

# Firebase URL
firebase_url = 'https://finalproject-64112-default-rtdb.europe-west1.firebasedatabase.app/'

# Define pins
GAS_SENSOR_PIN = 26
IR_RECEIVER_PIN = 2
MOTOR_PINS = [3, 4, 5, 6]
RGB_PINS = {'red': 10, 'green': 11, 'blue': 12}

# Initialize pins
gas_sensor = ADC(Pin(GAS_SENSOR_PIN))
ir_receiver = Pin(IR_RECEIVER_PIN, Pin.IN)
motor_pins = [Pin(pin, Pin.OUT) for pin in MOTOR_PINS]
rgb_pins = {color: Pin(pin, Pin.OUT) for color, pin in RGB_PINS.items()}

# IR remote codes (example values, replace with your actual codes)
IR_REMOTE_RED = 0xBA45FF00
IR_REMOTE_GREEN = 0xB946FF00
IR_REMOTE_BLUE = 0xB847FF00

# Firebase functions
def firebase_put(path, data):
    url = firebase_url + path + '.json'
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, json=data, headers=headers)
    return response.json()

def firebase_get(path):
    url = firebase_url + path + '.json'
    response = requests.get(url)
    return response.json()

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Connecting to WiFi...")
        time.sleep(1)
    
    print("Connected to WiFi")
    print("IP Address:", wlan.ifconfig()[0])

# Control RGB LED
def set_rgb(red, green, blue):
    rgb_pins['red'].value(red)
    rgb_pins['green'].value(green)
    rgb_pins['blue'].value(blue)

# Stepper motor functions
def step_motor(steps):
    for i in range(steps):
        for j in range(4):
            for pin in range(4):
                motor_pins[pin].value((0b1100 >> (j + pin) % 4) & 1)
            time.sleep(0.001)

# Decode IR signal
def decode_ir():
    if ir_receiver.value() == 0:  # IR receiver active low
        code = 0
        for _ in range(32):  # Assuming 32-bit codes
            while ir_receiver.value() == 0:
                pass  # Wait for the signal to go high
            time.sleep_us(562)  # Wait for the middle of the bit
            if ir_receiver.value() == 1:
                code = (code << 1) | 1
            else:
                code = (code << 1)
            while ir_receiver.value() == 1:
                pass  # Wait for the signal to go low
        return code
    return None

# Main loop
def main():
    connect_wifi()
    
    while True:
        # Read gas sensor
        gas_value = gas_sensor.read_u16() >> 4  # Scale to 0-1023
        print("Gas Value:", gas_value)
        
        # Get commands from Firebase
        commands = firebase_get('commands')
        motor_command = commands.get('motor', False)
        rgb_command = commands.get('rgb', {'red': 0, 'green': 0, 'blue': 0})
        
        # Check IR receiver for RGB control
        ir_code = decode_ir()
        if ir_code:
            print("IR Code:", hex(ir_code))
            if ir_code == IR_REMOTE_RED:
                set_rgb(1, 0, 0)
            elif ir_code == IR_REMOTE_GREEN:
                set_rgb(0, 1, 0)
            elif ir_code == IR_REMOTE_BLUE:
                set_rgb(0, 0, 1)
        
        # Control motor based on command
        if motor_command:
            step_motor(10)
        
        # Control RGB LED based on command
        set_rgb(rgb_command['red'], rgb_command['green'], rgb_command['blue'])
        
        # Update sensor data to Firebase
        firebase_data = {
            'gas_value': gas_value
        }
        firebase_put('sensor_data', firebase_data)
        
        time.sleep(1)

main()

