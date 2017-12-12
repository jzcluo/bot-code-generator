"""
tasks:
    convert command for link to sending herocard
    check whether a waterfall has both card button and prompts. card button takes precedence
    combine anything if necessary such as herocards
    re-adjust size of each block in each waterfall
"""
import re
from my_lib import get_list_of_dicts

def preprocess(file):
    preprocessed_file_name = file.split('.')[0] + "_preprocessed.txt"
    with open(file, "r") as src, open(preprocessed_file_name, "w+") as dst:

        """
        - change all links to herocard with link attribute
        - get rid of newline characters in the middle of the text
        """
        for command in src.read().split(';')[:-1]:
            #get rid of newline character
            command = command.replace("\n", "").strip()
            if re.search('\S*', command).group() == "link":
                #replace link command with herocard command
                dst.write("herocard {links : [" + re.search("{.*}", command).group()[1:-1] + "]};\n")
            else:
                dst.write(command + ";\n")

        """
        - insert necessary propmt comfirmation
        - put entityconditional after next
        - parse choiceprompt and put its decisions in next waterfall step
        """
        #place read pointer at the start of the file again
        dst.seek(0)
        dst_contents = dst.readlines()
        dst.seek(0)
        dst.truncate()

        #two variables that will be used in the loop
        #they are the things that should be inserted before or after a next command
        insert_before = ""
        insert_after = ""

        for line in dst_contents:
            if "herocard" in line:
                dst.write(line)

                herocards = get_list_of_dicts(re.search("{.*}", line).group())
                #if there is a button in the herocard then there should be conditional block after next
                if any("buttons" in herocard for herocard in herocards):
                    #define insert_after
                    pass
            elif line.strip().strip(';') == "next":
                if insert_before:
                    #if insert_before has a value
                    dst.write(insert_before)
                else:
                    #if there is not a insert_before
                    #put in a choiceprompt that waits for user interaction
                    dst.write("choiceprompt {text : , choices:[Next Step]};\n")
                    insert_after = ""

                dst.write(insert_before)
                dst.write("next;\n")
                dst.write(insert_after)

                insert_before = ""
                insert_after = ""

            else:
                dst.write(line)




preprocess("installation_matlab_mac.txt")
