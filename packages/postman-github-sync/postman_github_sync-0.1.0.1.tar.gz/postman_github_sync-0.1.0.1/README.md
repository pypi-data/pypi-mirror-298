# PostmanxGithub Action Automatic Sync

This Python package automates the process of setting up GitHub Actions workflows for Postman collections. It supports both GitHub repository integration and local workflow setup, allowing for flexible usage in various scenarios.

## Features

- Export Postman collections using a UID or from a local file
- Add Postman collections to GitHub repositories (new or existing)
- Create or update GitHub Actions workflows
- Set up workflows locally without GitHub interaction
- Use custom YAML templates for GitHub Actions workflows
- Support for both new and existing repositories

## Installation

You can install the package using pip:

```bash
pip install postman-github-sync
```

## Usage

After installation, you can use the package in two ways:

1. As a command-line tool:

```bash
postman_github_sync [--local] [--template PATH_TO_TEMPLATE]
```

2. As a Python module:

```python
from postman_github_sync import main

main()
```

### Command-line Options

- `--local`: Set up the workflow files locally without interacting with GitHub.
- `--template PATH_TO_TEMPLATE`: Use a custom YAML template for the GitHub Actions workflow.

### Environment Variables

- `GITHUB_TOKEN`: Your GitHub personal access token (required for GitHub operations)
- `POSTMAN_API_KEY`: Your Postman API key (required for exporting collections by UID)

## Examples

1. Setting up a workflow in a GitHub repository:
   ```bash
   postman_github_sync
   ```

2. Setting up a local workflow:
   ```bash
   postman_github_sync --local
   ```

3. Using a custom template for GitHub setup:
   ```bash
   postman_github_sync --template my_template.yml
   ```

## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/postman_github_sync.git
   cd postman_github_sync
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
