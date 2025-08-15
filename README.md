# Telegram Medical Project

## About

Hi! I'm working on a cool project that uses Telegram to collect medical data, like images and messages, and analyze it with machine learning. I’m using Jupyter notebooks to explore the data and train models (like YOLO for image classification) and Python scripts to automate stuff like data processing. This is my attempt to build something useful for medical data analysis, and I’m excited to share it!

## What’s Inside

- **Data Collection**: I set up Telegram bots to grab medical data, which gets saved in the `data/raw/` folder.
- **Data Analysis**: My Jupyter notebooks in the `notebooks/` folder do the heavy lifting for analyzing data and training models.
- **Automation**: Python scripts in the `scripts/` folder handle tasks like cleaning data or running models.
- **Other Files**:
  - `.gitignore`: Keeps out files I don’t want to share, like my virtual environment.
  - `.gitattributes`: Makes sure line endings work across different computers.
  - `requirements.txt`: Lists the Python packages you need to run the project.
  - `structure.txt`: A quick note on how I organized the project.

## How to Set It Up

1. **Get the Code**:

   ```bash
   git clone https://github.com/bekonad/Telegram_Medical_Project_week7.git
   ```
2. **Go to the Project Folder**:

   ```bash
   cd Telegram_Medical_Project_week7
   ```
3. **Set Up a Virtual Environment** (optional but I recommend it):

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run It

- **Jupyter Notebooks**: Open a notebook to see my analysis or train models:

  ```bash
  jupyter notebook notebooks/Yolo.ipynb
  ```
- **Python Scripts**: Run a script to process data or automate tasks:

  ```bash
  scripts/main.py
  ```

## Who’s Behind This

bekonad

## License

I’m using the MIT License for this project, so feel free to use or modify it as you like.
