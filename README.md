# connectivity_checker
Ridiculously overengineered python script to check a bunch of connections.
I make this just to practise my -poor- python.


# Testing
Unit tests can be run with the following command from the project directory.

```
 python -m unittest discover
 ```
Tests classes are implemented under the tests directory of the project.

# Input file format

```json
{
"connectionSets": [
   {
        "localIP": "1.1.1.1",
        "localPort": 111,
        "protocol": "TCP",
        "remoteIPandPorts": [
            {   
                "IP": "2.2.2.2",
                "Port": 2222
            },
            {   
                "IP": "3.3.3.3",
                "Port": 3333
            }
        ]
        
   }
]
}
```

# TODO/Backlog
* Make the args get to the printing function to decide the print format of the results
* Make unit tests for -o option
* Improve unit tests
* Make ping option available

# Linkdump

Low level networking can be done with the sockets library

https://docs.python.org/2.7/library/socket.html

