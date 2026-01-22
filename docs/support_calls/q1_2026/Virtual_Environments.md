## Virtual Environments with Miniconda

### Description

- Virtual environments are isolated environments that have a Python installation which makes it really simple for installing packages that are very project-specific while avoiding any conflicts on your overall Python installation at the system level.

### Installation and Setup

1. Install `miniconda`.

- [Anaconda Official Installer Page](https://www.anaconda.com/docs/getting-started/miniconda/install#linux-2)

2. Test your installation by opening a command line interface (CLI) and type in the following command:

```bash
# Option 1 - Show all commands
conda

# Option 2 -- See version number
conda --version
```

3. Create a new virtual environment.

- Replace `env_name` with your desired environment name.
- Replace `3.11` with your specific desired version of Python to install.

```bash
conda create -n env_name python=3.11
```

4. Activate the environment.

- Replace `env_name` with your desired environment name.

```bash
conda activate env_name
```

5. Install packages either directly from `pip` or using the Conda registry via `conda` and `-c` command.

- **Alternative 1**: Install via `pip`

```bash
pip install streamlit
```

- **Alternative 2**: Conda Registry

```bash
conda install conda-forge::streamlit
```

6. Deactivate environments

```bash
conda deactivate
```

7. Remove environments

- Replace `env_name` with your desired environment name.

```bash
conda env remove -n env_name
```

