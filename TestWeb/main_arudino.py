from flask import Flask, render_template
import pyfirmata
import time
# Create a Flask instance
print("//Duothan 4.0 - Lamp Control System")
print("Initializing...")
app = Flask(__name__, static_url_path='/templates/static')
board = pyfirmata.Arduino('/dev/ttyACM0')

# Resetting the state of the all switches
print("Resetting the state of the all switches...")
for i in range(2,13):
    print("Switch ",i," is resetting...")
    board.digital[i].write(1)

print("System Initialized !")
# Define a route and a view function

@app.route('/')
def main():
    return render_template('lamptest.html')

@app.route('/turnOffbutt/<int:value>/<int:status>', methods=['POST'])
def turnOffbutt(value, status):
    if True: #It'll Not fail XD (Hopefully)
        board.digital[value].write(0)
        print("Ready :",value, status)
        time.sleep(2)
        board.digital[value].write(1)
        print("Ready Clock Reset")
        return '', 204
    # except:
    #     return '', 400


# Run the Flask app on the local network
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
