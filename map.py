from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def map_func():
	return render_template('map.html')
@app.route('/events/')
def events():
    #filename = os.path.join(app.static_folder, 'events.json')
    #with open(filename) as test_file:
    #    data = json.load(test_file)
    #return render_template('events.html', data=data)
    return render_template('events.html')
if __name__ == '__main__':
    app.run(debug = True)