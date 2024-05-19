# CHAPY: A GenAI Based Python Programming Assistant Prototype

A Python Assistant Application Prototype based on GPT for local files. Users can interact with the app 
through test or voice messages. 

## Requirements

- Python 3.11 or higher


## Repository Contents

This repository contains the following files:

### `main.py`

This is the main entry point for the application. It sets up the user interface using Flet and handles user interactions such as text input and voice commands. It also integrates with other modules to provide responses and process user inputs.

### `Model.py`

This file contains the code related to the GPT-based model used by the application. It handles loading the model, processing inputs, and generating responses. The model interacts with the user's text or voice inputs to provide relevant programming assistance.

### `python_script.py`

This file includes utility functions for handling and executing Python scripts. It is responsible for running user-provided Python code snippets and returning the output or any errors encountered during execution.

### `audio_record.py`

This file manages audio recording and processing. It allows the user to interact with the application through voice commands by recording audio, converting it to text, and sending it to the model for processing. It also handles playback of audio responses if implemented.

### `functions.py`

This file contains various helper functions used throughout the application. These functions may include text processing, file handling, and other utility operations needed to support the main functionality of the application.



## Installation

1. Clone this repository:

    ```sh
    git clone https://github.com/mathhackuab190524/python_assistant.git
    ```

2. Install the dependencies:

    ```sh
    pip install flet tkinter soundfile pyaudio langchain langchai_openai langchain_core langchain_community
    ```

## Usage

To run the application locally:

```sh
python main.py
```
