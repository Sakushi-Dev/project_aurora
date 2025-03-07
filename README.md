# Aurora Project

**Aurora** is a project that simulates an autonomous AI personality. The goal is to convey hope, connection, and trust through realistic interactions – an innovative approach in AI simulation.

|[![Image1](https://iili.io/3HVoU22.th.png)](https://freeimage.host/i/3HVoU22) | [![Image2](https://iili.io/3HVog7S.th.png)](https://freeimage.host/i/3HVog7S) | [![Image3](https://iili.io/3HVo8rl.th.png)](https://freeimage.host/i/3HVo8rl)|
|:---:|:---:|:---:|

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Update](#update)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Aurora Project simulates an autonomous AI that interacts dynamically, empathetically, and independently. Through advanced mechanisms such as emotion scoring, time perception, and long-term memory, it aims to create the most authentic user experience possible – even though it is a simulation.

## Features

- **Autonomous Behavior:** Aurora exhibits dynamic, independent behavior.
- **Emotion Score:** A continuously calculated emotion score influences the AI's responses.
- **Time Perception:** A specially developed time logic ensures realistic dialogues.
- **Long-Term Memory:** Important interactions are stored to provide a continuous experience.

## Installation

Follow these steps to install Aurora locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Sakushi-Dev/project_aurora
    ```
2. **Check if Python is installed:**

    ```bash
    cd check_python.bat
    ```
    or start the file `check_python.bat` in main folder.
3. **Install dependencies:**

    ```bash
    cd install_req.bat
    ```
    or start the file `install_req.bat` in main folder.

## Update

<details>
<summary>Update (March 7, 2025)</summary>

# Project Aurora Functionality Analysis

## Core Code Functions

1. **Character AI Simulation**: 
   - The code creates an interactive AI character system with different personalities (Mia and Yu-jun)
   - Each character has their own traits, memories, and reactions

2. **Prompt Engineering Framework**:
   - The `PromptBuilder` class generates structured prompts for the AI model
   - Dynamic template system using Jinja for flexible prompts
   - Parameters like `char_name`, `user_name`, `language`, and `gender` are inserted into templates

3. **Emotion System**:
   - Character has dynamic moods based on user interaction
   - `<mood>` tags store and communicate the emotional state to the model

4. **Time Perception**:
   - Characters can have a sense of time (especially Mia)
   - `time_sense` parameter is used to simulate temporal continuity

5. **Memory System**:
   - The AI retains memories of previous conversations
   - `<memory>` tags enable context-aware responses

6. **Response Processing**:
   - Responses are split into two parts: `<inner_reflection>` and `<response>`
   - `inner_reflection` contains the character's internal thought processes
   - `response` contains the actual text seen by the user

7. **API Communication**:
   - Structured communication with Claude API through `final_client.messages.stream`
   - Streaming response processing for real-time interaction
   - Error handling for API failures

8. **Interactive User Interface**:
   - `dynamic_typing` and `animated_typing_panel` for animated text output
   - Rich library for colored console display and formatted text

9. **Command Mode**:
   - Commands with `/` as prefix
   - Enables meta-interactions like mood queries and setting changes

10. **Cost Monitoring**:
    - Calculation of tokens and costs for API requests
    - Display of usage metrics after each interaction

11. **Dynamic Response Length**:
    - `random_response_length()` generates random minimum and maximum lengths for responses
    - Adjusts based on settings like "short", "medium", "long"

12. **YAML Configuration**:
    - External YAML files for prompt templates and system rules
    - Clear separation of code and content

## Data Flow

1. User enters a message → formatted to `format_user_input`
2. Message is added to the history
3. `stream_chat_response` prepares the request and sets global variables
4. `print_ki_response` sends the request to the API and receives chunks
5. Response is split through `split_response` into reflection and response text
6. Response is displayed with animation and costs calculated
7. The new response is added to the history for context retention

The code skillfully combines AI technology with narrative elements to create an immersive chat experience with dynamic, context-aware responses.

I have improved the prompt structure to make it more organized and easier to read.
</details>

## Usage

Run `start.bat` in the main directory.
    
Or start the simulation with the following command:

```bash
python ./src/aurora.py
```
    
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

