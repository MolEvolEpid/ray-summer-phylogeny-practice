from ete3 import Tree
import sys

######################################
### Parameters that need to be set ###
######################################

# The number of days in each unit of time on the input trees (default 365)
time_unit_days = 365

# The number of days a generation takes (default 1.5)
generation_days = 1.5

# Whether or not to override the original files (default False)
# If set to False, will create a copy and append "_rescaled" to the name.
overwrite_original_files = True

###############################################################################

def scale_trees(tree_list, scale):
    """
    Scale every tree in a list by the same scaling factor
    and return the new list.

    Parameters:
      tree_list (list): List containing one or more ete3 Tree objects
      scale (float): Scaling factor to change trees by

    Returns:
      scaled_trees (list): New list containing the scaled Tree objects.
    """
    # We don't want to change the original list unexpectedly
    scaled_trees = tree_list.copy()
    for tree in scaled_trees:
        for node in tree.traverse():
            node.dist *= scale
    return scaled_trees

def output_to_file(lines_out, outfile):
    """
    Write the Newick string representation of each tree in
    the list to a file.

    ANY DATA IN THE FILE WILL BE OVERWRITTEN

    Parameters:
      tree_list (list): List containing one or more ete3 Tree objects
      outfile (str): Relative path to the output file.

    Returns:
      nothing
    """
    with open(outfile, 'w') as treefile:
        treefile.writelines(lines_out)
    print(f"Successfully written to {outfile}.")

def parse_trees(lines):
    """
    Provided a list of lines from any file, determine
    if any trees are in the file and scale them.

    Parameters:
      lines (list): List of line strings, read from a file

    Returns:
      lines (list): List of line strings, but with trees scaled.
    """
    try:
        trees = [Tree(l) for l in lines]
        rest = []
    except Exception as e:
        if type(e).__name__ == "NewickError":
            trees = [Tree(lines[0])]
            rest = lines[1:]
        else:
            raise Exception(e)
    scale = time_unit_days / generation_days
    trees_scaled = scale_trees(trees, scale)
    tree_strings = [t.write(format=1) + '\n' for t in trees_scaled]
    return tree_strings + rest

def main():
    """
    For each file provided as a command line argument, attempt to process it
    and scale it up as specified at the top of the file.
    """
    # Check that a file exists and we can try to read it
    if sys.argv[1:] == []:
        print('No input file name was provided. Please provide the relative path\nto a file containing one or more trees in Newick format.')
        return 1
    try:
        for arg in sys.argv[1:]:
            print(f'Processing {arg}...')
            with open(arg) as f:
                lines = f.readlines()
                first_tree = Tree(lines[0]) # Attempt to convert the first line, catch the error it may throw
                lines_out = parse_trees(lines)
                name, ext = arg.split('.')
                if overwrite_original_files:
                    name_out = name + "." + ext
                else:
                    name_out = name + "_rescaled." + ext
                output_to_file(lines_out, name_out)
        return 0
    except Exception as e:
        if type(e).__name__ == "FileNotFoundError":
            print('An input was provided, but no file was found with that name.\nPlease check that you have spelled the name correctly and that the file is readable.')
            return 1
        elif type(e).__name__ == "NewickError":
            print('The file does not seem to contain tree data. Please ensure\nthat the first line in the file is a tree.')
            return 1
        else:
            raise Exception(e)

if __name__ == '__main__':
    main()
