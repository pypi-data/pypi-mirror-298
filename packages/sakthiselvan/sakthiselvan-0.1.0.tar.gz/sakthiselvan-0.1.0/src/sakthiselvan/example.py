"""Hi I am Skathi

mymodule - A module containing custom functions for various tasks.

This module provides functions to:
- Customize print behavior with different newline characters.
- Convert binary strings to decimal values.
- Perform other utility functions.

Example usage:
    from mymodule import sakthi_add_tab_space
    sakthi_add_tab_space("Hello", "World")
"""
#24/08/2024
#creating my own print function
#creating the inbuild function as user defined function

#importing the sys library for displaying the output
import sys

def sakthi_show_it(*input_texts, sep=' ', file = sys.stdout, end='\n', flush = False):
    """Custom print function creation"""
    #converting whatever the user entered into string format
    output = sep.join(str(input_text) for input_text in input_texts)

    #accessing the console (or) terminal using sys.stdout file like object
    #sys.stdout is acting as variable and whatever in variable is displayed on console (or) terminal
    file.write(output + end)

    #fluch is a function that stop the buffering mechanism of the program
    #conditional test to check the flush is needed or not
    if flush:
        file.flush()
#---------------------------------------------------------------------------------------------------


def sakthi_out_in_file(file_name):
    with open(file_name, 'w') as f:
        sys.stdout = f
        print("This will be written to the file instead of the console")

#---------------------------------------------------------------------------------------------------

# 30/08/2024
# sorting the array using timsort algorithm
def sakthi_arrange_ascending_order(arr, left, right):
    """Sort the array in ascending order using Timsort (Insertion Sort for small segments)."""
    # Traverse through elements starting from the second element
    for i in range(left + 1, right + 1):
        # Store the current element (key) to be compared
        key = arr[i]
        # Initialize the index of the previous element
        j = i - 1
        # Move elements of arr[0...i-1] that are greater than key, to one position ahead
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

#---------------------------------------------------------------------------------------------------

def sakthi_arrange_descending_order(arr, left, right):
    """Sort the array in descending order using Timsort (Insertion Sort for small segments)."""
    # Traverse through elements starting from the second element
    for i in range(left + 1, right + 1):
        # Store the current element (key) to be compared
        key = arr[i]
        # Initialize the index of the previous element
        j = i - 1
        # Move elements of arr[0...i-1] that are smaller than key, to one position ahead
        while j >= left and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

#---------------------------------------------------------------------------------------------------

#25/08/2024
#creating the own newline character using own printfunction
#import sys from handle console (or)terminal

def sakthi_add_newline(*input_texts, sep=' ', end='\n', file = sys.stdout, flush=False):
    """Customizing the print function to change newine character"""
    #replacing the newline character to 'sakthi'
    #iterating the tuple to implement this custom newline character
    custom_newline_texts = [input_text.replace('sakthi', end) for input_text in input_texts]

    #convert the tuple to sinlge string
    #join function to form string
    output = sep.join(str(custom_newline_text) for custom_newline_text in custom_newline_texts)

    #moving the cursor to newline and print on console
    file.write(output + end)

    #conditional test to check the buffer mechanism needed or not
    if flush:
        sys.stdout.flush()

#---------------------------------------------------------------------------------------------------

#25/08/2024
#creating the own newline character using own printfunction
#import sys from handle console (or)terminal

def sakthi_add_tab_space(*input_texts, sep=' ', end='\t', file = sys.stdout, flush=False):
    """Customizing the print function to change newine character"""
    #replacing the newline character to 'sakthi'
    #iterating the tuple to implement this custom newline character
    custom_newline_texts = [input_text.replace('sakthi', end) for input_text in input_texts]

    #convert the tuple to sinlge string
    #join function to form string
    output = sep.join(str(custom_newline_text) for custom_newline_text in custom_newline_texts)

    #moving the cursor to newline and print on console
    file.write(output + end)

    #conditional test to check the buffer mechanism needed or not
    if flush:
        sys.stdout.flush()


#---------------------------------------------------------------------------------------------------


def sakthi_backspace(*input_texts, sep=' ', end='\n', file=sys.stdout, flush=False):
    """Custom function to replace 'sakthi' with a backspace character."""
    # Replace 'sakthi' in each input with the backspace character '\b'
    custom_backspace_texts = [input_text.replace('sakthi', '\b') for input_text in input_texts]

    # Convert the tuple to a single string and join them with the separator
    output = sep.join(str(custom_backspace_text) for custom_backspace_text in custom_backspace_texts)

    # Print the final output to the console
    file.write(output + end)

    # Check if we need to flush the output buffer
    if flush:
        sys.stdout.flush()
#---------------------------------------------------------------------------------------------------


def sakthi_add_vertical_tab(*input_texts, sep=' ', end='\n', file=sys.stdout, flush=False):
    """Custom function to replace 'sakthi' with a vertical tab character."""
    # Replace 'sakthi' in each input with the vertical tab character '\v'
    custom_vertical_tab_texts = [input_text.replace('sakthi', '\v') for input_text in input_texts]

    # Convert the tuple to a single string and join them with the separator
    output = sep.join(str(custom_vertical_tab_text) for custom_vertical_tab_text in custom_vertical_tab_texts)

    # Print the final output to the console
    file.write(output + end)

    # Check if we need to flush the output buffer
    if flush:
        sys.stdout.flush()

#---------------------------------------------------------------------------------------------------


def sakthi_add_form_newline(*input_texts, sep=' ', end='\n', file=sys.stdout, flush=False):
    """Custom function to replace 'sakthi' with a form feed character."""
    # Replace 'sakthi' in each input with the form feed character '\f'
    custom_form_feed_texts = [input_text.replace('sakthi', '\f') for input_text in input_texts]

    # Convert the tuple to a single string and join them with the separator
    output = sep.join(str(custom_form_feed_text) for custom_form_feed_text in custom_form_feed_texts)

    # Print the final output to the console
    file.write(output + end)

    # Check if we need to flush the output buffer
    if flush:
        sys.stdout.flush()

#---------------------------------------------------------------------------------------------------


def sakthi_sart_from_first(*input_texts, sep=' ', end='\n', file=sys.stdout, flush=False):
    """Custom function to replace 'sakthi' with a carriage return character."""
    # Replace 'sakthi' in each input with the carriage return character '\r'
    custom_carriage_return_texts = [input_text.replace('sakthi', '\r') for input_text in input_texts]

    # Convert the tuple to a single string and join them with the separator
    output = sep.join(str(custom_carriage_return_text) for custom_carriage_return_text in custom_carriage_return_texts)

    # Print the final output to the console
    file.write(output + end)

    # Check if we need to flush the output buffer
    if flush:
        sys.stdout.flush()



#---------------------------------------------------------------------------------------------------

def sakthi_unicode_character(code_point):
    #define a 'unicode_mapping' dictionary
    unicode_mapping = {97: 'a', 65: 'A', 66: 'B'}
    #continue it for all the characters
    # Retrieve the Unicode character from the mapping table
    character = unicode_mapping[code_point]
    #-----------------Return it--------------#
    
    # Encode the character using UTF-8 --------------- unnecessary
    encoded_character = character.encode('utf-8')
    
    # Return the encoded character as a string---------unnecessary
    return encoded_character.decode('utf-8')


#---------------------------------------------------------------------------------------------------


#26/08/2024
#creatinh a custom function for lower to upper case convertion
def sakthi_change_capital_A_B_C_D(sequence_of_characters):
    """Transforming the lowercase letter in the string to uppercase"""
    #defing a empty list to hold the uppercase character after transformation
    output = []

    #Iterating the string for converting one by one
    for character in sequence_of_characters:
        #conditional test to check a alphabetical lowercase letters
        if 'a' <= character <= 'z':
            #extracting th e Unicode number for each individual character
            unicode = ord(character)

            #finding the corresponding unicode for it's upppercase character
            #By substracting '32' we get the unicode for uppercase characters
            unicode_for_uppercase = unicode - 32

            #converting the transformed unicode back into character using 'chr' function
            #Appending the uppercase lettter to output list
            output.append(chr(unicode_for_uppercase))

        #handling the non-alphabetical character in else
        else:
            #Else block executed only when the chacter is upper or any symbols
            #append the characters without transforming
            output.append(character)

    #Format the output list into a string
    output_string = ''.join(output)

    #return the transformed uppercase string
    return output_string


#---------------------------------------------------------------------------------------------------


def sakthi_change_to_lowercase(sequence_of_characters):
    """Transform uppercase letters in the string to lowercase."""
    # Define an empty list to hold the lowercase characters after transformation
    output = []

    # Iterate over each character in the string to convert one by one
    for character in sequence_of_characters:
        # Conditional test to check if the character is an uppercase letter
        if 'A' <= character <= 'Z':
            # Extract the Unicode number for each individual character
            unicode = ord(character)

            # Find the corresponding Unicode for its lowercase character
            # By adding '32' we get the Unicode for lowercase characters
            unicode_for_lowercase = unicode + 32

            # Convert the transformed Unicode back into a character using 'chr' function
            # Append the lowercase letter to the output list
            output.append(chr(unicode_for_lowercase))

        # Handle non-alphabetical characters in the else block
        else:
            # Else block executed only when the character is not an uppercase letter
            # Append the characters without transforming
            output.append(character)

    # Format the output list into a string
    output_string = ''.join(output)

    # Return the transformed lowercase string
    return output_string

#------------------------------------------------------------------------------------------

def sakthi_to_ascii_values(sequence_of_characters):
    """Convert each character in the string to its ASCII value."""
    # Define an empty list to hold the ASCII values
    ascii_values = []

    # Iterate over each character in the string
    for character in sequence_of_characters:
        # Get the ASCII value of the character using ord() function
        ascii_value = ord(character)
        
        # Append the ASCII value to the list
        ascii_values.append(ascii_value)

    # Format the list of ASCII values into a string with space separation
    ascii_string = ' '.join(str(value) for value in ascii_values)

    # Return the string of ASCII values
    return ascii_string

#------------------------------------------------------------------------------------------

def sakthi_to_hexadecimal_values(sequence_of_characters):
    """Convert each character in the string to its hexadecimal value."""
    # Define an empty list to hold the hexadecimal values
    hex_values = []

    # Iterate over each character in the string
    for character in sequence_of_characters:
        # Get the ASCII value of the character using ord() function
        ascii_value = ord(character)
        
        # Convert the ASCII value to hexadecimal and format it to two digits
        hex_value = format(ascii_value, '02X')
        
        # Append the hexadecimal value to the list
        hex_values.append(hex_value)

    # Format the list of hexadecimal values into a string with space separation
    hex_string = ' '.join(hex_values)

    # Return the string of hexadecimal values
    return hex_string

# Example usage of the custom function
text_to_convert = "Hello, Sakthi!"

#------------------------------------------------------------------------------------------

def sakthi_to_binary_values(sequence_of_characters):
    """Convert each character in the string to its binary value."""
    # Define an empty list to hold the binary values
    binary_values = []

    # Iterate over each character in the string
    for character in sequence_of_characters:
        # Get the ASCII value of the character using ord() function
        ascii_value = ord(character)
        
        # Convert the ASCII value to binary and format it to 8 bits
        binary_value = format(ascii_value, '08b')
        
        # Append the binary value to the list
        binary_values.append(binary_value)

    # Format the list of binary values into a string with space separation
    binary_string = ' '.join(binary_values)

    # Return the string of binary values
    return binary_string

#------------------------------------------------------------------------------------------

def sakthi_to_decimal_values(sequence_of_characters):
    """Convert each character in the string to its decimal ASCII value."""
    # Define an empty list to hold the decimal values
    decimal_values = []

    # Iterate over each character in the string
    for character in sequence_of_characters:
        # Get the ASCII value of the character using ord() function
        decimal_value = ord(character)
        
        # Append the decimal value to the list
        decimal_values.append(decimal_value)

    # Format the list of decimal values into a string with space separation
    decimal_string = ' '.join(str(value) for value in decimal_values)

    # Return the string of decimal values
    return decimal_string


#------------------------------------------------------------------------------------------


def sakthi_to_octal_values(sequence_of_characters):
    """Convert each character in the string to its octal value."""
    # Define an empty list to hold the octal values
    octal_values = []

    # Iterate over each character in the string
    for character in sequence_of_characters:
        # Get the ASCII value of the character using ord() function
        ascii_value = ord(character)
        
        # Convert the ASCII value to octal and format it to three digits (if needed)
        octal_value = format(ascii_value, 'o').zfill(3)
        
        # Append the octal value to the list
        octal_values.append(octal_value)

    # Format the list of octal values into a string with space separation
    octal_string = ' '.join(octal_values)

    # Return the string of octal values
    return octal_string


#------------------------------------------------------------------------------------------


def sakthi_decimal_to_binary(*numbers):
    """Convert decimal numbers (or a single number) to binary values."""
    # Define an empty list to hold the binary values
    binary_values = []

    # Process each number in the input
    for number in numbers:
        # Check if the input is a single number or a string of numbers
        if isinstance(number, str):
            # Split the string by spaces and convert each part to an integer
            number_list = map(int, number.split())
        else:
            # Convert the single number to a list
            number_list = [number]
        
        # Convert each number to binary
        for num in number_list:
            # Convert the number to binary and format it to a binary string
            binary_value = format(num, 'b')
            
            # Append the binary value to the list
            binary_values.append(binary_value)

    # Format the list of binary values into a string with space separation
    binary_string = ' '.join(binary_values)

    # Return the string of binary values
    return binary_string


#--------------------------------------------------------------------------------------


def sakthi_decimal_to_octal_values(*numbers):
    """Convert decimal numbers (or a single number) to octal values."""
    # Define an empty list to hold the octal values
    octal_values = []

    # Process each number in the input
    for number in numbers:
        # Check if the input is a single number or a string of numbers
        if isinstance(number, str):
            # Split the string by spaces and convert each part to an integer
            number_list = map(int, number.split())
        else:
            # Convert the single number to a list
            number_list = [number]
        
        # Convert each number to octal
        for num in number_list:
            # Convert the number to octal and format it to an octal string
            octal_value = format(num, 'o')
            
            # Append the octal value to the list
            octal_values.append(octal_value)

    # Format the list of octal values into a string with space separation
    octal_string = ' '.join(octal_values)

    # Return the string of octal values
    return octal_string


#------------------------------------------------------------------------------------------


def sakthi_decimal_to_hexadecimal_values(*numbers):
    """Convert decimal numbers (or a single number) to hexadecimal values."""
    # Define an empty list to hold the hexadecimal values
    hex_values = []

    # Process each number in the input
    for number in numbers:
        # Check if the input is a single number or a string of numbers
        if isinstance(number, str):
            # Split the string by spaces and convert each part to an integer
            number_list = map(int, number.split())
        else:
            # Convert the single number to a list
            number_list = [number]
        
        # Convert each number to hexadecimal
        for num in number_list:
            # Convert the number to hexadecimal and format it to uppercase
            hex_value = format(num, 'X')
            
            # Append the hexadecimal value to the list
            hex_values.append(hex_value)

    # Format the list of hexadecimal values into a string with space separation
    hex_string = ' '.join(hex_values)

    # Return the string of hexadecimal values
    return hex_string


#---------------------------------------------------------------------------------------

def sakthi_binary_to_decimal_values(*binaries):
    """Convert binary numbers (or a single binary string) to decimal values."""
    # Define an empty list to hold the decimal values
    decimal_values = []

    # Process each binary input
    for binary in binaries:
        # Check if the input is a single binary string or a string of binaries
        if isinstance(binary, str):
            # Split the string by spaces and convert each binary to decimal
            binary_list = binary.split()
        else:
            # Convert the single binary number to a list
            binary_list = [binary]
        
        # Convert each binary string to decimal
        for bin_str in binary_list:
            # Convert the binary string to a decimal number
            decimal_value = int(bin_str, 2)
            
            # Append the decimal value to the list
            decimal_values.append(decimal_value)

    # Format the list of decimal values into a string with space separation
    decimal_string = ' '.join(str(value) for value in decimal_values)

    # Return the string of decimal values
    return decimal_string


#------------------------------------------------------------------------------------------


def sakthi_character_to_ascii_code(character):
    # Encode the character using UTF-8
    encoded_character = character.encode('utf-8')
    
    # Retrieve the Unicode code point from the encoded bytes
    code_point = int.from_bytes(encoded_character, byteorder='big')
    
    return code_point


#------------------------------------------------------------------------------------------


# 27/08/2024
# creating the function to remove leading and trailing whitespace
def sakthi_clean_front_and_back(dirty_texts):
    """Removing the leading and trailing whitespace from string"""
    #defining a set to hold alll the whitespace characters
    if dirty_texts:
        whitespace = {' ', '\t', '\n', '\f', '\r','\v'}

        # defining a variable to start where with characters
        # negulecting the whitespace
        start = 0

        #defining a flag with active state
        active = True
        #while loop to move the 'start' to where the character is persent
        while active:
            #conditional test to check whether the character is whitespace
            if start < len(dirty_texts) and dirty_texts[start] in whitespace:
                start = start + 1
            
            else:
                active = False
        
        #define a 'end' variable to hold the index of character ending not whitespace not ending
        end = len(dirty_texts) - 1

        # again chage the state of active to 'True'
        active = True

        #while loop to move the 'end' to where the character is persent
        while active:
            #conditional test to check whether the character is whitespace
            if end >= start and dirty_texts[end] in whitespace:
                end = end - 1
            
            else:
                active = False

        clean_string = dirty_texts[start : end+1]
        # Returning the string with no whitespace at fron and back
        return clean_string


#-----------------------------------------------------------------------------

def sakthi_clean_left(dirty_texts):
    """Remove leading whitespace from string."""
    if dirty_texts:
        whitespace = {' ', '\t', '\n', '\f', '\r', '\v'}

        # Remove leading whitespace
        start = 0
        while start < len(dirty_texts) and dirty_texts[start] in whitespace:
            start += 1

        # Return the cleaned string
        return dirty_texts[start:]
    return dirty_texts


#-------------------------------------------------------------------------

def sakthi_clean_right(dirty_texts):
    """Remove trailing whitespace from string."""
    if dirty_texts:
        whitespace = {' ', '\t', '\n', '\f', '\r', '\v'}

        # Remove trailing whitespace
        end = len(dirty_texts) - 1
        while end >= 0 and dirty_texts[end] in whitespace:
            end -= 1

        # Return the cleaned string
        return dirty_texts[:end + 1]
    return dirty_texts


#------------------------------------------------------------------------------------


# 27/08/2024
# creating method that remove prefix if exists
def sakthi_remove_perfix(texts, prefix):
    """Remove the specified prefix from string"""
    #conditional test to check string starts with prefix mentioned
    if texts.startswith(prefix):
        return texts[len(prefix):]
    return texts

#------------------------------------------------------------------------------------

def sakthi_remove_suffix(texts, suffix):
    """Remove the specified suffix from the string if it exists."""
    # Conditional test to check if the string ends with the specified suffix
    if texts.endswith(suffix):
        return texts[:-len(suffix)]
    return texts


#------------------------------------------------------------------------------------------

# 27/08/2024
#creating a startswith function
def sakthi_it_starts_with(texts, prefix):
    """return boolean if the string starts with specified prefix"""
    #conditional test to check length of prefix is less than length of string
    if len(prefix) > len(texts):
        #it is not possible
        return False
    return (texts[:len(prefix)] == prefix)

#------------------------------------------------------------------------------------------


def it_ends_with(texts, suffix):
    """Return boolean if the string ends with the specified suffix."""
    # Conditional test to check if the suffix length is greater than the string length
    if len(suffix) > len(texts):
        # It is not possible for the suffix to be at the end
        return False
    # Check if the end of the string matches the suffix
    return (texts[-len(suffix):] == suffix)

#------------------------------------------------------------------------------------------


# 30/08/2024
# Creating a function for creatinf a list of numbers
def i_need_number_list(start, stop=None, step=1):
    """generating a list of elemnts"""
    if stop == None:
        start, stop = 0, step
    if step == 0:
        raise ValueError("Step cannot be zero!")
    current = start

    # while loop for g eneration numbers
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current = current + step


#------------------------------------------------------------------------------------------


# 30/08/2024
# Find ing the length of function starting from one
def how_many_elements_present(list):
    """returns the length of the iterable from one"""
    # Define a temporary variable for counting
    count = 0
    # Define a loop where there is no need to use iterator
    for _ in list:
        count = count + 1
    
    #return the length of the list
    return count



#------------------------------------------------------------------------------------------

# 29/08/2024
# Creating a title function
def make_title(input_texts):
    """Capitailze the first character of each words"""
    #initializing a empty string to store output
    output = ""
    
    # A flag veriable to capitalize first character
    change_nest_character = True

    # Loop to extracte each and every character
    for charcter in input_texts:
        if change_nest_character:
            # Ternary conditional test, if the character is alphabet than it captalize
            # If character is not alphabet than do nothing
            output += charcter.upper() if charcter.isalpha() else charcter

            # Ternary conditional test for flag variable
            change_nest_character = False if charcter.isalpha() else True
        else:
            output += charcter.lower() if charcter.isalpha() else charcter
            # Ternary conditional test for flag variable
            change_nest_character = not charcter.isalpha()
    
    # Return the output
    return output



#------------------------------------------------------------------------------------------


# 28/08/2024
# creating the custom sum function for handling list
def sakthi_total_of_list(iterable, start=0):
    """Add the elements together and returns the total"""
    #conditional test check the list is non-empty
    if iterable:
        #initializing a temporary variable as 0
        total = start

        #iterate each elements and add together
        for element in iterable:
            total = total + element
        
        # Return the total
        return total


#------------------------------------------------------------------------------------------

#29/08/2024
#creating a custom 'min' function
def sakthi_lowest_number(*any_input, key=None):
    """find the minimum value in the given elements"""
    if len(any_input) == 1:
        #conclude that given item may be list
        iterable = any_input[0]
        iterator = iter(iterable)
        smallest = next(iterator)
    else:
        iterator = iter(any_input)
        smallest = next(iterator)
    # Iterate each element int iterator
    for element in iterator:
        # Conditional test to check key ia any function
        if key  is not None:
            if key(element) < key(smallest):
                smallest = element
        else:
            if element < smallest:
                smallest = element
                
    return smallest






#-------------------------------------------------------------------------------------------------------------------------------------------------

