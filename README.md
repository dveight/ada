# Ada
Visual Effects pipelines require passing a lot of data around various applications, manipulating that data with nodes and creating outputs which are used in other applications. 

A templates creator can decide what values the artist needs to change or an application needs to set. This effectively turns a template into a function/node which takes inputs, attributes, and outputs.

Each application has its own sets of requirements of how they want to externalise parameters to users and how to implement the execution framework.

Ada consists of a few parts. 
* A template which create a graph containing information about the templates parameters.
 * *  This is usually created at publish time into an asset management system.
* The Ada cli takes an application argument and a template, the template should have an associated graph file which is used to dynamically build command line arguments for the user
* The arguments values are fed into an Ada context and serialised to a protobuf
* Each application implents a command line script to launch headless to read the template, the context file and then execute the nodes in the specific way that DCC determines.
* Rendering of the baked script should be implemented as part of your internal pipeline, Ada is aimed at creating executable templates which can (but not always) create renderable outputs.
* Graph files can be created after a template is executed to pass further information to other processes such as rendering

The cli provided is only one way to create Ada contexts. The core API is meant to work in each DCC and can be used in its own way to create and serialise data. A simple example of this would be passing values directly from a Houdini scene directly into a Nuke template and knowing the exact parameters you have to pass into the Nuke template.
 ## Foundry Nuke Example
 You have a project that has come in and half of it is shot on blue screens and the other half on green
 screens. You want to run an automatic despill process but you need the user to choose what colour the screen
 is. 
 
 ```ada nuke ~/jobs/INV/001_ab/publish/nk/ada/F_MultiAliasInput.nk --script-dir ~/jobs/INV/001_ab/001_ab_0010/nuke/comp --script-name comp --kitten 1 --robot-grade 1.0 --input-scan /path/to/scan --input-camera /camera/path``` 
 
 Each argument after --script-name is dynamically created by the cli and driven by the creator of the template.

 ## Gaffer Example
 
    TODO
    
 ## Houdini Example

 ## Katana Example

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
    
    ```sudo cp six-1.12.0-py2.7.egg /Applications/Nuke11.3v1/Nuke11.3v1.app/Contents/MacOS/pythonextensions/site-packages/```

# Build Gaffer Protobuf with ucs4 for Mac OS X

Gaffer on Mac is built against python with ucs4 unicode bindings, this means that the `pip` or `homebrew` installed `google.protcolbuf` isn't compatible with Gaffer on the Mac. The easiest way to get a working install is to compile python with ucs4 enabled and then recompile protobuf's c++ implementation.

## compiling python ucs4

download python from https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz

```bash
# extract python 2.7.8 to /tmp/python
> cd /tmp/python-2.7.8
> ./Python-2.7.8/configure --enable-unicode=ucs4 --prefix=/tmp/python MACOSX_DEPLOYMENT_TARGET=10.13
> make
> make install
```

## compiling google.protobuf with ucs4

download protobuf from https://github.com/protocolbuffers/protobuf/archive/v3.7.1.zip

```bash
# extract google.protobuf to /tmp/protobuf-3.*.*
> cd /tmp/protobuf-3.*.*/python
> /tmp/python/bin/python setup.py build --cpp_implementation
> cp -rf build/lib.macosx-10.13-x86_64-2.7/google /Applications/gaffer-0.53.4.0-osx/python/
```

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

## per application executables

You can specify the executable path one of two ways:

### executable path declaration


- via cmake using a build time variable
```
-DNUKE_EXECUTABLE=/Applications/Nuke11.2v5/Nuke11.2v5.app/Contents/MacOS/Nuke11.2v5
-DGAFFER_EXECUTABLE=/Applications/gaffer-0.53.4.0-osx/bin/gaffer
```

- via and environment variable

```
export ADA_NUKE_EXECUTABLE=/Applications/Nuke11.2v5/Nuke11.2v5.app/Contents/MacOS/Nuke11.2v5
export ADA_GAFFER_EXECUTABLE=/Applications/gaffer-0.53.4.0-osx/bin/gaffer
```

# Testing

Testing is done using nosetest, unittest2 and cmake, so make sure the trifecta of unit testing is installed and ready to be used. Simple run `make install` then one of the following test commands:

```make test```

or with more verbosity and vigor

```make check```

### with Nuke

You will need to specify the path to the nuke executable when you run cmake in order to run all of the tests using the internal nuke python interpreter, to do this simply add the NUKE_EXECUTABLE flag onto your cmake command or environment.


### with Gaffer

Like Nuke testing, you will have to include the Gaffer executable path when you run your cmake command, to this simply add the GAFFER_EXECUTABLE flag to your cmake build or environment.

Done! 
