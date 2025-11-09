# Paper Finder

A web application for finding and exploring academic papers, built with Solara - a react like framework on top to python to build interactive web projects.

## Features

- Search academic papers 
- Filter and sort results
- Interactive UI powered by Solara

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd solara-paper-finder
   ```

2. **Install dependencies with uv**
   ```bash
   # Install uv if you haven't already
   pip install uv
   
   # Sync dependencies (creates .venv automatically)
   uv sync
   ```

3. **Run the application**
   ```bash
   # Using uv to run in the virtual environment
   uv run solara run app.py
   
   # Or activate the virtual environment first
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   solara run app.py
   ```

4. **Open in browser**
   Navigate to `http://localhost:8765`

## Project Structure

```
solara-paper-finder/
│
├── app.py           # Main Solara app
├── pyproject.toml   # Project config and dependencies
├── uv.lock          # Locked dependency versions
├── README.md        # Project info and setup guide
├── .gitignore       # Ignore files for Git
└── data/            # (optional) Cache or results if needed
```

## Technologies

- [Solara](https://solara.dev/) - Reactive web framework
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Python 3.13+

## License

MIT License
