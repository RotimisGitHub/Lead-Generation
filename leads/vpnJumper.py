from dotenv import load_dotenv
import os


import time
import random
import subprocess

load_dotenv()
class VPNJumper:
    def __init__(self, country=None, randomCountry=False, looping=False):
        self.country = country
        self.random = randomCountry
        self.sudoPasscode = os.environ.get('SUDO_PASSCODE')
        self.rootCode = f'echo "{self.sudoPasscode}" | sudo -S'
        self.looping = looping
        self.listOfCountries = {'United States': 'US',
                                'Canada': 'CA',
                                'United Kingdom': 'GB',
                                'Germany': 'DE',
                                'France': 'FR',
                                'Italy': 'IT',
                                'Spain': 'ES',
                                'Australia': 'AU',
                                'Japan': 'JP',
                                'China': 'CN'}
        self.chosenCode = self._chooseCountryCode()

    def establishConnection(self):
        if not self.looping:
            print(f"Trying to connect to {self.country}'s servers!")
            print(self.chosenCode)
            commandlineCode = f"protonvpn connect --cc {self.chosenCode}"
            os.system(f'{self.rootCode} {commandlineCode}')
            checkStatus = subprocess.run(f'{self.rootCode} protonvpn s', shell=True, capture_output=True, text=True)
            connectionStatus = self._statusChecker(checkStatus)
            if connectionStatus:
                print(f"Connection was successful to {self.chosenCode}")
                return True
            else:
                print("Connection has not been established")
                return False

    def establishLoopingConnection(self, seconds: int):
        if self.looping and self.random:
            while True:
                self.establishConnection()
                time.sleep(seconds)

    def reconnect(self):

        reconnect = subprocess.run(f'{self.rootCode} protonvpn r', shell=True, capture_output=True, text=True)
        connectionStatus = self._statusChecker(reconnect)
        if connectionStatus is True:
            print("Reconnection was successful")
            return True
        else:
            print("Reconnection has not been established")
            return False

    def disconnect(self):
        disconnect = subprocess.run(f'{self.rootCode} protonvpn d', shell=True, capture_output=True, text=True)
        connectionStatus = self._statusChecker(disconnect, disconnect=True)
        if connectionStatus is True:
            print("Disconnection was successful")
            return True
        else:
            print("Disconnection was unsuccessful")
            return False

    def _chooseCountryCode(self):
        if self.random:
            randomCountry = random.choice([i for i in self.listOfCountries.keys()])
            self.chosenCode = self.listOfCountries[randomCountry]
        else:
            if self.country in self.listOfCountries.keys():
                self.chosenCode = self.listOfCountries[self.country]
            else:
                print("That Country is not able to be connected with. Please Try again")
                return None
        return self.chosenCode

    def _statusChecker(self, process: subprocess, disconnect=False):
        if not disconnect:
            outputSeparated = process.stdout.strip().split("\n")
            outputPartition = []

            for output in outputSeparated:
                outputPartition.append(output.split(":"))

            outputKeys = {k: v.strip() for sublist in outputPartition for k, v in [sublist[:2]]}

            if outputKeys["Status"] == "Connected":
                return True
            else:
                return False
        else:

            output = process.stdout
            if output.strip() == 'Disconnected.':
                return True
            else:
                return False
