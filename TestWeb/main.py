from flask import Flask, render_template
import pyfirmata
# Create a Flask instance
app = Flask(__name__)
board = pyfirmata.Arduino('/dev/ttyACM0')


# Define a route and a view function
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/turnOff', methods=['POST'])
def turnOffbutt():
    board.digital[3].write(0)
    print("Ready")
    return  '', 204

@app.route('/turnOn', methods=['POST'])
def turnOnbutt():
    board.digital[3].write(1)
    print("Ready")
    return  '', 205

# Run the Flask app on the local network
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
