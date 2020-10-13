# Microchip theme for Sphinx #

This is a first attempt at a Microchip theme for [Sphinx](http://www.sphinx-doc.org/en/stable/)

To use:

- Put this sourcetree under a `Microchip` directory somewhere (consider
  putting it in `themes/Microchip`)
- Edit conf.py to add `html_theme = 'Microchip'`
- Edit conf.py to set the list `html_theme_path` to point to the directory
  containing `Microchip`, e.g.

      html_theme_path = ['../themes']

- That's it!
