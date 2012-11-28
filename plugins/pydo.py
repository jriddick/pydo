import re
import markdown
import urllib

REGEX = re.compile( \
	r'(?P<block>\<h2\>(?P<content>.*)\<\/h2\>)',
	re.DOTALL)

class PydoPostprocessor(markdown.postprocessors.Postprocessor):
	"""
		Find Header 2 elements in the HTML code and turn them into
		links so they can be used in an Table of Content.
	"""

	def __init__(self, md):
		markdown.postprocessors.Postprocessor.__init__(self, md)

	def run(self, lines):
		line = lines.split("\n")
		for index, text in enumerate(line):
			m = REGEX.search(text)
			if m:
				link	= urllib.parse.quote_plus(m.group("content").lower())
				content = m.group("block")
				line[index] = '<a id="%s" href="#%s">%s</a>' % (link, link, content)
		return "\n".join(line)

class PydoExtension(markdown.Extension):
	""" Add Pydo to Markdown as an Extension """
	def extendMarkdown(self, md, md_globals):
		"""Add Pydo extension to Markdown"""
		md.postprocessors.add('pydo', PydoPostprocessor(md), "_begin")
		md.registerExtension(self)

def makeExtension(configs={}):
	return PydoExtension(configs=configs)
