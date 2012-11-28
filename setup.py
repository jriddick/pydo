from setuptools import setup, find_packages

setup(
		name 		 = "Pydo",
		version 	 = "0.1.2",
		description  = """Pydo or Python Document takes an Markdown document file
		and turns it into a nice and easy to read HTML file.
		""",
		author		 = "Alexander Persson",
		author_email = "apersson.93@gmail.com",
		url 		 = "http://jriddick.me/pydo.html",
		packages 	 = find_packages(),
		entry_points = {
			'console_scripts': [
			'pydo = pydo.pydo:main',
			]
		},
		install_requires = ['markdown', 'pygments', 'pystache']
)