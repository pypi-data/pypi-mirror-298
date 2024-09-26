# zyjared-color

## 安装

```sh
pip install zyjared-color
```

## 使用

```py
from zyjared_color import color, Color

content = color('Hello World!').red() + ' -+-+-+- test'

text = f'{color("Hello World!").blue():<15} -+-+-+- test'
content = color(text)
```

### 拓展

```py
from zyjared_color import zprint

zprint([
    'Hello',
    'World!',
])

zprint({
    'Hello': 'World!'
    'Hello': ['World!']
    'Hello': {
        'World!': 'Hello World!'
    }
})
```

## HTML / CSS

```python
from zyjared_color.html import ColorHtml, StaticColorHtml
from zyjared_color.html import blue, red, bold, italic, underline, through

text = ColorHtml('Hello World!').red().bold()
print(text)

# custom styles
text = ColorHtml("Hello World!", {"opacity": 0.5, "font-weight": "bold"})
print(text)
```

**example:** Display `ColorHtml` in Jupyter Notebook

```python
from zyjared_color.html import ColorHtml as Color, StaticColorHtml as StaticColor
from zyjared_color.html import blue, red, bold, italic, underline, through
from IPython.display import display, HTML

text = Color('Hello World!').red().bold()

# f'{text}' or str(text)
display(HTML(f'{text}'))
```
