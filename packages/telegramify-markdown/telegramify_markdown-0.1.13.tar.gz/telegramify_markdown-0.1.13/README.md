# telegramify-markdown

[![PyPI version](https://badge.fury.io/py/telegramify-markdown.svg)](https://badge.fury.io/py/telegramify-markdown)  
[![Downloads](https://pepy.tech/badge/telegramify-markdown)](https://pepy.tech/project/telegramify-markdown)

> 🪄 Python Telegram Markdown Converter | No more formatting headaches.

**Convert Raw Markdown to Telegram's MarkdownV2 Style**

Introducing a robust Python library that enhances Markdown formatting support in Telegram. This library automatically
processes various Markdown inputs, preserving the original formatting without requiring manual escaping. It simplifies
your Markdown interactions on Telegram with seamless auto-processing.

Before this library, sending and rendering unknown Markdown content (like GitHub's README files) required complex
parsing and reconstruction. Now, you can easily handle this and customize it for better results!

Utilizing a custom renderer, the library has been tested in a real server environment to ensure its efficacy.

> For those interested, there is also a Node.js version of the library with the same
> name: [npm:telegramify-markdown](https://www.npmjs.com/package/telegramify-markdown)

## Installation

To install the library, run:

```bash
pip install telegramify-markdown
```

or, if you use `pdm`:

```shell
pdm add telegramify-markdown
```

## Supported Input

- [x] Headings (Levels 1-6)
- [x] `Links [text](url)`
- [x] `Images ![alt](url)`
- [x] Lists (Ordered and Unordered)
- [x] Tables `|-|-|`
- [x] Horizontal Rules `----`
- [x] Text Styles `*Italic*` and `**Bold**`
- [x] Underline `__Underline__` (if `customize.strict_markdown` is False)
- [x] Code Blocks
- [x] Inline Code
- [x] Block Quotes `>`
- [x] Strikethrough `~~Strikethrough~~`
- [x] Spoilers `||Spoiler||`
- [x] Task Lists
- [x] Expanded Citation
- [ ] Strikethrough `~Strikethrough~`
- [ ] Telegram Emojis
- [ ] Telegram User Mentions

> [!NOTE]
> Despite `~Strikethrough~` being mentioned in Telegram's official documentation, it can't be parsed as strikethrough.

## Use case

````python3
import telegramify_markdown
from telegramify_markdown import customize

customize.markdown_symbol.head_level_1 = "📌"  # If you want, Customizing the head level 1 symbol
customize.markdown_symbol.link = "🔗"  # If you want, Customizing the link symbol
customize.strict_markdown = True  # If you want to use __underline__ as underline, set it to False, or it will be converted to bold.
customize.cite_expandable = True  # If you want to enable expandable citation, set it to True.
markdown_text = """
# Title
## Subtitle
### Subsubtitle
#### Subsubsubtitle
'\_', '\*', '\[', '\]', '\(', '\)', '\~', '\`', '\>', '\#', '\+', '\-', '\=', '\|', '\{', '\}', '\.', '\!'
_ , * , [ , ] , ( , ) , ~ , ` , > , # , + , - , = , | , { , } , . , !
We will remove the \ symbol from the original text.
**bold text**
*bold text*
_italic text_
__underline__
~no valid strikethrough~
~~strikethrough~~
||spoiler||
*bold _italic bold ~~italic bold strikethrough ||italic bold strikethrough spoiler||~~ __underline italic bold___ bold*
__underline italic bold__
[link](https://www.google.com)
- [ ] Uncompleted task list item
- [x] Completed task list item
> Quote

> Multiline Quote In Markdown it's not possible to send multiline quote in telegram without using code block or html tag but telegramify_markdown can do it.

> If you quote is too long, it will be automatically set in expandable citation. 
> This is the second line of the quote.
> This is the third line of the quote.
> This is the fourth line of the quote.
> This is the fifth line of the quote.

```python
print("Hello, World!")
```
This is `inline code`
1. First ordered list item
2. Another item
    - Unordered sub-list.
    - Another item.
1. Actual numbers don't matter, just that it's a number
"""
converted = telegramify_markdown.markdownify(
    markdown_text,
    max_line_length=None,  # If you want to change the max line length for links, images, set it to the desired value.
    normalize_whitespace=False
)
print(converted)
# export Markdown to Telegram MarkdownV2 style.
````

output as follows:

| Exp 1                           | Exp 2                           |
|---------------------------------|---------------------------------|
| ![result](.github/result-5.png) | ![result](.github/result-6.png) |

