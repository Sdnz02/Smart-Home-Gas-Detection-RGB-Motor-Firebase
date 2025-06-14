# Smart Home IoT System with Raspberry Pi Pico W, Firebase and IR Control

This project demonstrates a smart home automation and monitoring system using a **Raspberry Pi Pico W**, a **MQ-5 gas sensor**, **IR remote**, **RGB LEDs**, and a **stepper motor**. The system is integrated with **Google Firebase** to enable **remote control** and **real-time sensor data monitoring** over the internet. It also supports **local control** via an infrared (IR) remote.

## Project Purpose

- Monitor gas levels in real time to enhance **home safety**.
- Remotely control RGB LEDs and a stepper motor using **Google Firebase**.
- Provide local control via **IR remote** for changing RGB LED colors.
- Perform **visual alerts** using RGB LEDs and trigger mechanical actions using the stepper motor in case of gas leakage.

---

## Hardware Components

| Component                     | Description                                |
|------------------------------|--------------------------------------------|
| Raspberry Pi Pico W          | Microcontroller with WiFi capability       |
| MQ-5 Gas Sensor              | Detects gas concentration (LPG, methane)   |
| IR Receiver + Remote         | Used for local control of RGB LEDs         |
| RGB LED or 3 Single LEDs     | Visual indication (color-coded alerts)     |
| 28BYJ-48 Stepper Motor       | Controlled by ULN2003 driver               |
| Infrared Communication Module| Receives IR signals                        |

---

## Software & Cloud

- **Programming Language**: MicroPython
- **IDE**: Thonny
- **Cloud Platform**: [Google Firebase Realtime Database](https://firebase.google.com/)
- **Wi-Fi SSID/Password**: Defined in the code
- **Libraries Used**:
  - `network` and `urequests` for Wi-Fi and HTTP
  - `machine` for hardware I/O
  - `time` for delays

---

## Functional Overview

### 1. Gas Sensor Monitoring
- Continuously reads gas concentration.
- Sends `gas_value` to Firebase every second.
- If above a threshold, triggers motor and sets RGB to red.

### 2. Firebase Remote Control
- Reads `commands` from Firebase:
  - `motor` flag: whether to rotate stepper
  - `rgb`: RGB values to display
- Sends sensor data (`gas_value`) back to Firebase.

### 3. IR Local Control
- Receives IR signals using IR receiver.
- Based on IR code, changes RGB LED color to red, green, or blue.
- Works without internet.

---

## Stepper Motor Function

The `step_motor()` function activates the motor in 4-phase full-step sequence, used for:
- Opening/closing windows
- Triggering mechanical alerts (e.g., buzzer, fan)

---

## RGB LED Function

- Visual indicator for gas level or user control
- Firebase and IR remote both can control it
- Red = Danger, Green = Normal, Blue = Manual mode

---

## Circuit Diagram

The wiring diagram is provided in `Homework-4_Fritzing.fzz` and shows:
- Connections for MQ-5 sensor to ADC pin
- Stepper motor pins connected via ULN2003 driver
- IR receiver connected to a GPIO pin
- RGB LEDs connected to PWM GPIO pins
- Powered and controlled by Raspberry Pi Pico W

---

## Demo Video (https://youtu.be/ET55Dop-mqg?feature=shared)

All functionalities are demonstrated in the project video:
- Line-by-line code explanation
- Successful Wi-Fi & Firebase connection
- Live data monitoring and control via Firebase
- IR remote interaction
- Real-time hardware response

---

## Conclusion

This project is a complete embedded system that demonstrates how **IoT**, **Cloud platforms**, and **hardware control** can work together to enhance home automation. It ensures:
- Safety (gas leak alerts),
- Control (remote and local),
- Real-time feedback (sensor monitoring).

> Developed by: **Suat Deniz**  
> Course: **EEE 320 – Introduction to IoT**

``


