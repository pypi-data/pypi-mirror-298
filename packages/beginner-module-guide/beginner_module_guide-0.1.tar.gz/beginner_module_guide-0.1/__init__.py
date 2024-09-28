import os

def generate():
    """Creates a directory containing TXT files with module usage guides."""

    directory_name = "module_guides"
    os.mkdir(directory_name)

    # Add your TXT files to the directory here
    # For example:
    with open(os.path.join(directory_name, "os_guide.txt"), "w") as f:
        f.write('''Course: Introduction to the os Module in Python
Module Overview
The os module in Python provides functions for interacting with the operating system. It allows you to perform tasks like:
* Creating, deleting, and renaming files and directories.
* Getting information about files and directories.
* Changing current working directories.
* Executing external commands.
Important Functions
1. File and Directory Operations
* os.path.exists(path): Checks if a file or directory exists.
* os.path.isfile(path): Checks if a path is a file.
* os.path.isdir(path): Checks if a path is a directory.
* os.mkdir(path): Creates a new directory.
* os.makedirs(path): Creates a directory and its parent directories if they don't exist.
* os.rmdir(path): Removes an empty directory.
* os.removedirs(path): Removes a directory and its parent directories if they are empty.
* os.rename(src, dst): Renames a file or directory.
* os.listdir(path): Lists the contents of a directory.
* os.walk(path): Recursively walks through a directory tree.
2. File Information
* os.path.getsize(path): Gets the size of a file.
* os.path.getmtime(path): Gets the modification time of a file.
* os.path.getatime(path): Gets the access time of a file.
* os.path.getctime(path): Gets the creation time of a file.
3. Current Working Directory
* os.getcwd(): Gets the current working directory.
* os.chdir(path): Changes the current working directory.
4. Environment Variables
* os.environ: A dictionary containing environment variables.
* os.getenv(key): Gets the value of an environment variable.
* os.putenv(key, value): Sets the value of an environment variable.
5. Execution
* os.system(command): Executes a system command.
* os.popen(command): Opens a pipe to a child process.
Example Usage


Python




import os

# Create a directory
os.mkdir("new_directory")

# List files in the current directory
files = os.listdir()
print(files)

# Get the size of a file
file_size = os.path.getsize("my_file.txt")
print(file_size)

# Change the current working directory
os.chdir("new_directory")

# Execute a command
result = os.system("ls")
print(result)

Additional Tips
* Always use absolute paths or relative paths relative to the current working directory.
* Handle potential exceptions like OSError when working with file and directory operations.
* Be aware of platform-specific differences in file paths and system commands.
By mastering these functions, you'll be able to effectively interact with the file system and perform various tasks in your Python programs.
''')


    with open(os.path.join(directory_name, "sys_guide.txt"), "w") as f:
        f.write('''Course: Introduction to the sys Module in Python
Module Overview
The sys module in Python provides access to system-specific parameters and functions. It allows you to interact with the Python interpreter and its environment.
Important Functions
1. Arguments
* sys.argv: A list containing command-line arguments passed to the script.
Python
import sys

print(sys.argv)
This will print a list of arguments, including the script name as the first element.
2. Exit Status
   * sys.exit(code): Terminates the Python interpreter with the specified exit code.
Python
import sys

if some_condition:
   sys.exit(1)  # Indicate an error
else:
   sys.exit(0)  # Indicate success

3. Path
      * sys.path: A list of directories that Python searches for modules.
Python
import sys

print(sys.path)
This will print the current search path.
4. Platform Information
         * sys.platform: The name of the operating system platform.
Python
import sys

print(sys.platform)
This will print the platform name, such as 'win32' for Windows or 'linux' for Linux.
5. Version Information
            * sys.version: A string containing the Python version information.
Python
import sys

print(sys.version)
This will print the version number and build information.
6. Standard Streams
               * sys.stdin: Standard input stream.
               * sys.stdout: Standard output stream.
               * sys.stderr: Standard error stream.
Example Usage


Python




import sys

# Print command-line arguments
print("Arguments:", sys.argv)

# Check the platform
print("Platform:", sys.platform)

# Read from standard input
user_input = input("Enter your name: ")
print("Hello,", user_input)

# Write to standard output
print("This is a message to standard output.")

# Write to standard error
sys.stderr.write("This is an error message.\n")

Additional Tips
               * Use sys.argv to create command-line tools.
               * Control the exit status of your scripts to indicate success or failure.
               * Modify sys.path to add custom module directories.
               * Use standard streams for input and output in your programs.
By understanding and using these functions, you can effectively interact with the Python interpreter and customize its behavior.
''')


    with open(os.path.join(directory_name, "math_guide.txt"), "w") as f:
        f.write('''Course: Introduction to the math Module in Python
Module Overview
The math module in Python provides a collection of mathematical functions and constants. It's essential for performing various numerical calculations.
Important Functions
1. Trigonometric Functions
* math.sin(x): Calculates the sine of x (in radians).
* math.cos(x): Calculates the cosine of x (in radians).
* math.tan(x): Calculates the tangent of x (in radians).
* math.asin(x): Calculates the arcsine of x (in radians).
* math.acos(x): Calculates the arccosine of x (in radians).
* math.atan(x): Calculates the arctangent of x (in radians).
* math.atan2(y, x): Calculates the arctangent of y/x (in radians).
2. Logarithmic Functions
* math.log(x): Calculates the natural logarithm of x.
* math.log10(x): Calculates the base-10 logarithm of x.
* math.log2(x): Calculates the base-2 logarithm of x.
3. Exponential Functions
* math.exp(x): Calculates the exponential of x (e^x).
* math.pow(x, y): Calculates x raised to the power of y.
* math.sqrt(x): Calculates the square root of x.
4. Other Functions
* math.factorial(x): Calculates the factorial of x.
* math.ceil(x): Returns the smallest integer greater than or equal to x.
* math.floor(x): Returns the largest integer less than or equal to x.  
* math.trunc(x): Truncates x to an integer.
* math.fabs(x): Calculates the absolute value of x.
* math.frexp(x): Breaks x into its mantissa and exponent.
* math.modf(x): Breaks x into its integer and fractional parts.
5. Constants
* math.pi: The mathematical constant pi (approximately 3.14159).
* math.e: The mathematical constant e (approximately 2.71828).
Example Usage


Python




import math

# Trigonometric functions
angle = math.pi / 4
sine = math.sin(angle)
cosine = math.cos(angle)
tangent = math.tan(angle)
print(sine, cosine, tangent)

# Logarithmic functions
number = 100
natural_log = math.log(number)
base10_log = math.log10(number)
base2_log = math.log2(number)
print(natural_log, base10_log, base2_log)

# Exponential functions
exponent = 2
result = math.exp(exponent)
power = math.pow(2, 3)
square_root = math.sqrt(16)
print(result, power, square_root)

# Other functions
factorial = math.factorial(5)
ceiling = math.ceil(3.7)
floor = math.floor(3.7)
truncation = math.trunc(3.7)
absolute_value = math.fabs(-5)
print(factorial, ceiling, floor, truncation, absolute_value)

Additional Tips
* Ensure that angles are provided in radians.
* Use the appropriate function based on the specific mathematical operation you need to perform.
* Be aware of potential domain errors for functions like logarithms and square roots.
* For more advanced mathematical operations, consider using libraries like NumPy.
By understanding and using these functions, you'll be able to perform a wide range of mathematical calculations in your Python programs.
Sources
1. https://github.com/YinHk-Notes/javascript-cheatsheet-and-note
''')


    with open(os.path.join(directory_name, "random_guide.txt"), "w") as f:
        f.write('''
Course: Introduction to the random Module in Python
Module Overview
The random module in Python provides functions for generating random numbers and making random choices. It's useful for various applications, such as simulations, games, and data analysis.
Important Functions
1. Generating Random Numbers
* random.random(): Returns a random floating-point number between 0 and 1 (exclusive).
* random.randint(a, b): Returns a random integer between a and b, inclusive.
* random.randrange(start, stop[, step]): Returns a random item from a range of integers, similar to range().  
* random.uniform(a, b): Returns a random floating-point number between a and b.
* random.choice(sequence): Returns a random element from a sequence (e.g., list, tuple, string).
* random.sample(sequence, k): Returns a k-length list of unique elements chosen from the sequence.
2. Shuffling Sequences
* random.shuffle(sequence): Shuffles a sequence in place.
3. Seeding the Random Number Generator
* random.seed(a=None): Sets the seed for the random number generator. This ensures reproducibility of random sequences.
Example Usage


Python




import random

# Generate random numbers
random_float = random.random()
random_int = random.randint(1, 10)
random_choice = random.choice(["apple", "banana", "cherry"])
print(random_float, random_int, random_choice)

# Shuffle a list
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(numbers)

# Sample elements from a list
sample = random.sample(numbers, 3)
print(sample)

# Set the seed for reproducibility
random.seed(42)
random_number = random.random()
print(random_number)

Additional Tips
* Use random.seed() to control the randomness and ensure reproducible results in certain scenarios.
* For more advanced random number generation, consider using libraries like numpy.random.
* Be aware that the random module provides pseudo-random numbers, not truly random ones.
By understanding and using these functions, you'll be able to introduce randomness into your Python programs for various purposes.
Sources
1. https://github.com/Malek-Abdelal/reading-notes
''')


    with open(os.path.join(directory_name, "datetime_guide.txt"), "w") as f:
        f.write('''
Course: Introduction to the datetime Module in Python
What is datetime?
The datetime module in Python is a tool for working with dates and times. It lets you do things like:
* Get the current date and time.
* Create specific dates and times.
* Calculate differences between dates and times.
* Format dates and times in different ways.
Key Classes
1. datetime.datetime: This represents a specific point in time, including the year, month, day, hour, minute, second, and microsecond.
2. datetime.date: This represents a date, without the time.
3. datetime.time: This represents a time, without the date.
4. datetime.timedelta: This represents a difference between two dates or times.
How to Use It
1. Getting the Current Date and Time:


Python




import datetime

now = datetime.datetime.now()
print(now)  # Output: 2023-11-28 12:34:56.789012

2. Creating Specific Dates and Times:


Python




# Create a specific date
birthday = datetime.date(1990, 1, 1)
print(birthday)  # Output: 1990-01-01

# Create a specific time
wakeup_time = datetime.time(7, 30)
print(wakeup_time)  # Output: 07:30:00

3. Calculating Differences:


Python




# Calculate the difference between two dates
today = datetime.date.today()
birthday = datetime.date(1990, 1, 1)
difference = today - birthday
print(difference.days)  # Output: 11887 (number of days)

4. Formatting Dates and Times:


Python




now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
formatted_time = now.strftime("%H:%M:%S")
print(formatted_date)  # Output: 2023-11-28
print(formatted_time)  # Output: 12:34:56

Common Tasks
* Timezones: The datetime module can handle different timezones.
* Date Arithmetic: You can add or subtract timedelta objects to dates and times.
* Time Intervals: You can create time intervals using timedelta objects.
By mastering these basics, you'll be able to work effectively with dates and times in your Python programs!
''')


    with open(os.path.join(directory_name, "json_guide.txt"), "w") as f:
        f.write('''
Course: Introduction to the json Module in Python
What is JSON?
JSON (JavaScript Object Notation) is a popular data format used to store and exchange data. It's a lightweight, human-readable format that's easy to work with in Python.
The json Module
The json module in Python provides functions for encoding and decoding JSON data.
Key Functions
1. Encoding JSON:
* json.dumps(obj): Converts a Python object (like a list, dictionary, or string) into a JSON string.
Python
import json

data = {"name": "Alice", "age": 30, "city": "New York"}
json_string = json.dumps(data)
print(json_string)  # Output: {"name": "Alice", "age": 30, "city": "New York"}

2. Decoding JSON:
   * json.loads(s): Converts a JSON string into a Python object.
Python
json_string = '{"name": "Bob", "age": 25}'
data = json.loads(json_string)
print(data)  # Output: {'name': 'Bob', 'age': 25}

Additional Functions
      * json.dump(obj, fp): Dumps a Python object into a JSON file.
      * json.load(fp): Loads a JSON file into a Python object.
      * json.loads(s, cls=None): Decodes a JSON string using a custom decoder class.
      * json.dumps(obj, indent=None): Dumps a Python object into a JSON string with indentation for better readability.
Common Use Cases
      * Data Storage: Storing data in JSON files.
      * Data Exchange: Sending and receiving data between applications.
      * API Interactions: Communicating with web APIs.
Example


Python




import json

# Create a Python object
data = {"fruits": ["apple", "banana", "orange"], "numbers": [1, 2, 3]}

# Convert to JSON string
json_string = json.dumps(data, indent=4)  # Indent for better readability
print(json_string)

# Save to a file
with open("data.json", "w") as f:
   json.dump(data, f)

# Load from a file
with open("data.json", "r") as f:
   loaded_data = json.load(f)
print(loaded_data)

By understanding these concepts, you'll be able to effectively work with JSON data in your Python programs.
''')


    with open(os.path.join(directory_name, "crpytography_guide.txt"), "w") as f:
        f.write('''
Course: Introduction to the cryptography Module in Python
What is Cryptography?
Cryptography is the practice of securing information by transforming it into a secret code. It's used to protect sensitive data from unauthorized access.
The cryptography Module
The cryptography module in Python is a powerful library that provides tools for cryptographic operations. It's designed to be secure, easy to use, and well-documented.
Key Concepts
* Encryption: The process of transforming plain text into ciphertext.
* Decryption: The process of transforming ciphertext back into plain text.
* Key: A secret value used for encryption and decryption.
* Cipher: The algorithm used for encryption and decryption.
Important Functions
1. Hashing:
* cryptography.hazmat.primitives.hashes.SHA256(): Creates a SHA-256 hash object.
Python
from cryptography.hazmat.primitives import hashes

digest = hashes.Hash(hashes.SHA256())
digest.update(b"Hello, world!")
hash_value = digest.finalize()
print(hash_value)

2. Symmetric Encryption:
   * cryptography.fernet.Fernet(): Creates a Fernet encryption object.
Python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

message = b"This is a secret message"
encrypted_message = fernet.encrypt(message)
decrypted_message = fernet.decrypt(encrypted_message)

3. Asymmetric Encryption:
      * cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(): Generates an RSA private key.
      * cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey.encrypt(): Encrypts data using an RSA public key.
      * cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey.decrypt(): Decrypts data using an RSA private key.
Additional Topics
      * Key Management: Storing, generating, and distributing keys securely.
      * Digital Signatures: Verifying the authenticity and integrity of data.
      * MACs (Message Authentication Codes): Ensuring data integrity and authenticity.
      * Padding: Adding extra data to ensure that the plaintext length is compatible with the cipher.
Remember
      * Security: Always handle cryptographic keys securely and avoid hardcoding them in your code.
      * Best Practices: Follow cryptographic best practices and stay updated on security vulnerabilities.
      * Complexity: Cryptography can be complex. Consider using higher-level libraries like cryptography to simplify the process.
By understanding these concepts and using the cryptography module effectively, you can protect sensitive data in your Python applications.
''')


    with open(os.path.join(directory_name, "rquests_guide.txt"), "w") as f:
        f.write('''
Course: Introduction to the requests Module in Python
What is requests?
The requests module is a popular HTTP library in Python that simplifies making HTTP requests. It's designed to be user-friendly and handles common HTTP scenarios efficiently.
Key Functions
1. Making GET Requests:
* requests.get(url): Sends a GET request to the specified URL.
Python
import requests

response = requests.get("https://api.example.com/data")
print(response.text)

2. Making POST Requests:
   * requests.post(url, data=None, json=None): Sends a POST request to the specified URL.
Python
data = {"name": "Alice", "age": 30}
response = requests.post("https://api.example.com/users", json=data)
print(response.json())

3. Making Other HTTP Methods:
      * requests.put(url, data=None, json=None): Sends a PUT request.
      * requests.patch(url, data=None, json=None): Sends a PATCH request.
      * requests.delete(url): Sends a DELETE request.
4. Handling Responses:
      * response.status_code: The HTTP status code of the response.
      * response.text: The text content of the response.
      * response.json(): Returns the JSON-decoded content of the response.
      * response.content: The raw content of the response.
5. Headers:
      * headers argument: Pass a dictionary of headers with the request.
Python
headers = {"Authorization": "Bearer your_token"}
response = requests.get("https://api.example.com/protected_data", headers=headers)

Example


Python




import requests

# Make a GET request
response = requests.get("https://api.github.com/users/octocat")

# Check the status code
if response.status_code == 200:
   # Get the JSON data
   data = response.json()
   print(data["login"])
else:
   print("Error:", response.status_code)

Additional Features
         * Session Management: Use requests.Session() for persistent connections and cookies.
         * Authentication: Implement authentication mechanisms like basic auth, OAuth, or API keys.
         * Timeouts: Set timeouts for requests to avoid blocking.
         * Proxies: Use proxies for network requests.
By understanding these basics, you'll be able to effectively interact with web APIs and retrieve data using the requests module.
''')


    with open(os.path.join(directory_name, "tkinter_guide.txt"), "w") as f:
        f.write('''Course: Introduction to the tkinter Module in Python
What is tkinter?
The tkinter module is Python's standard GUI toolkit. It allows you to create graphical user interfaces (GUIs) for your applications.
Key Concepts
* Widgets: These are the basic building blocks of a GUI, such as buttons, labels, text boxes, and more.
* Window: The main container for your GUI elements.
* Event Handling: Responding to user interactions like button clicks or keyboard input.
Important Widgets
* tk.Label: Displays text or images.
* tk.Button: Creates a clickable button.
* tk.Entry: Creates a text entry field.
* tk.Text: Creates a multi-line text editor.
* tk.Canvas: Creates a drawing surface for lines, shapes, and images.
* tk.Frame: Creates a container for other widgets.
Creating a Basic Window


Python




import tkinter as tk

# Create a window
window = tk.Tk()

# Set window title
window.title("My First GUI")

# Run the event loop
window.mainloop()

Adding Widgets


Python




import tkinter as tk

# Create a window
window = tk.Tk()

# Create a label
label = tk.Label(window, text="Hello, world!")
label.pack()

# Create a button
button = tk.Button(window, text="Click me")
button.pack()

# Run the event loop
window.mainloop()

Event Handling


Python




import tkinter as tk

def button_click():
   print("Button clicked!")

# Create a window
window = tk.Tk()

# Create a button with a callback function
button = tk.Button(window, text="Click me", command=button_click)
button.pack()

# Run the event loop
window.mainloop()

Layouts
* pack(): Packs widgets into the parent container.
* grid(): Arranges widgets in a grid layout.
* place(): Positions widgets at specific coordinates.
Additional Features
* Geometry Management: Control the size and position of widgets.
* Fonts: Customize fonts for text.
* Colors: Set colors for widgets and backgrounds.
* Images: Load and display images.
* Menus: Create menus and submenus.
By understanding these basics, you can start creating simple GUIs in Python using tkinter. Remember to experiment and explore the various widgets and options available to build more complex interfaces.
''')


    with open(os.path.join(directory_name, "pyttsx_guide.txt"), "w") as f:
        f.write('''Course: Introduction to the pyttsx3 Module in Python
What is pyttsx3?
The pyttsx3 module is a text-to-speech engine for Python. It allows you to convert text into spoken words.
Key Functions
1. Speaking Text:
* engine.say(text): Speaks the specified text.
* engine.runAndWait(): Starts the speech engine and waits for it to finish speaking.
2. Setting Properties:
* engine.setProperty(name, value): Sets a property of the speech engine.
   * Common properties:
      * rate: Sets the speech rate (words per minute).
      * volume: Sets the volume (0-1).
      * voice: Sets the voice to use (if available).
3. Getting Properties:
* engine.getProperty(name): Gets the value of a property.
4. Saving Speech:
* engine.save_to_file(text, filename): Saves the spoken text to a file.
Example


Python




import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Adjust speech rate
engine.setProperty('volume', 1.0)  # Adjust volume

# Speak text
engine.say("Hello, world!")
engine.runAndWait()

# Save speech to a file
engine.save_to_file("hello.mp3", "Hello, world!")
engine.runAndWait()

Additional Tips
* Voices: Check if your system has available voices using engine.getProperty('voices').
* Error Handling: Handle potential errors using try-except blocks.
* Platform-Specific: The module may have platform-specific limitations.
* Naturalness: For more natural-sounding speech, consider using advanced text-to-speech engines or services.
By understanding these basics, you can easily convert text to speech in your Python applications using the pyttsx3 module.
''')

    print(f"Guide directory created: {directory_name}")