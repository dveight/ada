# Ada
Ada is a framework for creating executable scripts. Visual Effects pipelines require passing alot of dataaround various applications, manipulating that data with nodes and creating outputs which are used in other applications. Ada allows you to write an application specific execution framework that
passes an input context (protobuf) into a DCC along with a template scripts containing nodes with executable instructions on it (in Nuke this takes the form of a Ada tab on each node). 
Users are able to setup a script, publish it (which saves out information about the execution order of the node graph) and run a cli or gui (todo) which gives them options for inputs, outputs, and any other attributes the creator decided to expose for manipulation. An Ada template becomes a node with inputs, outputs and attributes which is then executed.

 ## Nuke Example
 You have a project that has come in and half of it is shot on blue screens and the other half on green
 screens. You want to run an automatic despill process but you need the user to choose what colour the screen
 is. 
 
 ```ada nuke ~/jobs/INV/001_ab/publish/nk/ada/F_MultiAliasInput.nk --script-dir ~/jobs/INV/001_ab/001_ab_0010/nuke/comp --script-name comp --kitten 1 --robot-grade 1.0 --input-scan /path/to/scan --input-camera /camera/path``` 

 ## Houdini Example

 ## Katana Example

 ## Gaffer Example

# Patch Nuke Protobuf
Nuke uses protobuf 2.5.0 which does not support structs. In order to use Ada in Nuke you will have
to patch the sitepackages that comes with Nuke. 

1) Download the latest version of Protobuf using pip

    ```pip install protobuf```
    
2) Download the latest version of 'six'

    ```pip install six``` 

3) Remove or back up protobuf-2.5.0-py2.6.egg in your install path for Nuke:
    
    ```sudo mv /Applications/Nuke11.3v1/Nuke11.3v1.app/Contents/MacOS/pythonextensions/site-packages/protobuf-2.5.0-py2.6.egg /Applications/Nuke11.3v1/Nuke11.3v1.app/Contents/MacOS/pythonextensions/site-packages/protobuf-2.5.0-py2.6.egg.bak```

4) install protobuf 2.6.0 or higher to:
    
    ```/Applications/Nuke11.3v1/Nuke11.3v1.app/Contents/MacOS/pythonextensions/site-packages/```
   
    along with its 
    
    ```protobuf-3.7.1-py2.7-nspkg.pth```
    
5) install Six 1.9.0:
    
    
    sudo cp six-1.12.0-py2.7.egg /Applications/Nuke11.3v1/Nuke11.3v1.app/Contents/MacOS/pythonextensions/site-packages/

# Building

You will need CMake 3.13 or higher in order to build the proto buffer files and install the scripts and python files into the specified location. A recommended location for the install is to a local directory called `packages` which can then easily be added to the `PATH` and `PYTHONPATH`.

update your .profile or equivalent with the following:
```
export PATH=/Users/$USER/packages/bin:$PATH
export PYTHONPATH=/Users/$USER/packages/lib/python:$PYTHONPATH
```

From a separate build directory, eg. `~builds/ada/`, you can run the following cmake command to build the project.

`cmake -DCMAKE_INSTALL_PREFIX=~/packages/ ~/dev/nuke/ada/`

Then to finally build the proto files and install it, simply run

```make install```

# Testing

Testing is all done using nosetest, unittest2 and cmake, so make sure the trifecta of unit testing is installed.

```make test```

or with more verbosity and vigor

```make check```

### with Nuke

You will need to specify the path to the nuke executable when you run cmake in order to run all of the tests using the internal nuke python interpreter, to do this simply add the NUKE_EXECUTABLE flag onto your cmake command.

```-DNUKE_EXECUTABLE=/Applications/Nuke11.2v5/Nuke11.2v5.app/Contents/MacOS/Nuke11.2v5``` 

Done! 
