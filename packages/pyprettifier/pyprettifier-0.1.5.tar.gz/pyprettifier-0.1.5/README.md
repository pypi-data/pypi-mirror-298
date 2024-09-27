
# PyPrettifier

**PyPrettifier** is a simple Python package for converting between emoji names (like `:smile:`) and actual emoji characters (like 😄), and vice versa. It also includes several utility functions to manipulate strings that contain emojis, such as counting, replacing, and removing emojis.

More beautiful feature will uploaded in the future to handle the output and different output format.

In addition an automatic update, emoji retrieval and several other options will be coded.

## Features

- **Convert emoji names to emojis**: Convert emoji names such as `:smile:` to their corresponding emoji characters 😄.
- **Convert emojis to emoji names**: Replace emoji characters with their `:emoji_name:` tags.
- **Count emojis**: Count the number of emojis in a string.
- **Remove emojis**: Remove all emoji characters from a string.
- **Replace emojis with custom alternatives**: Replace each emoji in a string with a custom alternative (e.g., descriptive text or themed emojis).
- **Support for a wide range of emojis**: The package includes a dictionary with a large set of emojis, which can be expanded easily.

## Installation

Install the package using `pip`:

```bash
pip install pyprettifier
```

## Usage

### Import the package

```python
from pyprettifier import EmojiConverter
```

### Convert Emoji Names to Emojis

```python
text = "Hello :smile:, how are you? :fire:"
converted_text = EmojiConverter.replace_emojis_in_string(text)
print(converted_text)  # Output: "Hello 😄, how are you? 🔥"
```

### Convert Emojis to Emoji Names

```python
emoji_text = "Hello 😄, how are you? 🔥"
converted_back_text = EmojiConverter.replace_emojis_with_names(emoji_text)
print(converted_back_text)  # Output: "Hello :smile:, how are you? :fire:"
```

### Remove Emojis from a String

```python
emoji_text = "Hello 😄, how are you? 🔥"
text_without_emojis = EmojiConverter.remove_emojis(emoji_text)
print(text_without_emojis)  # Output: "Hello , how are you? "
```

### Replace Emojis with Custom Alternatives

```python
emoji_text = "Hello 😄, how are you? 🔥"
replacements = {
    "😄": "smiling face",
    "🔥": "fire emoji"
}
text_with_replacements = EmojiConverter.replace_emojis_with_alternatives(emoji_text, replacements)
print(text_with_replacements)  # Output: "Hello smiling face, how are you? fire emoji"
```

## License

This project is licensed under the MIT License.
