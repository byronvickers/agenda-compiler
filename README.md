# agenda-compiler
A tool to label all attachments for an agenda and compile them together into a single master PDF document.

## Getting started on Windows for new users
### Downloading this tool
If you're not familiar with git, then you can download this package as a zipfile. Click the 'Clone or download' button next to the file list above, and download everything as a zip. Make sure to extract everything from this zip file before proceeding. Pay attention to where you have extracted the contents to, as you will need to navigate to that location later in order to run the tool with Python.

### Python
Make sure you have [Python 3](https://www.python.org/downloads/) installed. You don't need to be an admin user on your computer to do this, just de-select the "install for all users" option in the installation dialogue. I strongly recommend also selecting the "Add Python 3.X to PATH" option, if this is your first time with Python.

Once you have installed Python, open Powershell (open the windows menu and type ``powershell`` into the search bar), type ``python --version`` at the prompt, and hit enter. You should see a line telling you which version of Python you've just installed. If this gives an error, you'll need to resolve this before going further.

Note that you can open an interactive Python session by running ``python``, or execute a python script ("example.py") by running ``python example.py``.

### Navigation in Powershell
To get around in Powershell, use ``cd`` to change directory and ``dir`` to see the contents of your current directory. You can usually copy-and-paste a location from Windows Explorer (click in the location bar and you should see the path, or right click -> Properties should also work).

For example, if your agenda documents are under ``G:\\MyCollege Admin\Committees\MyCommittee\Agenda Files``, then ``cd "G:\\MyCollege Admin\Committees\MyCommittee\Agenda Files"`` will get you to the right spot. The surrounding quotes are necessary if your path has any spaces in it, here.

### Installing dependencies
The agenda compiler tool needs a few Python packages installed. Python has a handy package manager to help you install these. Get to the directory where you've put the agenda compiler and run
``pip install -r requirements.txt``
to install all the required packages. If you get an error message about ``pip`` not being found, try
``python -m pip install -r requirements.txt``
instead.

You're now ready to compile your agenda!

## Running the agenda compiler
The agenda compiler needs two things: the location of the agenda PDF file, and the location of the folder containing the attachments.

You can supply these as command line arguments or interactively.

To pass these locations as command line arguments, use the syntax
``python agenda_compiler.py "<path to agenda pdf>" "<path to folder containing attachments>"``
To pass the locations interactively, simply run 
``python agenda_compiler.py``
and follow the prompts. Note that you do *not* need to surround paths in quotes when entering them interactively.

The tool will give feedback on progress through the compilation process, and will output a file called ``agenda-compiled.pdf`` once the compilation is complete. The file will also have bookmarks added pointing to the agenda and each of the attachment files within the compiled PDF document.

## Attachment naming
The agenda compiler will attach your attachments in alphabetical order. Note that, for example, ``ATT10_Example filename.pdf`` comes _before_ ``ATT2_Example filename.pdf`` in an alphabetical ordering. I suggest naming files as, e.g.:
```
ATT010_First attachment.pdf
ATT020_Second attachment.pdf
ATT030_And another one.pdf
...
ATT090_More filenames.pdf
ATT100_Here's a tenth one.pdf
ATT110_And wrap it up.pdf
```
That is:
 1. Put a leading zero on your single-digit numberings so that ``02`` comes before ``10``, and
 2. Put a trailing zero (i.e. count by tens) so that if a last-minute new file comes in, you can slip it between the existing files (e.g. ``ATT035_Last minute file to go fourth.pdf``). The agenda compiler will automatically increment the numbering for the subsequent attachments in the output PDF file.

The exact names of the PDF files do not matter; the agenda compilation tool only uses these names for ordering the attachments.

## Issues and feedback
Feedback of all sorts is very welcome. If the tool isn't working for you, or you have ideas for useful features, file an issue on the GitHub page.

Pull requests are also very welcome, if you want to make some changes directly!
