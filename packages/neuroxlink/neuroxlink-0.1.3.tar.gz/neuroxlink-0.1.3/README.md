## neuroxlink

[![PyPI version](https://badge.fury.io/py/neuroxlink.svg)](https://badge.fury.io/py/neuroxlink)

An experimental [mdast](https://github.com/syntax-tree/mdast) parser to have fun with MyST articles.


```python
nxlink = NeuroxLink('10.55458/neurolibre.00021')
their_fig_4 = nxlink.create_plotly_figure('fig4')
their_fig_4.show()
```
