# Microsoft Bot Dialog Code Generator

Given a txt file with instructions, this code generates code that can be as waterfall steps to guide the user through an installation.

## Getting Started

```
python installation_steps_generator.py <source_file.txt> <destination_file.js>
```

### Text file syntax
things in [] is optional

nouns:

    image {image_url}
    text {texts}   
    link {url}    
    herocard {text : sometext, images : [n, image_url1, image_url2 ... image_urln], buttons : [n, [button_text1, button_text2 ... button_textn]}    
    thumbnailcard {text : sometext, image : [n, image_url1, image_url2 ... image_urln], button : [n, [button_text1, button_text2 ... button_textn]}  
    choiceprompt {text : sometext, choices : [n, choice1, choice2, choice3 ... choicen]}   
    next

description:

    image:
        sends an image whose url is given as a parameter inside {}
    text:
        sends a text whose content is given as a parameter inside {}
    link:
        sends a button containing a link given as a parameter inside {}
    herocard:
        sends a herocard which contain optional text, n optional images, and n optional buttons
    thumbnailcard:
        sends a thumbnail which contain optional text, n optional images, and n optional buttons
    choicepropmpt:
        sends a choiceprompt which contains some optional text and n choices displayed in buttons
    next:
        go to the next waterfall step



```
#source_file.txt

```
