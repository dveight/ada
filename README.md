# Ada
Ada is a framework for creating executable scripts. Visual Effects pipelines require passing data
around various applications, manipulating that input data with nodes and creating outputs which are
used in other applications. Ada allows you to write an application specific execution framework that
uses context data to manipulate the inputs. Users are able to setup a script, publish it then run a cli or gui which gives them
options for inputs, output, and any other options they might need to choose before executing the
script. 

 ## Nuke Example
 You have a project that has come in and half of it is shot on blue screens and the other half on green
 screens. You want to run an automatic despill process but you need the user to choose what colour the screen
 is. 
 
 ```ada nuke ~/jobs/INV/001_ab/publish/nk/ada/F_MultiAliasInput.nk --script-dir ~/jobs/INV/001_ab/001_ab_0010/nuke/comp --script-name test --kitten 1 --patrick 1000 --input input1 --input input2 --input input3``` 

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
              
Done! 