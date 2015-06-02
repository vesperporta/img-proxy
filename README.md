# img-proxy

GET parameter based image resizing python app.

## Requires

Flask
Pillow (PIL)

## Parameters

*width=xxx&height=xxx*

Will resize an image directly to the dimensions defined.

*width=xxx or height=xxx only*

Auto resize of the other dimension keeping the images ratio.

*url=xxx*

The target image required to be resized and served back to client.
