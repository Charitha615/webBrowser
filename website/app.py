from flask import Flask, render_template, request

app = Flask(__name__)

# Define your secret key
secret_key = "123456"

@app.route('/')
def home():
    # Check if the provided key matches the secret key
    provided_key = request.args.get('key', '')
    if provided_key == secret_key:
        return render_template('index.html')
    else:
        return "Unauthorized. Please provide a valid key."

if __name__ == '__main__':
    app.run(debug=True)
