from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

print("//Duothan 4.0 - Lamp Control System")
print("Initializing...")
app = Flask(__name__, static_url_path='/templates/static')

GPIO.setmode(GPIO.BCM)

switch_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# Set up GPIO pins as outputs
for pin in switch_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Reset the state of all switches

print("System Initialized !")

# Define a route and a view function
@app.route('/')
def main():
    return render_template('lamptest.html')

@app.route('/turnOffbutt/<int:value>/<int:status>', methods=['POST'])
def turnOffbutt(value, status):
    if True: # It'll Not fail XD (Hopefully)
        GPIO.output(value, GPIO.LOW)  # Turn off the specified switch
        print("Ready :", value, status)
        time.sleep(2)
        GPIO.output(value, GPIO.HIGH)  # Reset the specified switch
        print("Ready Clock Reset")
        return '', 204
    # except:
    #     return '', 400

# Run the Flask app on the local network
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
