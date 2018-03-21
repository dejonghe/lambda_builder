#!/usr/bin/env python

import argparse
import lambda_builder.logger
from lambda_builder.builder import LambdaBuilder

__version__ = '0.0.0'

def main():
    """Main entry point for lambda_build cli."""
    # Setup parser and arguments
    parser = argparse.ArgumentParser(description='Schedule batch jobs')
    parser.add_argument("path", help="Path to source directory.",default=None)
    parser.add_argument("output", help="Desired output file.",default=None)
    args = parser.parse_args()

    # Setup builder and run
    builder = LambdaBuilder(src=args.path,dest=args.output)
    builder.run()

if __name__ == '__main__':
    try: main()
    except: raise
