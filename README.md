# Microsoft Bot Dialog Code Generator

Given a txt file with instructions, this code generates code that can be as waterfall steps to guide the user through an installation.

## Getting Started

```
python installation_steps_generator.py <source_file.txt>
```

### Text file syntax

actions:

    image [image_url, ... image_urln];
    text [text, .. textn];   
    link [(url, text), .. (urln, textn)];    
    herocard {text : sometext, image : [image_url1, image_url2 ... image_urln], button : [button_text1, button_text2 ... button_textn], link : [(link_text1, link_url1), (link_text2, link_url2) ... (link_textn, link_urln)]},
        {text : sometext, image : [image_url1, image_url2 ... image_urln], button : [button_text1, button_text2 ... button_textn], link : [(link_text1, link_url1), (link_text2, link_url2), ...(link_textn, link_urln)]
    };    
    thumbnailcard {text : sometext, image : [n, image_url1, image_url2 ... image_urln], button : [n, [button_text1, button_text2 ... button_textn], link : [(link_text1, link_url1), (link_text2, link_url2) ... (link_textn, link_urln)]},
        {text : sometext, image : [image_url1, image_url2 ... image_urln], button : [button_text1, button_text2 ... button_textn], link : [(link_text1, link_url1), (link_text2, link_url2) ... (link_textn, link_urln)]
    };  
    choiceprompt {text : sometext, choices : [choice1->{text : [text, textn], image : [image1, imagen], button : [button1, buttonn], link : [(link_text1, link_url1), (link_textn, link_urln)]},
        choice2->{text : [text, textn], image : [image1, imagen], button : [button1, buttonn], link : [(link_text1, link_url1), (link_textn, link_urln)]},
        ... choicen->{text : [text, textn], image : [image1, imagen], button : [button1, buttonn], link : [(link_text1, link_url1), (link_textn, link_urln)]}]
    };
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
