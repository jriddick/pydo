"""
Import our external dependencies
"""
import pydo_resources
import pystache
import os
import re
import optparse
import codecs
from plugins import pydo, pygmentize
from os import path
from markdown import markdown
from datetime import datetime

def ensure_directory(directory):
	"""
	Ensures that the given directory exist and if it does not
	exist it will create it.
	"""
	if not os.path.isdir(directory):
		os.mkdir(directory)

def destination(filepath, outdir=None):
	"""
	Creates an string for the complete path
	for the new file that should be created
	"""
	if not outdir:
		raise TypeError("Missing the required 'outdir' keyword argument.")
	try:
		name = filepath.replace(filepath[ filepath.rindex("."): ], "")
	except ValueError:
		name = filepath
	return path.join(outdir, "%s.html" % name)

def process(sources, outdir=None, title=None):
	if not outdir:
		raise TypeError("Missing the required 'outdir' keyword argument.")
	
	# Sort our sources
	sources = sorted(sources)

	if sources:
		ensure_directory(outdir)
		css = open(path.join(outdir, "pydo.css"), "w")
		css.write(pydo_resources.css)
		css.close()

		for source in sources:
			dest 	= destination(source, outdir=outdir)
			title	= title and title or os.path.splitext(source)[0].title()

			try:
				os.makedirs(path.split(dest)[0])
			except OSError:
				pass

			mr = codecs.open(source, mode="r", encoding="utf8")
			mw = codecs.open(dest, 	 mode="w", encoding="utf8")

			pyg = pygmentize.PygmentizeExtension({})
			pyd = pydo.PydoExtension(None)

			text = mr.read()
			html = pystache.render(pydo_resources.html, {
				"title"			: title,
				"stylesheet"	: path.relpath(path.join(outdir, "pydo.css"), path.split(dest)[0]),
				"time"			: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			})

			mw.write(
				re.sub(
					r'<<content>>', 
					markdown(text, output_format="html5", extensions=[pyg, pyd]), 
					html
				)
			)

			print("pydo has converted '%s' to '%s'" % (source, dest))

def main():
	parser = optparse.OptionParser()

	parser.add_option('-d', '--directory', action='store', type='string', dest='outdir', default='docs',
		help='The output directory that the rendered files should go to.')

	parser.add_option('-t', '--title', action='store', type='string', dest='title',
		help='The title for the rendered HTML')

	opts, sources = parser.parse_args()

	process(sources, outdir=opts.outdir, title=opts.title)



if __name__ == "__main__":
	main()