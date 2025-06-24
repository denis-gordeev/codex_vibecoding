"""Generate a simple bar chart race GIF from GDP data scraped from Wikipedia."""

import json
import os
import pandas as pd
import bar_chart_race as bcr

try:  # openai is optional and used to parse table structure
    import openai  # type: ignore
except ImportError:  # pragma: no cover - openai not available
    openai = None  # type: ignore


WIKI_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

def _llm_extract_columns(table: pd.DataFrame) -> tuple[str, str] | None:
    """Use an LLM to guess the country and GDP column names."""
    if openai is None or not os.getenv("OPENAI_API_KEY"):
        return None

    cols = [str(c) for c in table.columns]
    prompt = (
        "Given the following column names from a Wikipedia table about nominal "
        f"GDP: {cols}. Which column contains the country names and which column "
        "contains the GDP values? Respond in JSON as {\"country\": \"<name>\", "
        "\"gdp\": \"<name>\"}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        data = json.loads(resp.choices[0].message.content)
        return data.get("country"), data.get("gdp")
    except Exception:
        return None


def _heuristic_columns(table: pd.DataFrame) -> tuple[str, str]:
    """Fallback heuristic to find country and GDP columns."""
    country_col = None
    gdp_col = None
    for col in table.columns:
        cstr = " ".join(col) if isinstance(col, tuple) else str(col)
        l = cstr.lower()
        if country_col is None and ("country" in l or "territory" in l):
            country_col = col
        if gdp_col is None and ("gdp" in l or "forecast" in l or "imf" in l):
            gdp_col = col
    if country_col is None:
        country_col = table.columns[0]
    if gdp_col is None:
        gdp_col = table.columns[1]
    return country_col, gdp_col


def scrape_gdp_data(top_n: int = 5) -> pd.DataFrame:
    """Return a DataFrame of the top N countries by GDP from Wikipedia."""
    tables = pd.read_html(WIKI_URL)
    def has_gdp(tbl: pd.DataFrame) -> bool:
        for col in tbl.columns:
            col_str = " ".join(col) if isinstance(col, tuple) else str(col)
            if "gdp" in col_str.lower():
                return True
        return False

    table = next((t for t in tables if has_gdp(t)), tables[0])

    columns = _llm_extract_columns(table) or _heuristic_columns(table)
    country_col, gdp_col = columns

    df = table[[country_col, gdp_col]].head(top_n)
    df.columns = ["Country", "GDP"]
    df = df[~df["Country"].str.contains("World", case=False, na=False)]
    df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")
    return df


def create_steps(df: pd.DataFrame) -> pd.DataFrame:
    """Transform rows to sequential steps for bar_chart_race."""
    countries = df["Country"].values
    gdp_values = df["GDP"].values
    data = {}
    for i in range(len(countries)):
        step = {}
        for j in range(i + 1):
            step[countries[j]] = gdp_values[j]
        for k in range(i + 1, len(countries)):
            step[countries[k]] = 0
        data[f"Step {i + 1}"] = step
    df_steps = pd.DataFrame(data).T
    df_steps.index.name = "Step"
    return df_steps


def make_video(df: pd.DataFrame, output: str):
    """Generate bar chart race video."""
    bcr.bar_chart_race(
        df,
        filename=output,
        orientation='h',
        sort='desc',
        n_bars=len(df.columns),
        period_length=500,
        steps_per_period=10,
        title='Top Countries by GDP (Nominal)',
        bar_size=0.95,
        figsize=(6, 4),
    )


if __name__ == '__main__':
    df = scrape_gdp_data()
    df_steps = create_steps(df)
    make_video(df_steps, 'gdp.gif')
    print('Video saved to gdp.gif')
