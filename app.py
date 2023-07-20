from flask import Flask, render_template
import os

# Configuration
app = Flask(__name__)

# Routes 
@app.route('/')
def root():
    return render_template("base.html")

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7791)) 
    
    app.run(port=port, debug=True)
