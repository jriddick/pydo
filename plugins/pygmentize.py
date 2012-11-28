import re
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter


PYGMENTIZE_REGEX = re.compile( \
	r'(?P<fence>^(?:~{3,}|`{3,}))[ ]*(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*)\}?)?[ ]*\n(?P<code>.*?)(?<=\n)(?P=fence)[ ]*$', 
	re.MULTILINE|re.DOTALL)

class Pygmentize:
	"""
	Highlights code using Pygments
	"""

	def __init__(self, code=None, lines=False, guess=True, lang=None, tab_length=4):
		self.code = code
		self.lang = lang
		self.guess = guess
		self.lines = lines
		self.tab_length = tab_length

	def run(self):
		self.code = self.code.strip('\n')

		if self.lang is None:
			if self.guess:
				try:
					lexer = guess_lexer(self.code)
				except ValueError:
					lexer = TextLexer()
			else:
				lexer = TextLexer()
		else:
			try:
				lexer = get_lexer_by_name(self.lang)
			except ValueError:
				if self.guess:
					try:
						lexer = guess_lexer(self.code)
					except ValueError:
						lexer = TextLexer()
				else:
					lexer = TextLexer()

		return highlight(self.code, lexer, HtmlFormatter(linenos=self.lines))

class PygmentizePreprocessor(markdown.preprocessors.Preprocessor):
	"""
	Find GitHub styled codeblocks and turn them into HTML5 codeblocks,
	and if possible style them with Pygments.
	"""

	def __init__(self, md):
		markdown.preprocessors.Preprocessor.__init__(self, md)

	def run(self, lines):
		# join the lines together with "\n" as separator
		text = "\n".join(lines)

		while 1:
			m = PYGMENTIZE_REGEX.search(text)
			if m:
				highlighter = Pygmentize(m.group('code'),
					lines   = self.config['lines'],
					guess   = self.config['guess'],
					lang    = (m.group('lang') or None))
				code 		= highlighter.run()
				placeholder = self.markdown.htmlStash.store(code, safe=True)
				text 		= '%s\n%s\n%s' % (text[:m.start()], placeholder, text[m.end():])

			else:
				break

		return text.split("\n")

class PygmentizeTreeprocessor(markdown.treeprocessors.Treeprocessor):
	def run(self, root):
		blocks = root.getiterator('pre')
		for block in blocks:
			children = block.getchildren()
			if len(children) == 1 and children[0].tag == 'code':
				code = Pygmentize(children[0].text,
					lines = self.config['lines'],
					guess = self.config['guess'])
				placeholder = self.markdown.htmlStash.store(code.run(), safe=True)

				block.clear()
				block.tag = 'p'
				block.text = placeholder

class PygmentizeExtension(markdown.Extension):
	def __init__(self, configs):
		self.config = {
			'lines' : [False, "Enable line numbers"],
			'guess' : [True, "Automatic language detection"]
		}

		for key, value in configs:
			if value == 'True': value = True
			if value == 'False': value = False
			self.setConfig(key, value)

	def extendMarkdown(self, md, md_globals):
		"""Add Pygmentize extension to Markdown"""
		preprocessor = PygmentizePreprocessor(md)
		treprocessor = PygmentizeTreeprocessor(md)

		preprocessor.config = self.getConfigs()
		treprocessor.config = self.getConfigs()

		md.preprocessors.add('pygmentize', preprocessor, "_begin")
		md.treeprocessors.add('pygmentize', treprocessor, "<inline")

		md.registerExtension(self)

def makeExtension(configs={}):
	return PygmentizeExtension(configs=configs)
