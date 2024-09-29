# gradient message box

<img src="https://github.com/inviti8/gradientmessagebox/blob/main/gradientmessagebox_img.png?raw=true" alt="gradientmessagebox_img.png" width="536" height="319">

A very simple tkinter prompt window with an animated gradient background.

Installation:

```
pip install gradientmessagebox
```

Several Presets that require basic configuration:

```python
from gradientmessagebox import ColorConfig, PresetPromptWindow, PresetLoadingMessage, PresetImageBgMessage, PresetChoiceWindow, PresetChoiceEntryWindow, PresetChoiceMultilineEntryWindow, PresetCopyTextWindow, PresetUserPasswordWindow
```

**PresetLoadingMessage:**  
<img src="https://github.com/inviti8/gradientmessagebox/blob/main/loading.png?raw=true" alt="loading.png" width="400" height="107">

```python
'''
Basic loading indicator that can create a custom Loading message, plays a simple text animation.
shows without a frame, must be closed in code.
'''

loading = PresetLoadingMessage('LOADING')

loading.Play()

time.sleep(10)

loading.Close()
```

**PresetImageBgMessage:**

<img src="https://github.com/inviti8/gradientmessagebox/blob/main/splash.png?raw=true" alt="loading.png" width="339" height="280">

```python
'''
Basic text pop up with a background image.
shows without a frame, must be closed in code.
'''

splash = PresetImageBgMessage(msg='THE TITLE', bg_img='./bg_image.png', logo_img='./logo.png')

splash.Show()

time.sleep(10)

splash.Close()
```

**PresetPromptWindow:**

```python
'''
Basic choice window with an accept and a reject button.
returns the text of the clicked button
'''

prompt = PresetPromptWindow('You are kinda cool!', 'OK')
prompt.Prompt()

##no return
```

**PresetChoiceWindow:**

```python
'''
Basic choice window with an accept and a reject button.
returns the text of the clicked button
'''

choice = PresetChoiceWindow('Cool?', 'Yup', 'Nope')

answer = choice.Ask()
print(answer.response)

#~"Yup"
```

**PresetChoiceEntryWindow:**

```python
'''
Basic choice window with a text entry, an accept button, and a reject button.
returns the text of the entry, or reject button
'''

prompt = PresetChoiceEntryWindow('Why so Cool?', 'Enter', 'Nope')

prompt.Ask()

answer = prompt.Ask()
print(answer.response))

#Returns text entered into field
#~"None of your business..."
```

&nbsp;

**PresetDropDownWindow:**

```python
'''
Basic choice window with a drop down, an accept button, and a reject button.
returns the drop down value, or reject button
'''

prompt = PresetDropDownWindow('How Cool?', 'Enter')

answer = prompt.DropDown(['Pretty cool', 'Cool', 'Huh?'])

print(answer.response)

#Returns text entered into field
#~"None of your business..."
```

&nbsp;

**PresetChoiceMultilineEntryWindow:**

```python
'''
Basic choice window with a multi line text entry, and an accept and a reject button.
returns the text of the entry, or reject button
'''

prompt = PresetChoiceMultilineEntryWindow('Coolness details:', 'Enter', 'Nope')

answer = prompt.Ask()

print(answer.response)

#Returns text entered into field
#~"None of your business..."
```

&nbsp;

All window objects  text and color attributes can be configured, here are some examples:

```python
popup = PresetChoiceWindow('Cool?', 'Yup', 'Nope')

'''
Add a header text to the popup
'''
win.set_title_text('QUIZ')

'''After creating various attributes can be configured
Here we lighten the foreground, and darken the background
By Default, foreground is the text color, and background is the widget surface color.'''
popup.fg_luminance(0.65)
popup.bg_luminance(0.35)

'''
add a bg image & logo to the window
'''

window.imagery('./hvym_3d_logo.png', './logo.png')

'''If you want to invert the foreground and background colors:'''
popup.invert()

'''On instantiation a midground color is created, based on the
the color that is halfway between the foreground and background.
To swap the midground for the foreground or background:'''
popup.swap_mg_for_fg()
##or
popup.swap_mg_for_bg()

'''Here we reduce the saturation of the gradient used on the pop up background
We could also lighten or darken it with config.gradient_luminance'''
popup.gradient_saturation(0.5)

'''Set the text to a custom color with'''

popup.custom_txt_color('red')#use web color codes
```

&nbsp;

Pop ups can also be configured with a config object, for more customization:

```python
from gradientmessagebox import ColorConfig, ChoiceWindow, MultiTextChoice, CopyText, UserPasswordWindow

'''Create the color configuration for the dialog:'''
config = ColorConfig(width=450, height=300, color1="#00ffff", color2="#ffa500", alpha=1.0, saturation=1.0, direct='+x', hasframe=True)
```

Color colors can be manipulated per element:

```
'''Here we lighten the foreground, and darken the background
By Default, foreground is the text color, and background is the widget surface color.'''
config.fg_luminance(0.65)
config.bg_luminance(0.35)

'''If you want to invert the foreground and background colors:'''
config.invert()

'''On instantiation a midground color is created, based on the
the color that is halfway between the foreground and background.
To swap the midground for the foreground or background:'''
config.swap_mg_for_fg()
##or
config.swap_mg_for_bg()

'''Here we reduce the saturation of the gradient used on the pop up background
We could also lighten or darken it with config.gradient_luminance'''
config.gradient_saturation(0.5)

'''This call will add an image to the pop up background on
top of the gradient.  If logo is set, a logo for the window
is applied. If useImgSize is True, the pop up size is based on
the image size passed.'''
config.imagery(path='./test-bg.png', icon_path='./logo.png', useImgSize=False)
```

animation can be applied to the gradient background of the pop up:

```python
'''Speed is in ms, so lower is faster
Stretch, lengthens the gradient, generally makes it look
better if it's a little longer in length.'''
config.animation(speed=10, stretch=2)
```

Example1 ~ Choice Window:

```python
'''Create the window:'''
choice = ChoiceWindow(config)

'''Create a simple pop up, with option to add a text entry field,
Without the field, the popup returns the text of the button pressed
With an entry field, the accept button returns the text from the entry field.'''
answer = choice.Ask(msg='What's up?', b_accept='Chillin', b_decline='Nah', entry=False, horizontal=True)

print(answer.response)

'''Returns: "Chillin"'''
```

There are currently 4 window types:  
ChoiceWindow, MultiTextChoice, CopyText, UserPasswordWindow

Each Window has an Ask('your prompt') method which will pop the window.