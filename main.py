"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Andrew Francis"
__email__ = "franca17@my.erau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare


def search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Basic search strategy goes like this:
    - until the provided list is empty.
    - remove the 1st item from the provided file_list
    - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
    - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
    As a result we have a list, each item of that list is a list,
    each of those lists contains files that have the same content
    """
    lol = []
    while 0 < len(file_list):
        dups = [x for x in file_list if compare(file_list[0], x)]
        if 1 < len(dups):
            lol.append(dups)
        file_list = [x for x in file_list if not compare(file_list[0], x)]
    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    # sort these by size and then run an if statement to compare them only if they are the same size
    lol = []
    while 0 < len(file_list):
        dups = [file_list.pop(0)]
        for i in range(len(file_list) - 1, -1, -1):
            if compare(dups[0], file_list[i]):
                dups.append(file_list[i])
        if 1 < len(dups):
            lol.append(dups)

    return lol


def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    print("== == Duplicate File Finder Report == ==")
    # most dups

    print(f"Max: {max(lol, key=lambda x: len(x) * len(x[0]))}"
          f"\nMax Duplicates: {max(lol, key=lambda x: len(x))} ")
    return

    #
    # else:
    #     print("No duplicates found")


print(search(all_files("images")))

print(faster_search(all_files("images")))


if __name__ == '__main__':
    path = join(".", "images")

    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now w/ a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
