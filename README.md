# Home-Security-System-Raspberry Pi and IOT
This is a Python code for Internet of Things based Home Security System using Raspberry pi .
The idea of home security to prevent robberies and thefts.
We created a security system that can be controlled by the user and operates according to user’s instructions.
The system will detect the presence of intruder and alert the user by sending him a message through telegram. 
It uses an android platform called “Telegram” to interact or control the system, which represents the real-worlds problem like theft-detection etc.

# Working:
1. Intially, user needs to enroll his/her fingerprint and password (0-9).
2. If any one gives the correct input via keypad or the fingerprint is matched, then system unlocks the door with the help of servo motor attached to the door.
3. If fingerprint does not match with the enrolled one and password is entered incorrectly for three time, then an alert along with the photo of an intruder will be sent to the owner via telegram bot.
4. Door can be unlocked or locked remotely using the commands in telegram (Remote monitoring).
