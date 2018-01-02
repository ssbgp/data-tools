# SS-BGP Data Tools

This repository includes a set of tools to process data obtained from the routing [simulator](https://github.com/ssbgp/simulator). These tools were developed to process data from simulation we conducted during our research. They were conceived to meet out own requirements. For this reason, they may not be very useful for most people.

## Tool summary

Here is the list of tools included in this repository.

- basic-data
- plot-times

## Installation

All tools require the python interpreter version 3.6 or later. The next section shows how the python interpreter can be installed in different platforms. If you are sure your system already includes the correct version of python installed, please move to [Install Tools](#install-tools).

### Install Python Interpreter (and pip)

The way python is installed greatly depends on your platform.

###### Windows/MacOS

1. Go to Python's download page https://www.python.org/downloads/
1. Press the *'Download'* for the latest version of python 3. At the time of writing that is version 3.6.4. This will direct you to the download page for that release.
1. Scroll all the way down. There should be a table called *Files* including multiple installers. Download the installer for your OS and architecture. 
1. The last step is to run the installer and follow each step.

**IMPORTANT:** make sure **`pip`** is installed.

###### Linux

Most linux distributions come with python 3 pre-installed. Thus, the first step is to check which version is installed. Enter the following command in a terminal.

    python3 -V

If the installed is earlier than 3.6, then you have to install a later version. The best way to install a new python version may differ from distribution to distribution. Our suggestion is to search for the best way to install python 3.6 (or later) on your distribution and install it that way. 

After making sure python 3.6 (or later) is installed, you have to make sure `pip` is installed. Most linux distribution include `pip` in their main repositories. To install `pip` follow the indications included in this [guide](https://packaging.python.org/guides/installing-using-linux-tools/) for your linux distribution.


### Install Tools

1. Make sure both python 3.6 (or later) and `pip` correctly installed.
    
        python -V
        python -m pip -V
    
1. Clone the project from this repository.

        git clone https://github.com/ssbgp/data-tools.git
        
1. Move to project directory.

        cd data-tools
        
1. Install tools.

        python -m pip install .
        python -m pip install -r requirements.txt
        
   **Warning:** for some distributions you mut use `python3` instead of `python` to use python 3.

1. Check if tools were correctly installed.

        basic-data -h
        plot-times -h
        
   Each of these commands will fail if the tools are not installed correctly. Otherwise, they will show a help message for each tool.

## Tool: basic-data

The most important command of any tool is the one that helps you. Execute the tool with option `-h/--help`.

    basic-data --help
    
This command prints an help message showing the tool's usage pattern and a description for each option.  


## Tool: plot-times

The most important command of any tool is the one that helps you. Execute the tool with option `-h/--help`.

    plot-times --help
    
This command prints an help message showing the tool's usage pattern and a description for each option.


