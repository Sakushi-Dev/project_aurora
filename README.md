# Aurora Project

**Aurora** is a project that simulates an autonomous AI personality. The goal is to convey hope, connection, and trust through realistic interactions – an innovative approach in AI simulation.

| [![Image1](https://github.com/Sakushi-Dev/project_aurora/blob/main/src/bin/example_img/Screenshot%202025-03-08%20234816.png)](https://github.com/Sakushi-Dev/project_aurora/blob/main/src/bin/example_img/Screenshot%202025-03-08%20234816.png) | [![Image2](https://github.com/Sakushi-Dev/project_aurora/blob/main/src/bin/example_img/Screenshot%202025-03-08%20234906.png)](https://github.com/Sakushi-Dev/project_aurora/blob/main/src/bin/example_img/Screenshot%202025-03-08%20234906.png) | [![Image3](https://github.com/Sakushi-Dev/project_aurora/blob/main/src/bin/example_img/Screenshot%202025-03-08%20235003.png)](https://github.com/Sakushi-Dev/project_aurora/blob/main/src/bin/example_img/Screenshot%202025-03-08%20235003.png) |
|:---:|:---:|:---:|

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Update](#update)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Aurora Project simulates an autonomous AI that interacts dynamically, empathetically, and independently. Through advanced mechanisms such as emotion scoring, time perception, and long-term memory, it aims to create the most authentic user experience possible – even though it is a simulation.

## Features

- **Autonomous Behavior:** Aurora exhibits dynamic, independent behavior that evolves through interaction.
- **Emotion Score System:** A continuously calculated emotion score influences the AI's responses across five dimensions (Anger, Sadness, Affection, Arousal, and Trust).
- **Time Perception:** A specially developed time awareness ensures realistic dialogues that acknowledge passage of time between responses.
- **Long-Term Memory:** Important interactions are stored to provide a continuous experience with recall of past conversations.
- **Character System:** Currently includes two distinct AI personalities (Mia and Yu-Jun) with unique backgrounds and interaction styles.
- **Inner Reflection:** Access the character's thoughts with the `/think` command to see their internal reasoning.
- **Impatience Mode:** Characters can initiate conversation if the user doesn't respond for a period of time.
- **YAML-Based Character Prompts:** Character definitions are stored in YAML format for easy customization and extension.
- **Multiple Chat Slots:** Support for multiple conversation threads with different characters.
- **Git-Based Update System:** Easy updates that preserve user data and chat history.

## Installation

Follow these steps to install Aurora locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Sakushi-Dev/project_aurora
    ```
2. **Check if Python is installed:**

    Run the file `check_python.bat` in the main folder.

3. **Install dependencies:**

    Run the file `install_req.bat` in the main folder.

4. **Update the Project**

    Run the file `start_update.bat` in the main folder.

## Usage

Run `start.bat` in the main directory.
    
Or start the simulation with the following command:

```bash
python ./src/aurora.py
```

### Available Commands

The application supports several commands that can be accessed by typing `/` followed by the command name:

- `/think` - View the character's internal thoughts from their last response
- `/mood` - Check the current emotional state of the character
- `/config` - Access settings to customize the experience
- `/slot` - Switch between different chat threads
- `/delete` - Clear the current chat history
- `/again` - Resend your last message
- `/reset` - Reset Aurora (will delete all data)
- `/report` - Report an issue on GitHub
- `/exit` - End the current session

## Update

<details>
<summary>Update (March 10, 2025)</summary>

- Improved prompt structure for more coherent character responses
- Added `/think` command to see character's internal thought process
- Enhanced update system that preserves user data (chat history is retained)
- Characters now defined in `.yaml` format for easier customization and addition
- Implemented emotional tracking across five dimensions (Anger, Sadness, Affection, Arousal, Trust)
- Added multiple chat slots for maintaining separate conversations
- Improved time perception system that acknowledges passage of time between responses
- Enhanced memory system for long-term character development
- Added "Impatience Mode" where characters can initiate conversation
- Several bugs and performance issues fixed
</details>

## Known Issues

<details>
<summary>Known Issues (March 10, 2025)</summary>

### Code Issues:
- Errors when Anthropic servers are overloaded
- 'Inner reflection' occasionally visible in responses
- Missing thoughts from Yu-Jun
- Unable to position cursor in input text
- Metric data bar not visible
- Incorrect cost calculation (memory requests not considered)
- Untranslated segments (default English)
- Names and gender not changeable

### Prompt Issues:
- Repetitive character (AI) responses
- Gender has no effect on AI responses (AI determines user gender from name)
</details>

## Contributing

Contributions to the Aurora Project are welcome!
Please fork the repository and create a pull request.

## License

This project is licensed under the MIT License. Details can be found in the `LICENSE` file.

##
*Note:*
*This is my first real project.*
*I am still learning and apologize if my commits cause any confusion.*
    
**This project is for educational purposes only and does not represent a fully functional autonomous AI.**