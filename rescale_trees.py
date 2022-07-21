from ete3 import Tree
import sys

def input_with_default(text, default):
    """
    Ask a question until either a float value is provided or
    a blank field is entered. Return either the entered float 
    or the specified default.

    Parameters:
      text (str): Prompt for the user to answer
      default (float): Default value if nothing is entered.
        Will be appended to the prompt in brackets.

    Returns:
      val (float): Either the user-specified number or the default value
    """
    question = text + " [" + str(default) + "]: "
    response = input(question)
    val = default
    if response == '':
        return val
    else:
        try:
            val = float(response)
        except ValueError:
            input_with_default(text, default)
    return val

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
    # We don't wanna change the original list unexpectedly
    scaled_trees = tree_list.copy()
    for tree in scaled_trees:
        for node in tree.traverse():
            node.dist *= scale # TODO does this just work?
    return scaled_trees

def output_to_file(tree_list, outfile):
    """
    Write the Newick string representation of each tree in
    the list to a file. 

    THE FILE WILL BE OVERWRITTEN.

    Parameters:
      tree_list (list): List containing one or more ete3 Tree objects
      outfile (str): Relative path to the output file.

    Returns:
      nothing
    """
    lines_out = [tree.write(format=1) + '\n' for tree in tree_list]
    with open(outfile, 'w') as treefile:
        treefile.writelines(lines_out)

def main():
    """
    Ask the user about the scaling of the existing tree(s) in a file
    and make the necessary calls to transform it to generations.
    """
    # Check that a file exists and we can try to read it
    try:
        with open(sys.argv[1]) as treefile:
            nwk_list = treefile.readlines()
    except IndexError:
        print('No input file name was provided. Please provide the relative path\nof a file containing one or more trees in Newick format.')
        return 1
    except FileNotFoundError:
        print('An input was provided, but no file was found with that name.\nPlease check that you have spelled the name correctly and that the file is readable.')
        return 1

    # Try to read the file and make it into trees
    tree_list = []
    for nwk in nwk_list:
        try:
            tree_list.append(Tree(nwk))
        except Exception as e:
            if type(e).__name__ == 'NewickError':
                print(f'The file cannot be converted into a tree. Expected newick formatted text, got \"{nwk[:-1]}\"')
                return 1
            else:
                raise Exception(e)

    # Ask for scaling factors about the input tree
    days_per_timeunit = input_with_default('On the input tree(s), how many days are there per time unit?', 365.0)
    days_per_generation = input_with_default('How many days are there in a generation?', 1.5)

    # Scale each tree in the file
    scale = days_per_timeunit / days_per_generation
    scaled_trees = scale_trees(tree_list, scale)

    # Make a new file name and output to that file
    name, extension = sys.argv[1].split('.') # TODO I could handle this better but it may be okay
    outname = name + "_scaled." + extension
    output_to_file(scaled_trees, outname)

if __name__ == '__main__':
    main()
