# specific_import

## This package allows you to import resources by their relative or absolute file paths.<br><br>

## Features
  * Is open source
  * Is compatible with the latest version of Python3
  * Is great at doing imports relative to the file doing the actual importing
    * (as opposed to relative to the file doing the calling as other import libraries do.)
  * Doesn't reload module if module already loaded
  
## How to install
* Method 1: Use PIP
```
pip install specific_import
```

* Method 2: 
Download from Github<br><br>  
  
  
 ## Example
```python
from specific_import import import_file

# import relatively
app_setup = import_file('../app_setup.py')

# import absolutely
app_setup = import_file('/home/projects/my_project/app_setup.py')

```

 ## Why?
 I love Python but sometimes the builtin import system can be a headache
