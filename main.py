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
    lol = []  # initialize my list of lists
    while 0 < len(file_list):  # will continue to run until i pop all of my files
        dups = [file_list.pop(0)]  # initializing my list for adding duplicates
        for i in range(len(file_list) - 1, -1, -1):
            if compare(dups[0], file_list[i]):
                dups.append(file_list[i])
        if 1 < len(dups):
            lol.append(dups)  # adding my duplicates to the list of list

    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """

    lol = []
    # filter my file list to reduce the amount of times compare is called
    file_sizes = list(map(getsize, file_list))
    filtered_files = list(filter(lambda x: 1 < file_sizes.count(getsize(x)), file_list))

    while 1 < len(filtered_files):
        dups = [filtered_files.pop(0)]
        for i in range(len(filtered_files) - 1, -1, -1):
            if compare(filtered_files[i], dups[0]):
                dups.append(filtered_files[i])
        if 1 < len(dups):
            lol.extend([dups])
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
    m = max(lol, key=lambda x: len(x))
    print(f"File with the most duplicates: {m.pop(0)}")
    print(f"It has {len(m)} duplicates:")
    for d in m:
        print(d)

    # most disk space
    m = max(lol, key=lambda x: len(x) * getsize(x[0]))

    print(f"\nFile that takes the most disk space: {m.pop(0)}")
    print(f"It has {len(m)} duplicates:")
    for d in m:
        print(d)
    print(f"It and its duplicates take up {(len(m) + 1) * getsize(m[0])} disk space")

    return


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
