Pydo
====

A simple static HTML generator that transforms all your Markdown documents
into nicely styled HTML documents. 

## Good-To-Know

You should know before you start to convert all your Markdown documents that Pydo 
looks for `h1` tags to use for page header. So they will be big and they will be centered.
All other header tags will work and looks as expected.

The default style can be changed just open `__init__.py` that resides in the folder
`pydo_resources` and you can change the css and the HTML. 

## Now what?

The `pydo` command does not have alot of options, infact only two exists right now.

 - `-o --output` changes the output folder for the HTML files [default to docs/]
 - `-t --title` changes the site title for the generated HTML files [defaults to the filename]

So to convert an Markdown file to HTML you just run

```python
pydo Pydo.md
> pydo has converted 'Pydo.md' to 'docs\Pydo.html'
```