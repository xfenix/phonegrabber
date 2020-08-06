# Phones grabber
This simple cli/lib package can grab phones from various web pages

## Usage
* Clone this repo (this package are not going to pypi)
* Setup environment and requirements `pipenv install && pipenv shell`
* And then
    * Run `python -m phonegrabber page_url [page_url ...]`
* OR
    * `from phonegrabber.base import grab_pages` and use raw function

## Testing
* Setup environment and requirements `pipenv install --dev && pipenv shell`
* Run `pytest .`
