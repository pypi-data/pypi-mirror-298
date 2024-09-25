import os
import argparse
from codenamize import codenamize
from friendly_hash.version import __version__

def get_friendly_hash(filename):
    """Generate a human-readable hash for the given filename."""
    return codenamize(filename)

def rename_file(filename, friendly_hash):
    """Rename the file with the human-readable hash."""
    new_filename = f"{friendly_hash}-{filename}"
    os.rename(filename, new_filename)
    return new_filename

def main():
    parser = argparse.ArgumentParser(
        description="Rename files with human-readable hashes.",
        epilog="Example usage:\n"
               "  friendly_hash -f 2024-07-05-09-15-18.bag\n"
               "  friendly_hash 2024-07-05-09-15-18.bag",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'filename',
        help='The name of the file to hash',
        nargs='?'  # This makes the filename argument optional for version check
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Actually rename the file'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='Show the version number and exit'
    )
    
    args = parser.parse_args()
    
    if args.filename:
        friendly_hash = get_friendly_hash(args.filename)
        new_filename = f"{friendly_hash}-{args.filename}"
        
        if args.force:
            new_filename = rename_file(args.filename, friendly_hash)
            print(f"File renamed to {new_filename}")
        else:
            print(new_filename)

if __name__ == "__main__":
    main()
