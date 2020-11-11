# Andy's Notebook

Hosting Jupyter Notebooks on GitHub Pages

## Why?

I wanted to work more with Jupyter Notebooks, 
both to give myself experience and also demonstrate 
my experience on a public webpage. I especially 
wanted a website for this portfolio with custom styling, 
which would appear better for viewing than a PDF, 
especially on mobile devices. This necessarily led 
to the need for a static site building system which 
could convert jupyter notebooks into custom styled 
html webpages and also provide a front page to access 
these notebooks. Currently, as I haven't found such a 
system on PyPi that met my needs, I've built my own system
that I've called Callystio (a sort of morph of the name
Callisto, the largest moon of Jupiter). It was of course
written in Python, so it can take advantage of tools like
nbconvert that already exist for converting Jupyter Notebooks.