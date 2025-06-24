# Stat Videos

This project demonstrates how to create simple statistic-based videos using the
[`bar_chart_race`](https://github.com/dexplo/bar_chart_race) library. It now
scrapes nominal GDP data from Wikipedia and displays the countries one by one.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

If you provide an `OPENAI_API_KEY` environment variable, the script will use the
OpenAI API to automatically detect the GDP table structure.

## Usage

Run the script to generate the video:

```bash
python create_video.py
```

An `GIF` file named `gdp.gif` will be created in the project directory.
