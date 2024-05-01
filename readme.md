# Automatically quantify in WDCquantify

This Image uses python selenium and Firefox to automatically sign you in and press the "Quantify" button for you on a specified time.\
To solve the login captcha we use tesseract ocr.

# Running

To run the container, specify your environment variables and run the image using docker:
> The container runs in London time, just like WDC.
```bash
docker run -e "HOUR=20" -e "MINUTE=05" -e "WDCUsername=123456789" -e "WDCPassword=changeme" -it ghcr.io/makramc/wdcautomate:latest
```

Or deploy using docker-compose:

```yml
services:
  wdcautomate:
    image: ghcr.io/makramc/wdcautomate:latest
    environment:
      - HOUR=20
      - MINUTE=05
      - WDCUsername=123456789
      - WDCPassword=yourpassword
```

# Contents
This container is based on the python image. There are additional packages that need to be installed to the alpine base image.

## Packages
`firefox` - The firefox web browser where we load the site and log in.\
`tesseract` - For solving captchas using optical character recognition.\
`tesseract-eng` - The English dataset for tesseract.\

## Pip dependencies
`selenium` - For controlling the headless firefox browser.\
`pytesseract` - Wrapper to use tesseract in python.\
`webdriver-manager` - So we don't manually have to install the webdrivers for selenium.

# Building
To build a test image:

```bash
docker build -t wdcautomate:test .
```

# Disclamer
WDC Quantify is likely a pyramid scheme. Please do not "invest" your hard earned money on this platform.
I am of course not responsible for any losses on this platform or through my script.

I created this project as a proof of concept and to educate myself and learn about python and docker and had a lot of fun creating it. I do not know if I find the time/resources to maintain this if something ever changes on WDC's website/backend.

# Contributing
If you got ideas/fixes/patches I am open to pull requests or issues.