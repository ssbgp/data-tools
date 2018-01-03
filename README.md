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

The `basic-data` tool computes various statistical metrics for multiple sets of data. A *dataset* corresponds to a directory containing multiple data files (`.basic.csv`) output from the simulator. A data file is called a *data unit*. Each data unit contains multiple data samples, obtained from multiple simulations with the same inputs, but different seeds for generating the message delays. 

###### Inputs

The tool takes a configuration file specifying the datasets to compute metrics for. The configuration file is a JSON formatted file containing a single object. Each key/value pair on this object specifies one dataset, where the value is the path to the directory containing the data files, and the key is a label to identify that dataset. Here is an example of a configuration file specifying two different datasets,
    
    {
        "BGP - Peer+ 0.25%": "/path/to/bgp/peer+/0.25%",
        "SS-BGP - Siblings": "/path/to/ss-bgp/siblings"
    }

###### Outputs

For each dataset specified in the configuration file, the tool computes all of the following metrics. 

- Number of non-terminated data units (destinations)
    
    *A data unit (destination) is considered to have not terminated if it contains at least one sample that did not terminate.*
    
- Average of the termination times over all samples of each data unit in the dataset, excluding samples that did not terminate.

    *The termination time of one sample corresponds to time at which there were no more routing events to be processed.* 

- Average of the number of messages over all samples of each data unit in the dataset, excluding samples that did not terminate.

- Average of the number of deactivations over all samples of each data unit in the dataset, excluding samples that did not terminate.

The actual output is a CSV file containing a table with a row for each dataset and a column for each output metric. Here is an example of the corresponding table for the two datasets included in the example of a configuration file shown before.

|      Dataset      	| Data Unit Count 	| Non-Terminated Count 	| Termination Time (Avg.) 	| Messages (Avg.) 	| Deactivations (Avg.) 	|
|:-----------------:	|:---------------:	|:--------------------:	|:-----------------------:	|:---------------:	|:--------------------:	|
| BGP - Peer+ 0.25% 	|       200       	|          25          	|         34000.0         	|     400000.0    	|          0.0         	|
| SS-BGP - Siblings 	|       200       	|           0          	|         24000.0         	|     200000.0    	|          1.0         	|

#### Usage

Here we consider an usage example to illustrate how to use the tool. Assume we performed simulations with BGP and SS-BGP under the *siblings* annotated topology. We want to compute our statistical metrics for each protocol independently, which means each protocol requires its own dataset. To accomplish this, 

1. Store the data corresponding to each protocol in its own directory, as shown below.

    - data/
        - BGP/
        - SS-BGP/
        
    Data from BGP is stored in `data/BGP/`, and data from SS-BGP is store in `data/SS-BGP/`.

1. Create the configuration file, called `conf.json`.


    {
        "BGP - Siblings": "data/BGP",
        "SS-BGP - Siblings": "data/SS-BGP"
    }
    
1. Run the tool.


    basic-data conf.json
    

This will output a CSV file called `basic-data.csv`.

Finally, the most important command of any tool is the one that helps you. Use the option `-h/--help` to have the tool print an help message showing its usage pattern and all options with their corresponding descriptions.

    basic-data --help 


## Tool: plot-times

Finally, the most important command of any tool is the one that helps you. Use the option `-h/--help` to have the tool print an help message showing its usage pattern and all options with their corresponding descriptions.

    plot-times --help 


