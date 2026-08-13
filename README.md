
## Dependencies

```
sudo apt update && sudo apt install -y \
  build-essential \
  python3-dev \
  libjpeg-dev \
  zlib1g-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libopenjp2-7-dev \
  libtiff5-dev \
  libwebp-dev \
  swig \
  liblgpio-dev
```

## uv run:
`uv run --env-file .env --with ./dexcom_paper_display-0.1.0-py3-none-any.whl --no-project -- dexcom-paper-display`
