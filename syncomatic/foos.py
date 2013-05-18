import os
import datetime
from syncomatic import app, lm

def get_filelist():
	"""
		Returns a list of dictionaries;
		Each dictionary contains the following keys:
		'name', 'size', 'creation_date'
	"""
	filenames = os.listdir(app.config['UPLOAD_FOLDER'])
	files = []
	for name in filenames:
		# os.stat returns a 10-tuple
		stats = os.stat(''.join(([app.config['UPLOAD_FOLDER'], '/', name])))
		size = stats[6]
		creation_date = datetime.datetime.fromtimestamp(stats[-2]).strftime("%H:%M %d.%m.%Y")
		f = {'name': name, 'size': size, 'creation_date': creation_date}
		files.append(f)

	return files
