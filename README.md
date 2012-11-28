## Pydo

Converts your README.d and documentation files made in Markdown to styled
HTML files. Better templating support and styling is planned but for now the
style is defined statically in '\_\_init\_\_.py' inside the folder 'pydo_resources'

## Dependencies

 - Markdown >= 2.2.1
 - Pygments >= 1.5
 - Pystache >= 0.5.3

## Installation

Clone the repository, open an terminal and navigate to the folder
containing the Pydo files.

```python
python setup.py install
```

And now you can use Pydo to generate static HTML version of all your 
Markdown documents.