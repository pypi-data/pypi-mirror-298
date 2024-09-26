Perpetual Context is a proprietary algorithm for expanding the context window in Machine Learning and Deep Learning applications that use language models.

# Perpetual Context

This code is an algorithm projected, architected and developed by Sapiens Technology®️ and aims to manage context window memory in Artificial Intelligence projects for language models. It manages context memory by saving and indexing the encrypted dialogs for later consultation and return of excerpts referring to the input prompt, summarizing these excerpts when necessary to prevent the character sequence from exceeding the tokens limit previously established by the control variable. This makes it possible to establish a perpetual and limitless context even for language models with limited context windows.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Perpetual Context.

```bash
pip install perpetual-context
```

If you have a problem with one or more dependencies, you can install them manually via the requirements file.

```bash
pip install -r requirements.txt
```

## Usage
Basic usage example:
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter.
summary_file = perpetual_context.getSummaryTXT(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the txt file (accepts any file in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You will can use the constructor's "display_error_point" parameter to display or hide details of possible errors during execution.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext( # creation of the object for accessing class resources
    display_error_point=True # "True" to display error details if an error occurs, or "False" to display no error details
) # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter.
summary_file = perpetual_context.getSummaryTXT(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the txt file (accepts any file in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryCode" function returns the summary of a programming code contained in a string respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to variables
file_path = './files/file_name.py' # address read file
max_tokens = 200000 # maximum number of tokens to be returned in the summary
# opens the file addressed in the "file_path" variable in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "text" which will be passed to the parameter of the same name in the code summary function
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file: text = file.read() # reading the text contained in the file
# code for generating summary of read content
# returns a summary of the code contained in the variable of the "text" parameter with a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryCode(text=text, max_tokens=max_tokens) # function call that will return the summary of the code (accepts any type of code in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryText" function returns the summary of a string respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# opens the file addressed in the "file_path" variable in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "text" which will be passed to the parameter of the same name in the text summary function
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file: text = file.read() # reading the text contained in the file
# code for generating summary of read content
# returns a summary of the string contained in the variable of the "text" parameter with a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryText(text=text, max_tokens=max_tokens) # function call that will return the summary of the string (accepts any string value)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryTXT" function returns the summary of a text file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.txt' # address read file
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryTXT(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the txt file (accepts any type of file in text format)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryYouTube" function returns the summary of a YouTube video respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://www.youtube.com/watch?v=9iqn1HhFJ6c' # youtube video address
max_tokens = 10000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the video contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryYouTube(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of the video (only youtube videos)
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryWEBPage" function returns the summary of a WEB Page respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://en.wikipedia.org/wiki/Artificial_intelligence' # address of a web page
max_tokens = 20000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the web page contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryWEBPage(file_path=file_path, max_tokens=max_tokens) # function call that will return the summary of web page
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryPDF" function returns the summary of a PDF file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pdf' # pdf file address
max_tokens = 8000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the pdf file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryPDF(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in pdf format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
) # function call that will return the summary of pdf file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
Note that it is possible to define a main page with an integer referring to the page numbering in the "main_page" parameter, so the page in question will have a number of tokens in the summary greater than the number of tokens in the other pages.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pdf' # pdf file address
max_tokens = 8000 # maximum 8000 tokens in result string
main_page = 2 # page number 2 should have all the attention focused on it
# code for generating summary of read content
# returns a string with the summary of the pdf file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryPDF(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in pdf format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=main_page # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
) # function call that will return the summary of pdf file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
All file summary functions (of any type) will accept in the "file_path" parameter either a local file or a file at a web address.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://www.sjsu.edu/writingcenter/docs/handouts/Articles.pdf' # pdf file address
max_tokens = 1000 # maximum 1000 tokens in result string
main_page = 3 # page number 3 should have all the attention focused on it
# code for generating summary of read content
# returns a string with the summary of the pdf file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryPDF(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in pdf format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=main_page # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
) # function call that will return the summary of pdf file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryWord" function returns the summary of a Microsoft Word file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.docx' # microsoft word file address
max_tokens = 1000 # maximum 1000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the microsoft word file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryWord(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in docx format)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally
) # function call that will return the summary of microsoft word file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryPowerPoint" function returns the summary of a Microsoft Powerpoint file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pptx' # microsoft powerpoint file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the microsoft powerpoint file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryPowerPoint(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: pptx, ppsx, pptm)
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None # integer with the number of the page/slide that should receive the most attention, or "None" to distribute attention equally
) # function call that will return the summary of microsoft powerpoint file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryCSV" function returns the summary of a CSV file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv' # csv file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the csv file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryCSV(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in csv format)
    max_tokens=max_tokens # maximum tokens limit in result string
) # function call that will return the summary of csv file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryExcel" function returns the summary of a Microsoft Excel file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.xlsx' # microsoft excel file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the microsoft excel file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryExcel(
    file_path=file_path, # address of a local file or a file on the web (only accepts files in xlsx format)
    max_tokens=max_tokens # maximum tokens limit in result string
) # function call that will return the summary of microsoft excel file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryImage" function returns the summary of a image file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.jpg' # image file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the image file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryImage(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: webp, jpg, jpeg, png, gif, bmp, dng, mpo, tif, tiff, pfm)
    max_tokens=max_tokens # maximum tokens limit in result string
) # function call that will return the summary of image file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryAudio" function returns the summary of a audio file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.wav' # audio file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the audio file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryAudio(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: mp3, wav, mpeg, m4a, aac, ogg, flac, aiff, wma, ac3, amr)
    max_tokens=max_tokens # maximum tokens limit in result string
) # function call that will return the summary of audio file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryVideo" function returns the summary of a video file respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.mp4' # video file address
max_tokens = 4000 # maximum 4000 tokens in result string
# code for generating summary of read content
# returns a string with the summary of the video file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryVideo(
    file_path=file_path, # address of a local file or a file on the web (accepted file types: mp4, avi, mkv, mov, webm, flv, 3gp, wmv, ogv)
    max_tokens=max_tokens # maximum tokens limit in result string
) # function call that will return the summary of video file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "getSummaryFile" function returns the summary of any file accepted by the expert functions, respecting the tokens limit defined in the call.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# assigning values to parameter variables
file_path = './files/file_name.pdf' # file address
max_tokens = 8000 # maximum number of tokens to be returned in the summary
# code for generating summary of read content
# returns a string with the summary of the file contained in the address of the "file_path" parameter and a number of tokens equal to or less than that defined in the "max_tokens" parameter
summary_file = perpetual_context.getSummaryFile( # accepts microsoft word files, powerpoint, excel, pdf documents, csv spreadsheets, text files, code files, youtube video addresses, web page addresses, images, audios and videos
    file_path=file_path, # address of a local file or a file on the web
    max_tokens=max_tokens, # maximum tokens limit in result string
    main_page=None # integer with the number of the page that should receive the most attention, or "None" to distribute attention equally (only for pdf, word and powerpoint files)
) # function call that will return the summary of file
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You can use the "getFileType" function to obtain the type of a file through its address. Any file of any type can be recognized.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
file_type = perpetual_context.getFileType(file_path='./files/file_name.xlsx') # returns the type of file extension assigned to the string in "file_path"
print('The file is of type: '+file_type+'.') # displays the file type
```
```bash
The file is of type: xlsx.
```
You can use the "countTokens" function to count the tokens in a string.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
string = 'This is example text for counting tokens in a string.' # example text for tokens count
number_of_tokens = perpetual_context.countTokens(string=string) # returns the number of tokens contained in the "string" parameter text
print(f'The "{string}" text has {number_of_tokens} tokens.') # displays the number of tokens
```
```bash
The "This is example text for counting tokens in a string." text has 11 tokens.
```
You can use the "getKeyWords" function to obtain a list of keywords contained in a string.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
string = 'Brazil was discovered in 1500.' # Example text for keywords recognition
keywords_list = perpetual_context.getKeyWords(string=string) # returns the keywords contained in the "string" parameter text (the return will always be a list of strings)
print(f'The keywords contained in the text "{string}" are:', ', '.join(keywords_list)+'.') # displays the keywords
```
```bash
The keywords contained in the text "Brazil was discovered in 1500." are: brazil, discovered, 1500.
```
You can use the "getBeginningAndEnd" function to return only the beginning and end of a text based on the tokens limit.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# opens the file addressed in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "string" which will be passed to the parameter of the same name in the text summary function
with open('./files/file_name.txt', 'r', encoding='utf-8', errors='ignore') as file: string = file.read() # reading the string contained in the file
# code for generating summary of read content
# returns a summary with the start and end of the input string
summary_file = perpetual_context.getBeginningAndEnd(
    string=string, # string with the text that will be summarized
    max_tokens=1000, # maximum number of tokens returned in result text
    separator='' # string that will be between the beginning and end of the summary (use an empty string so that the two parts are completely joined together)
) # function call that will return the summary of the string
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You can also assign a separator text between the beginning and end of the return from the "getBeginningAndEnd" function.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# opens the file addressed in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "string" which will be passed to the parameter of the same name in the text summary function
with open('./files/file_name.txt', 'r', encoding='utf-8', errors='ignore') as file: string = file.read() # reading the string contained in the file
# code for generating summary of read content
# returns a summary with the start and end of the input string
summary_file = perpetual_context.getBeginningAndEnd(
    string=string, # string with the text that will be summarized
    max_tokens=1000, # maximum number of tokens returned in result text
    separator='\n...\n' # an ellipsis will be placed between the beginning and end of the summarized text
) # function call that will return the summary of the string
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
You can use the "getBeginningMiddleAndEnd" function to return only the beginning, middle and end of a text based on the tokens limit.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
# opens the file addressed in reading mode with "r", using the "utf-8" encoding and ignoring possible errors in the file; the read content will be assigned to the variable "string" which will be passed to the parameter of the same name in the text summary function
with open('./files/file_name.txt', 'r', encoding='utf-8', errors='ignore') as file: string = file.read() # reading the string contained in the file
# code for generating summary of read content
# returns a summary with the beginning, middle and end of the input string
summary_file = perpetual_context.getBeginningMiddleAndEnd(
    string=string, # string with the text that will be summarized
    max_tokens=1000, # maximum number of tokens returned in result text
    separator='\n...\n' # an ellipsis will be placed between the beginning and end of the summarized text (use an empty string so that the three parts are completely joined together)
) # function call that will return the summary of the string
# checking the text returned by the summary function
if len(summary_file.strip()) > 0: print('Summary generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the summary!') # if there is no text in the return, it displays the error message
# code to save a text file with the summary returned by the function
write = open('./summary_file.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "summary_file.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(summary_file) # writes the content of the "summary_file" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Summary generated successfully.
```
The "imageToBase64" function returns a dictionary with the base-64 string of an image in the "base64_string" key and the image type in the "image_type" key.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
file_path = './files/file_name.png' # variable to store the image address; this variable will be assigned to the parameter of the same name as the function
base64_of_the_image = perpetual_context.imageToBase64(file_path=file_path) # function call that will return the string with the base-64 encoding of the image (accepts any image file)
base64_of_the_image = base64_of_the_image['base64_string'] # the base64 string will be returned in a dictionary with the name key "base64_string"
# checking the text returned by the summary function
if len(base64_of_the_image.strip()) > 0: print('Base 64 generated successfully.') # if there is text in the return, it displays the success message
else: print('ERROR when generating the base-64!') # if there is no text in the return, it displays the error message
# code to save a text file with the base-64 returned by the function
write = open('./base64_of_the_image.txt', 'w', encoding='utf-8', errors='ignore') # opens a file in the local directory with the name "base64_of_the_image.txt" in writing mode with "w", in "utf-8" encoding and ignoring possible recording errors
write.write(base64_of_the_image) # writes the content of the "base64_of_the_image" variable to the file, if the file does not exist it will be created
write.close() # closes the file that was opened for writing, freeing it from memory
```
```bash
Base 64 generated successfully.
```
The "saveBase64Image" function converts a base-64 image string into an image file.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
file_path = './files/file_name.png' # variable to store the image address; this variable will be assigned to the parameter of the same name as the "imageToBase64" function
result_dictionary = perpetual_context.imageToBase64(file_path=file_path) # function that will return a dictionary with the base-64 string in the "base64_string" key and the type of the converted image in the "image_type" key (accepts any image file)
# code to generate the corresponding base-64 image file
result = perpetual_context.saveBase64Image( # call the function that will convert base-64 into a physical file; returns "True" if the file is generated without errors, or "False" if an error occurs
    base64_string=result_dictionary['base64_string'], # parameter that receives the base-64 string
    file_path='./', # parameter that receives the address of the directory where the file will be generated
    image_name='my_image', # parameter that receives the name of the image file that will be generated
    extension=result_dictionary['image_type'] # parameter that receives the type of image file that will be generated
) # the return will be "True" or "False" (if the image is saved successfully the return will be "True")
# checks if the file was generated successfully and without errors
if result: print('The image was generated successfully.') # if the return is "True", it displays the success message
else: print('ERROR when generating the image!') # if the return is "False", it displays the error message
```
```bash
The image was generated successfully.
```
The "saveImageFromPDF" function converts a page of a PDF file into an image.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
result = perpetual_context.saveImageFromPDF( # call of the function that will convert one of the pages of the pdf file into an image
    pdf_path='./files/file_name.pdf', # address of the pdf file that will have its page extracted as an image (only for pdf files)
    image_path='./', # parameter that receives the address of the directory where the file will be generated
    image_name='my_image', # parameter that receives the name of the image file that will be generated
    extension='png', # parameter that receives the type of image file that will be generated
    page_index=2 # index starting from zero referring to the position of the page that will be converted into an image
) # the return will be "True" or "False" (if the image is saved successfully the return will be "True")
# checks if the file was generated successfully and without errors
if result: print('The image was generated successfully.') # if the return is "True", it displays the success message
else: print('ERROR when generating the image!') # if the return is "False", it displays the error message
```
```bash
The image was generated successfully.
```
The "countPDFPages" function returns an integer with the number of pages in a PDF file.
```python
from perpetual_context import PerpetualContext # module import
perpetual_context = PerpetualContext() # main class object instantiation
file_path = './files/file_name.pdf' # variable for the address of the pdf file that will be assigned to the parameter of the same name
number_of_pages = perpetual_context.countPDFPages(file_path=file_path) # call of the function that returns the number of pages in the pdf file addressed in the "file_path" parameter (only for pdf files)
print(f'The PDF file "{file_path}" has {number_of_pages} pages.') # displays the number of pages in the read pdf file
```
```bash
The PDF file "./files/file_name.pdf" has 15 pages.
```
The "saveContext" function saves the current context as an index file in the directory of the referenced dialog.
```python
from perpetual_context import PerpetualContext # module main class import
perpetual_context = PerpetualContext() # main class object instantiation
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
# saves the current context of an input prompt with its corresponding response
# the input/prompt pair with output/answer will be saved as one of the dialog indexes
save_context = perpetual_context.saveContext( # only contexts previously saved by this function can be remembered by the model
    user_id=user_id, # assignment of identifier of the user who will have their dialogs saved
    dialog_id=dialog_id, # assigning identifier of current dialog with user input and output pairs
    prompt='Hello, who are you?', # user prompt; used to obtain a response from the language model
    answer="Hi, I'm Sapiens Chat." # response issued by the model to respond to the user's last prompt
) # the return will be "True" or "False" (if the context is saved successfully the return will be "True")
# checks if the context was saved successfully and without errors
if save_context: print('Context saved successfully.') # if the return is "True", it displays the success message
else: print('ERROR when saving the context!') # if the return is "False", it displays the error message
```
```bash
Context saved successfully.
```
The "deleteContext" function deletes all indexed inputs and outputs in the referenced dialog
```python
from perpetual_context import PerpetualContext # module main class import
perpetual_context = PerpetualContext() # main class object instantiation
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
# deletes all input and output pairs indexed in the dialog directory with the corresponding identifier
save_context = perpetual_context.deleteContext( # the deleted dialog will no longer be remembered when the corresponding context is consulted
    user_id=user_id, # assigning an identifier to the user whose dialogues were saved
    dialog_id=dialog_id # assigning identifier of the dialog to be deleted with user input and output pairs
) # the return will be "True" or "False" (if the context is successfully deleted the return will be "True")
# checks whether the context was deleted successfully and without errors
if save_context: print('Context deleted successfully.') # if the return is "True", it displays the success message
else: print('ERROR when deleting the context!') # if the return is "False", it displays the error message
```
```bash
Context deleted successfully.
```

## Methods
### Construtor: PerpetualContext

Parameters
| Name                | Description                                  | Type  | Default Value |
|---------------------|----------------------------------------------|-------|---------------|
| display_error_point | Enable or disable error details              | bool  | True          |

### getFileType (function return type: str): Returns the type of a file
Parameters
| Name          | Description                                         | Type | Default Value |
|---------------|-----------------------------------------------------|------|---------------|
| file_path     | Local path or a web address to any file             | str  | ''            |

### countTokens (function return type: int): Returns the number of tokens in a string
Parameters
| Name      | Description                                             | Type | Default Value |
|-----------|---------------------------------------------------------|------|---------------|
| string    | String with the text that will have the tokens counted  | str  | ''            |

### getKeyWords (function return type: list): Returns a list with the keywords from a string
Parameters
| Name   | Description                                                | Type | Default Value |
|--------|------------------------------------------------------------|------|---------------|
| string | String that will have the keywords extracted               | str  | ''            |

### getBeginningAndEnd (function return type: str): Returns the beginning and end of text in a string
Parameters
| Name       | Description                                            | Type | Default Value |
|------------|--------------------------------------------------------|------|---------------|
| string     | String with the text that will be summarized           | str  | ''            |
| max_tokens | Maximum number of tokens in result string              | int  | 1             |
| separator  | Separator between joined parts in the result string    | str  | ''            |

### getBeginningMiddleAndEnd (function return type: str): Returns the beginning, middle and end of text in a string
Parameters
| Name       | Description                                            | Type | Default Value |
|------------|--------------------------------------------------------|------|---------------|
| string     | String with the text that will be summarized           | str  | ''            |
| max_tokens | Maximum number of tokens in result string              | int  | 1             |
| separator  | Separator between joined parts in the result string    | str  | ''            |

### getSummaryCode (function return type: str): Returns the summary of a programming code
Parameters
| Name       | Description                                            | Type | Default Value |
|------------|--------------------------------------------------------|------|---------------|
| text       | Text with the code that will be summarized             | str  | ''            |
| max_tokens | Maximum number of tokens in result string              | int  | 1             |

### getSummaryText (function return type: str): Returns the summary of any text
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| text       | Text with the string that will be summarized          | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryTXT (function return type: str): Returns the summary of a TXT file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a TXT file                    | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### imageToBase64 (function return type: dict): Returns a dictionary with the base-64 of an image and the type of that same image
Parameters
| Name      | Description                                            | Type  | Default Value |
|-----------|--------------------------------------------------------|-------|---------------|
| file_path | Local or web address of a image file                   | str   | ''            |

### saveBase64Image (function return type: bool): Saves an image file in base-4
Parameters
| Name          | Description                                        | Type  | Default Value |
|---------------|----------------------------------------------------|-------|---------------|
| base64_string | Image base-64 string                               | str   | ''            |
| file_path     | Directory address where the file will be saved     | str   | ''            |
| image_name    | Name of the file to be saved                       | str   | ''            |
| extension     | Extension of the type of file to be saved          | str   | ''            |

### saveImageFromPDF (function return type: bool): Saves an image of a page from a PDF file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| pdf_path   | Local or web address of a PDF file                    | str   | ''            |
| image_path | Directory address where the file will be saved        | str   | ''            |
| image_name | Name of the file to be saved                          | str   | ''            |
| extension  | Extension of the type of file to be saved             | str   | ''            |
| page_index | Index of the page that will be converted into an image| int   | 0             |

### countPDFPages (function return type: int): Returns the number of pages in a PDF file
Parameters
| Name      | Description                                            | Type  | Default Value |
|-----------|--------------------------------------------------------|-------|---------------|
| file_path | Local or web address of a PDF file                     | str   | ''            |

### getSummaryYouTube (function return type: str): Returns the content summary of a YouTube video
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | YouTube video address                                 | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryWEBPage (function return type: str): Returns the summary of the content of a WEB page
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | WEB page address                                      | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryPDF (function return type: str): Returns the summary of the content of a PDF file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a PDF file                    | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |
| main_page  | Page number that will contain most of the summary     | int   | None          |

### getSummaryWord (function return type: str): Returns the summary of the content of a Microsoft Word file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a Microsoft Word file         | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |
| main_page  | Page number that will contain most of the summary     | int   | None          |

### getSummaryPowerPoint (function return type: str): Returns the summary of the contents of a Microsoft PowerPoint file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a Microsoft PowerPoint file   | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |
| main_page  | Page number that will contain most of the summary     | int   | None          |

### getSummaryCSV (function return type: str): Returns the summary of the content of a CSV file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a CSV file                    | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryExcel (function return type: str): Returns the summary of the content of a Microsoft Excel file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a Microsoft Excel file        | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryImage (function return type: str): Returns the summary of the content of a image file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a image file                  | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryAudio (function return type: str): Returns the summary of the content of a audio file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a audio file                  | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryVideo (function return type: str): Returns the summary of the content of a video file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a video file                  | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |

### getSummaryFile (function return type: str): Returns the summary of the contents of a file
Parameters
| Name       | Description                                           | Type  | Default Value |
|------------|-------------------------------------------------------|-------|---------------|
| file_path  | Local or web address of a file                        | str   | ''            |
| max_tokens | Maximum number of tokens in result string             | int   | 1             |
| main_page  | Page number that will contain most of the summary     | int   | None          |

### saveContext (function return type: bool): Saves current context to indexed files
Parameters
| Name      | Description                                            | Type  | Default Value |
|-----------|--------------------------------------------------------|-------|---------------|
| user_id   | User identifier                                        | int   | 0             |
| dialog_id | Dialog identifier                                      | int   | 0             |
| prompt    | User input prompt                                      | str   | ''            |
| answer    | Virtual assistant output response                      | str   | ''            |

### deleteContext (function return type: bool): Deletes the conversation context of a dialog belonging to a user
Parameters
| Name      | Description                                            | Type  | Default Value |
|-----------|--------------------------------------------------------|-------|---------------|
| user_id   | User identifier                                        | int   | 0             |
| dialog_id | Dialog identifier                                      | int   | 0             |

### getContext (function return type: str/list): Gets the full conversational context of a user's dialog
Parameters
| Name      | Description                                            | Type  | Default Value |
|-----------|--------------------------------------------------------|-------|---------------|
| user_id   | User identifier                                        | int   | 0             |
| dialog_id | Dialog identifier                                      | int   | 0             |
| config    | Setting for context return format                      | dict  | None          |

## getContext (function return type: list/str): Returns context based on semantic comparison algorithms
```python
from perpetual_context import PerpetualContext # module main class import
perpetual_context = PerpetualContext() # main class object instantiation
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
system = 'You are an Artificial Intelligence created by Sapiens Technology called Sapiens Chat.' # system prompt used to define how the language model should behave
prompt = 'Hello! Please tell me who you are.' # user prompt; used to obtain a response from the language model
# code to get the main context of the conversation from one of any user's dialogs
main_context = perpetual_context.getContext( # function call that will return the main context in the format "list" or "str" respecting the tokens limit established in the model settings
    user_id=user_id, # assignment of identifier of the user who will have their dialogs consulted
    dialog_id=dialog_id, # assignment of identifier of one of the dialogs with user input and output pairs
    config={'system': system, 'prompt': prompt, 'max_tokens': 4000} # assignment of the configuration dictionary that will define the context format
) # the "main_context" variable will store the return of the "getContext" function contained in the "perpetual_context" object
if len(main_context) > 0: # checks if there is content in the returned context
    write = open( # assigns to the "write" object the opening of a file for writing and recording
        './main_context.txt', # address, name and extension of the file that will receive the recorded content, if the file does not exist it will be generated
        'w', # "w" value so that the file is opened in writing mode
        encoding='utf-8', # assigns "utf-8" to the opening encoding to interpret any special accent characters
        errors='ignore' # the "ignore" value ignores possible errors when opening the file
    ) # the "write" variable receives the opened file
    write.write(str(main_context)) # writes the string corresponding to the returned context to the file
    write.close() # closes the file that was opened, freeing it from memory
    print('The main context of the dialogue was successfully achieved.') # displays a success message if everything goes correctly
else: print('ERROR getting main dialog context!') # displays an error message if context is not returned
```
```bash
The main context of the dialogue was successfully achieved.
```
```python
from perpetual_context import PerpetualContext # module main class import
perpetual_context = PerpetualContext( # main class object instantiation
    display_error_point=False # if "True", it enables the detailed display of possible errors, if "False" it disables the detailed display of possible errors
) # the "perpetual context" variable receives the value of the "PerpetualContext" class instantiation and becomes an object of that same class
# code for assigning values to main variables
user_id = 2 # identifier of the user the dialog belongs to
dialog_id = 1 # identifier of one of the user dialogs
system = 'You are an Artificial Intelligence created by Sapiens Technology called Sapiens Chat.' # system prompt used to define how the language model should behave
prompt = 'Hello! Please tell me who you are.' # user prompt; used to obtain a response from the language model
# data dictionary used as configuration for the context output format
config = { # with the exception of the key named "max_tokens", all other keys are dispensable
    'system': system, # system prompt assignment (optional value)
    'prompt': prompt, # user prompt assignment (optional value)
    'max_tokens': 4000, # assigning of maximum tokens limit in the context (optional value but highly recommended as the default is 1)
    ''''
        the supported format types in "return_format" are: "dictionaries_list" (ChatGPT API messages vector pattern with customizable keys and values),
        "chatgpt_pattern" (ChatGPT API messages vector pattern), "gemini_pattern" (Gemini API messages vector pattern),
        "claude_pattern" (Claude API input text pattern), "llama3_pattern" (Llama 3 input text pattern),
        "mistral_pattern" (Mistral input text pattern), "gemma_pattern" (Gemma input text pattern),
        "phi3_pattern" (Phi-3 input text pattern), "yi_pattern" (Yi input text pattern), "falcon_pattern" (Falcon input text pattern),
        "falcon2_pattern" (Falcon 2 input text pattern), "stablelm2_pattern" (Stable LM 2 input text pattern)
        or any string other than the previous ones for a standard return
    '''
    'return_format': 'dictionaries_list', # return context format; default value is "dictionaries_list" for a list of dictionaries similar to the one used by the OpenAI API
    'system_key': 'system', # name of the value used in the "role" key to specify the system prompt in the first dictionary of the return list (only used for the "dictionaries_list" pattern)
    'interlocutor_key': 'role', # name of the key used to define who owns the text content in the return list dictionaries (only used for the "dictionaries_list" pattern)
    'user_value': 'user', # value used in the "role" key or the key that replaces it; this value will specify that the dictionary text in the list belongs to the human user (only used for the "dictionaries_list" pattern)
    'assistant_value': 'assistant', # value used in the "role" key or the key that replaces it; this value will specify that the dictionary text in the list belongs to the virtual assistant issuing the responses (only used for the "dictionaries_list" pattern)
    'content_key': 'content', # name of the key used to define the text contents in the return list dictionaries (only used for the "dictionaries_list" pattern)
    'dialogue_indexes': [] # list of integers with the position indices of the input and output pairs that must appear in the returned context; if the list is empty, the input and output pairs returned will be those that best explain the user's current prompt
} # the keys "role" and "content" or their replacements in "interlocutor_key" and "content_key" will be in all dictionaries in the return list when the format returned is "dictionaries_list"
# code to get the main context of the conversation from one of any user's dialogs
main_context = perpetual_context.getContext( # function call that will return the main context in the format "list" or "str" respecting the tokens limit established in the model settings
    user_id=user_id, # assignment of identifier of the user who will have their dialogs consulted
    dialog_id=dialog_id, # assignment of identifier of one of the dialogs with user input and output pairs
    config=config # assignment of the configuration dictionary that will define the context format
) # the "main_context" variable will store the return of the "getContext" function contained in the "perpetual_context" object
if len(main_context) > 0: # checks if there is content in the returned context
    write = open( # assigns to the "write" object the opening of a file for writing and recording
        './main_context.txt', # address, name and extension of the file that will receive the recorded content, if the file does not exist it will be generated
        'w', # "w" value so that the file is opened in writing mode
        encoding='utf-8', # assigns "utf-8" to the opening encoding to interpret any special accent characters
        errors='ignore' # the "ignore" value ignores possible errors when opening the file
    ) # the "write" variable receives the opened file
    write.write(str(main_context)) # writes the string corresponding to the returned context to the file
    write.close() # closes the file that was opened, freeing it from memory
    print('The main context of the dialogue was successfully achieved.') # displays a success message if everything goes correctly
else: print('ERROR getting main dialog context!') # displays an error message if context is not returned
```
```bash
The main context of the dialogue was successfully achieved.
```

## Contributing

We do not accept contributions that may result in changing the original code.

Make sure you are using the appropriate version.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.
