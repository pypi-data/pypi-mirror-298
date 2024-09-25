# __main__.py
# Author: DaYuan Tan, dr.dayuantan at gmail dot com
# Last Modified: 2024-09-25
# This file is used to make the package executable as a script. When you run the package using python -m pdfgpt, the code in __main__.py will be executed.

"""Extract PDF contents with the magic of GPT.

-------------
Usage in CLI:
-------------

    $ pdfgpt [options]

Available options are:

    -h, --help         Show this help


------------------
Usage in Python:
------------------

    import pdfgpt
    pdfgpt.PDFGPT(openai_api_key)
    
    Check more in https://github.com/DayuanTan/pdfgptlib.


--------
Contact:
--------

- https://github.com/DayuanTan/pdfgptlib
- Author: DaYuan Tan, dr.dayuantan at gmail dot com

More information is available at:

- https://github.com/DayuanTan/pdfgptlib


--------
Version:
--------

- pdfgpt v0.1.0
"""
import sys


def main() -> None:
    """Extract contents from PDF files."""
    opts = [o for o in sys.argv[1:] if o.startswith("-")]
    
    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        raise SystemExit()
    else:
        print("Hello from pdfgpt!")
        print("Use -h or --help to see the help message.")
    

if __name__ == "__main__":
    main()