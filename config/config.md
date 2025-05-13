# AI Moon Visibility Reporting

This project provides a tool to generate moon visibility reports based on a specific date, Islamic month, and Islamic year. It includes a FastAPI server that can be accessed locally, a form to generate reports, and a batch file (`start_app.bat`) to automatically start the app when your computer boots.

## Requirements

Before running the app, make sure to install the required dependencies.

1. **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd AI_Moon_Visibilty_Reporting
    ```

2. **Create a Python environment**:

    If you are using Anaconda, you can create an environment and install the dependencies:

    ```bash
    conda create --name moon-env python=3.8
    conda activate moon-env
    ```

3. **Install required Python packages**:

    Make sure you have `pip` installed and then run:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should contain:

    ```
    fastapi
    uvicorn
    google
    requests
    tqdm
    pandas
    markdown-pdf
    python-dotenv
    ```

4. **Install any other dependencies**:
   Ensure all additional tools and packages (like `conda`) are installed properly. If using `conda`, make sure the virtual environment is activated.

---

## Running the Application

1. **Start the FastAPI server**:

   To run the FastAPI server locally, use the following command:

   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

   This will start the server on `http://127.0.0.1:8000`, and you can interact with it via the HTML form at `http://127.0.0.1:8000/`.

---

## Auto-Start Application on Boot (Windows)

To have this application start automatically when your computer boots up, follow these steps:

### Step 1: Create the Batch File (`start_app.bat`)

1. **Create a batch file** `start_app.bat` inside the project directory with the following content:

   ```bat
   @echo off
   cd to\the\project\AI_Moon_Visibilty_Reporting\
   call conda activate moon-env
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

   This batch file activates the `moon-env` environment and starts the FastAPI app with `uvicorn`.

### Step 2: Create the VBScript (`start_app.vbs`)

1. **Create a VBScript** `start_app.vbs` inside the same directory with the following content:

   ```vbs
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run chr(34) & "to\the\project\dir\AI_Moon_Visibilty_Reporting\start_app.bat" & Chr(34), 0
   Set WshShell = Nothing
   ```

   This script will silently run the `start_app.bat` file without showing a command prompt window.

### Step 3: Add the VBScript to the Startup Folder

1. Press `Win + R` to open the **Run** dialog, type `shell:startup`, and press **Enter**. This will open the **Startup** folder.
2. Copy the `start_app.vbs` file into the **Startup** folder.

Now, every time your computer restarts, the FastAPI server will start automatically, and you don't have to manually run the batch file.

---

## HTML Form Styling

The form is styled to center itself in the middle of the page for a better user experience. The updated HTML page includes input fields for the **Date**, **Islamic Month**, and **Islamic Year**.

---

## Troubleshooting

- **If the FastAPI server is not accessible**, make sure your firewall allows connections on port `8000`.
- **If you encounter errors related to the dependencies**, check that all required packages are installed by running `pip list` or `conda list`.
- **For API errors**, make sure that the necessary API keys and configurations (like `.env` files) are properly set up.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

## Summary of Updates in `README.md`:

1. **How to Run the Application**: Instructions on how to install dependencies and run the FastAPI server.
2. **Auto-Start on Boot**: Detailed instructions on how to automatically run the FastAPI app when the computer starts using a `start_app.bat` batch file and a `start_app.vbs` VBScript.
3. **Troubleshooting**: General tips on resolving issues that may arise during setup.

This should now fully document how to use the app and set it up to run on startup.