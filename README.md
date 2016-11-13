# img_to_angles
Convert the contours of an image to x*y angles

## What it does

It will slice an image in a predefined size x*y. Then it will put into each slice a line which goes through the center of the slice and
tries to fit best to all pixel.

Our typical use-case is 10*10 while the images are of size around 500*500. So a single slice is 50*50. To draw the line, we use [linear regression](https://en.wikipedia.org/wiki/Polynomial_regression) twice: one for x/y axis and one for y/x axis - the bast fit is used. After that we will move the function through the center of the slice and calculate the angle.

Additionally, we don't want to look at all the pixels, so we have a preprocessing step in which we will render this image in black and
white, correct aspect ratio for the resulting size and apply the filter `find_edges` to it.

### Example

Suppose you have following image of the letter I:
```
__****__
___**___
___**___
___**___
___**___
__****__
```
Then we want to divide this image in 6x8 slices and calculate an angle for each slice.
This means for slice(0,0) the symbol is `_` and the angle is 0. For slice(0,3) the symbol is `*` and the angle is 180.

Suppose we want to divide this image in 3x4 slices - then a single slice represents 2x2 pixel. This means for slice(0,0) the symbol is
```
__
__
```
and the angle is 0. For slice(0,1) the symbol is
```
_*
__
```
The angle will be 225 as we try to fit following line:
```
\
 \
```

## Installation
You need python3.

```
# Install the python requirements
pip install --user -r requirements.txt
```

## Usage

Normally you want to call `./img2angle.py file.png`
