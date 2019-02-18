# home-security-system-raspi
This is a Python code for Internet of Things based Home Security System using Raspberry pi .
The idea of home security to prevent robberies and thefts.
We created a security system that can be controlled by the user and operates according to user’s instructions.
The system will detect the presence of intruder and alert the user by sending him a message through telegram. 
It uses an android platform called “Telegram” to interact or control the system, which represents the real-worlds problem like theft-detection etc.

Working:
As system turns ‘ON’, telegram services will be running in the background. So, door is unlocked or locked remotely.
As soon as user enters the input via keypad or places the finger on fingerprint sensor, system checked for the correct match of fingerprint or password.
Initially, correct password is entered which unlocked the door and even tried with correct fingerprint which yielded the same output.
Later, an unenrolled finger is placed on sensor which didn’t unlock the door even a password is entered incorrectly which gave the same output.
The Pi camera captured photo and a text message named “INTRUDER DETECTED” along with the photo sent to our mobile phone via telegram application. Later, door is unlocked and locked remotely using some set of commands.
