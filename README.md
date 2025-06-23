# Sketchbook plugin

## About
Simple krita plugin for automated exporting as autonumerated PNG files. Read more on its [official page](https://krita-artists.org/t/sketchbook-like-exports-organizer-extension/106387).

## Screenshots
![toolbar](./sketchbook/screenshots/toolbar.png) ![create sketchbook dialog](./sketchbook/screenshots/create_sketchbook_dialog.png)

## Installation
- Add `sketchbook` folder, `actions` folder and `sketchbook.desktop` file to your `pykrita` folder (optionally add `sketchbook.action` file to your `actions` folder).
- Then open krita and enable this plugin by going to `Settings > Configure Krita... > Python Plugin Manager`.  
- Finally, restart krita.
- In case of troubles refer to [krita manual](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html).  

## Usage
You can use sketchbook plugin by going to `Tools > Sketchbook` or by defining shortcuts.  
For more details refer to [manual](https://saysaeqo.github.io/krita-scripts/sketchbook/manual.html).

# Other scripts
Other scripts can be used with `Ten Scripts` builtin plugin. Enjoy!  
- krita_add_sketch_layer.py - makes current layer at 30% opacity and creates new one
- krita_decrease_layer_opacity - decreases current layer opacity by 15%
- krita_increase_layer_opacity - increases current layer opacity by 15%
- krita_double_frames - adds new frame between every already existing frames
- nop - does nothing

# Changelog

- Added exporting as page (without need to create new empty document after saving current page)
