## Dagster Web Server

### Description

- A CLI and web UI to work with Dagster.

### Installation and Setup

1. Install the package via `pip`.

```bash
pip install dagster-webserver
```

2. Generate a Dagster project through the CLI.

- Replace `project_name` with the name of your project.

```bash
dagster project scaffold --name project_name
```

3. Navigate to the project.

```bash
cd project_name
```

4. Start the web UI.

```bash
dagster dev
```

