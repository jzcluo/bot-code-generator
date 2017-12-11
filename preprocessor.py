"""
tasks:
    convert command for link to sending herocard
    check whether a waterfall has both card button and prompts. card button takes precedence
    combine anything if necessary such as herocards
    fixed order of operators
    readjust size of each block in each waterfall
"""
import re
def preprocess(file):
    preprocessed_file_name = file.split('.')[0] + "_preprocessed.txt"
    with open(file, "r") as src, open(preprocessed_file_name, "w") as dst:

        """
        first change all links to herocard with link attribute
        """
        for command in src.read().split(';')[:-1]:
            #get rid of newline character
            command = command.replace("\n", "").strip()
            if re.search('\S*', command).group() == "link":
                #replace link command with herocard command
                dst.write("herocard {links : [" + re.search("{.*}", command).group()[1:-1] + "]}\n")
            else:
                dst.write(command + ";\n")
