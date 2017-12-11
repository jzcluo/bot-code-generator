# Microsoft Bot Dialog Code Generator

Given a txt file with instructions, this code generates code that can be as waterfall steps to guide the user through an installation.

## Getting Started

```
python installation_steps_generator.py <source_file.txt>
```

### Text file syntax
things in [] is optional

actions:

    image [n] {image_url, ... image_urln};
    text [n] {text, .. textn};   
    link [n] {(url, text), .. (urln, textn)};    
    herocard [n] {text : sometext, images : [image_url1, image_url2 ... image_urln], buttons : [button_text1, button_text2 ... button_textn], links : [(link_text1, link_url1), (link_text2, link_url2) ... (link_textn, link_urln)]}, {text : sometext, images : [image_url1, image_url2 ... image_urln], buttons : [button_text1, button_text2 ... button_textn], links : [(link_text1, link_url1), (link_text2, link_url2), ...(link_textn, link_urln)]};    
    thumbnailcard [n] {text : sometext, image : [n, image_url1, image_url2 ... image_urln], buttons : [n, [button_text1, button_text2 ... button_textn], links : [(link_text1, link_url1), (link_text2, link_url2) ... (link_textn, link_urln)]}, {text : sometext, image : [image_url1, image_url2 ... image_urln], buttons : [button_text1, button_text2 ... button_textn], links : [(link_text1, link_url1), (link_text2, link_url2) ... (link_textn, link_urln)]};  
    choiceprompt {text : sometext, choices : [n, choice1, choice2, choice3 ... choicen]};   
    next;

description:

    image:
        sends an image whose url is given as a parameter inside {}
    text:
        sends a text whose content is given as a parameter inside {}
    link:
        sends a button containing a link with the description given as a parameter inside {}
    herocard:
        sends a herocard which contain optional text, n optional images, n optional buttons, and n optional links
    thumbnailcard:
        sends a thumbnail which contain optional text, n optional images, n optional buttons, and n optional links
    choicepropmpt:
        sends a choiceprompt which contains some optional text and n choices displayed in buttons
    next:
        go to the next waterfall step



```
#source_file.txt

```
