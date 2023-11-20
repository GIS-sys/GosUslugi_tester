# Installation

1) clone this repository

2) install geckodriver:

a) download firefox geckodriver: https://github.com/mozilla/geckodriver/releases

b) unpack it in some system folder (for example C:/Program Files/ on Windows, /usr/bin/ on Linux)

c) put it's location into config.py, like this:

```GECKODRIVER_PATH = "/usr/bin/geckodriver"```


# Usage

1) change config.py if needed

2) add / change scene in ```scenes/``` folder if needed

3) run ```python main.py``` to execute script

4) when asked, input scene file names. For example, you can start by trying:
```618022_add_changes.scn 618022_convert.scn```

