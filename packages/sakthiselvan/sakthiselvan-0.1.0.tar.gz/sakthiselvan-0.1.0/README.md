
# `sakthi_library`

`sakthi_library` is a Python module that provides a collection of utility functions for string manipulation, character encoding, conversions, sorting, and list operations. It contains various custom functions designed to simplify common tasks.

## Features

### 1. String Manipulation Functions
- **`sakthi_show_it(*args, sep=' ', end='\n', file=None, flush=False)`**: Custom print function with adjustable separators, file output, and flushing.
- **`sakthi_clean_front_and_back(string)`**: Removes leading and trailing whitespace from a string.
- **`sakthi_clean_left(string)`**: Removes leading whitespace from a string.
- **`sakthi_clean_right(string)`**: Removes trailing whitespace from a string.
- **`sakthi_remove_prefix(string, prefix)`**: Removes the specified prefix from a string.
- **`sakthi_remove_suffix(string, suffix)`**: Removes the specified suffix from a string.
- **`sakthi_it_starts_with(string, prefix)`**: Checks if the string starts with a given prefix.
- **`it_ends_with(string, suffix)`**: Checks if the string ends with a given suffix.
- **`make_title(string)`**: Converts the string to title case by capitalizing the first letter of each word.

### 2. Character Encoding Functions
- **`sakthi_unicode_character(code_point)`**: Retrieves the Unicode character for a given code point.
- **`sakthi_character_to_ascii_code(character)`**: Converts a character to its ASCII or UTF-8 encoded value.

### 3. Case Conversion Functions
- **`sakthi_change_capital_A_B_C_D(string)`**: Converts lowercase letters to uppercase.
- **`sakthi_change_to_lowercase(string)`**: Converts uppercase letters to lowercase.

### 4. Number and Character Conversion Functions
- **`sakthi_to_ascii_values(string)`**: Converts characters in a string to their ASCII values.
- **`sakthi_to_hexadecimal_values(string)`**: Converts characters in a string to their hexadecimal values.
- **`sakthi_to_binary_values(string)`**: Converts characters in a string to binary values.
- **`sakthi_to_decimal_values(string)`**: Converts characters in a string to decimal values.
- **`sakthi_to_octal_values(string)`**: Converts characters in a string to octal values.
- **`sakthi_decimal_to_binary(decimal)`**: Converts a decimal number to binary.
- **`sakthi_decimal_to_octal(decimal)`**: Converts a decimal number to octal.
- **`sakthi_decimal_to_hexadecimal(decimal)`**: Converts a decimal number to hexadecimal.
- **`sakthi_binary_to_decimal(binary)`**: Converts a binary number to decimal.

### 5. Sorting Functions
- **`sakthi_arrange_ascending_order(arr)`**: Sorts an array in ascending order using Timsort.
- **`sakthi_arrange_descending_order(arr)`**: Sorts an array in descending order using Timsort.

### 6. List and Range Functions
- **`i_need_number_list(start, stop, step)`**: Generates a list of numbers within a specified range and step.
- **`how_many_elements_present(iterable)`**: Returns the number of elements in an iterable.
- **`sakthi_total_of_list(iterable, start=0)`**: Calculates the sum of elements in a list with an optional starting value.
- **`sakthi_min(list)`**: Custom function to find the minimum value in a list.
- **`sakthi_max(list)`**: Custom function to find the maximum value in a list.

### 7. Print Formatting Utilities
- **`sakthi_add_newline(string)`**: Adds a newline after "sakthi" in a string.
- **`sakthi_add_tab_space(string)`**: Adds a tab space after "sakthi".
- **`sakthi_backspace(string)`**: Adds a backspace after "sakthi".
- **`sakthi_add_vertical_tab(string)`**: Adds a vertical tab after "sakthi".
- **`sakthi_add_form_newline(string)`**: Adds a form feed after "sakthi".
- **`sakthi_sart_from_first(string)`**: Starts from the first character of a string.

## Installation

To install `mymodule`, clone the repository and use it in your Python projects.

```bash
git clone https://github.com/yourusername/mymodule.git
```

## Usage

Here's an example of how you can use some functions from `mymodule`:

```python
from mymodule import sakthi_show_it, sakthi_to_ascii_values

# Print using custom function
sakthi_show_it("Hello", "World", sep=", ")

# Convert string to ASCII values
ascii_values = sakthi_to_ascii_values("Hello")
print(ascii_values)
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you find any bugs or want to add new features.