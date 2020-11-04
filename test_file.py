import os
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'


app.run(debug=True,host='0.0.0.0')
