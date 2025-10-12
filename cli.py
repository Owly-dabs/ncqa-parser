#!/usr/bin/env python3
 
import fire
import main as parse
from mylib import io_utils as io

if __name__ == "__main__":
    fire.Fire({
        "parse": parse,
        "io" : io,
    })