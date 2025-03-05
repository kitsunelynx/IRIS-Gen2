# IRIS - Intelligent Reasoning & Information System

IRIS is an intelligent assistant that combines generative AI with a suite of specialized tools to deliver a rich, interactive experience. With support for multi-modal interaction (text and voice), system control, task management, reminders, and text-to-speech, IRIS provides a seamless integration of conversational and technical tools. Thanks to its modular plugin architecture, users and developers can easily extend IRIS functionalities by adding new plugins in the `plugins/` directory.

## Features

- **Multi-Modal Interaction:** Switch easily between text and voice inputs.
- **Task & Reminder Management:** Add, manage, and cancel reminders using dedicated plugins.
- **System Control & Diagnostics:** Retrieve real-time system stats and execute shell commands.
- **Web & Wikipedia Search:** Perform searches using DuckDuckGo and fetch summaries from Wikipedia.
- **Text-to-Speech (TTS):** Convert text responses into spoken words for an enhanced auditory experience.
- **Modular Plugin Support:** Extend IRIS with additional functionalities—check out plugins for current time, system stats, command execution, exit commands, and more.
- **Persistent Chat History:** Conversations are automatically saved to disk, ensuring continuity between sessions.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/iris
   cd iris
   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**

   On Linux/Mac:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install git+https://github.com/neuml/txtai#egg=txtai[pipeline-audio,pipeline-data] onnxruntime-gpu librosa
   ```

4. **Prepare the Data Directory:**

   - Create a `data/` directory in the project root if it doesn't already exist.
   - Place your system prompt files inside the `data/` directory. IRIS prefers `.sysdt` files but will fallback to `.txt` files.
   - The conversation history and reminders are stored in `data/memory.json`. This file is automatically created when running IRIS if it does not exist.

## Configuration

All sensitive keys and tokens are now managed via a `.env` file.

1. Create a file named `.env` in the root directory of the project.
2. Add your API keys and tokens to the `.env` file in the following format:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GROKIT_AUTH_TOKEN=your_grokit_auth_token_here
   GROKIT_CSRF_TOKEN=your_grokit_csrf_token_here
   ```
3. Make sure that the `.env` file is excluded from version control (it is already added to `.gitignore`).

## Usage

Run IRIS using the entry point:

```bash
python main.py
```

Once running, you can interact with IRIS via the command line.

### In-Session Commands

- **Text Input:** Type your instruction and press Enter.
- **Voice Mode:**  
  - Enable voice input: `/voice on`
  - Disable voice input: `/voice off`
- **TTS Mode:**  
  - Enable text-to-speech: `/tts on`
  - Disable text-to-speech: `/tts off`

IRIS will process your commands, manage reminders, and maintain a persistent chat history automatically.

## Plugins

IRIS leverages a plugin system to enhance and modularize its functionalities. The `plugins/` directory includes modules for:

- **Wikipedia Search:** Quickly fetch summaries from Wikipedia.
- **Reminder Management:** Add or remove reminders.
- **Web Search:** Retrieve content and information using the DuckDuckGo search engine.
- **System Stats:** Retrieve real-time system metrics like CPU usage and memory statistics.
- **Command Execution:** Run shell commands directly from IRIS.
- **Exit Application:** Cleanly exit the system.

Feel free to add your own plugins by placing Python files in the `plugins/` directory and implementing a `register()` function that returns a list of callable tools.


## Project Structure

- `core/`: Contains the core logic, including memory management, text-to-speech, tool integrations, and the main loop.
- `plugins/`: Contains plugins extending IRIS's capabilities (e.g., `wikipedia_plugin.py`, `reminder_plugin.py`, `time_plugin.py`, `web_search_plugin.py`, etc.).
- `main.py`: Entry point to run the application.
- `requirements.txt`: Lists required Python packages.
- `.gitignore`: Specifies files and patterns to be ignored in version control.

## Troubleshooting & Contributions

- Feel free to open issues or submit pull requests on our GitHub repository if you encounter any problems or have suggestions for improvements.

---

IRIS is designed to offer a comprehensive, engaging experience by seamlessly integrating conversational capabilities with robust technical tools. Enjoy exploring and extending IRIS!
