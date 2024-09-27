# Azure Voice List 

`azure_voice_list` is a Python package that integrates with Azure Cognitive Services Speech SDK to retrieve available voices.

## Features

- Retrieve available voices from Azure Speech SDK
- Save voice attributes to a text file
- Execute as a command-line tool for quick access
- Use as a standalone Python script within your projects

## Installation

You can install `azure_voice_list` via [PyPI](https://pypi.org/) using `pip`:

```bash
pip install azure_voice_list
```

## Usage

### 1. Importing and Using in Python Scripts

You can easily integrate `azure_voice_list` into your Python projects by importing the necessary functions.

```python
from azure_voice_list import get_available_voices

# Set your Azure credentials
speech_key = "YOUR_AZURE_SPEECH_KEY"
service_region = "YOUR_AZURE_SERVICE_REGION"

voices = get_available_voices(speech_key, service_region)
if voices:
    for voice in voices:
        print(voice)
```

### 2. Executing as a Command-Line Tool

Running `azure_voice_list` as a command-line tool allows you to retrieve and save voice attributes without writing additional Python code.

#### a. Install the Package

You can install `azure_voice_list` via [PyPI](https://pypi.org/) using `pip`:

```bash
pip install azure_voice_list
```

#### b. Run the Command-Line Tool

Once installed, you can execute the tool from your terminal:

```bash
azure-voice-list
```

**Example Output:**

```
Voice attributes have been saved to 'output/voice_attributes_20230927_123456.txt'
```

#### c. Provide Azure Credentials

The command-line tool relies on environment variables for Azure credentials. Ensure you have a `.env` file in your project's root directory with the following content:

```env
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_service_region
```

Alternatively, you can set these environment variables in your system.

### 3. Executing as a Standalone Python Script

If you prefer to run `azure_voice_list` without installing it as a package, you can execute the script directly using Python.

#### a. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/BlueBirdBack/azure_voice_list.git
cd azure_voice_list
```

#### b. Install the Package

Install the package and its dependencies using `pip`:

```bash
pip install .
```

#### c. Run the Script

Execute the `main.py` script using Python:

```bash
azure-voice-list
```

**Example Output:**

```
Voice attributes have been saved to 'output/voice_attributes_20230927_123456.txt'
```

#### d. Provide Azure Credentials

Similar to the command-line tool, ensure that the `.env` file with your Azure credentials is present in the project root directory:

```env
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_service_region
```

_Alternatively, set the environment variables in your system._

### Output Directory

By default, the `azure_voice_list` tool saves the voice attributes to an `output` directory located at the root of the project. If you encounter multiple `output` directories, ensure you're running the tool from the project root and verify the configuration in the script.

## License

[MIT](LICENSE)

## Additional Information

- **Homepage:** [https://github.com/BlueBirdBack/azure_voice_list](https://github.com/BlueBirdBack/azure_voice_list)
- **Repository:** [https://github.com/BlueBirdBack/azure_voice_list](https://github.com/BlueBirdBack/azure_voice_list)
