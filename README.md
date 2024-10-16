# ASEProject - N-Queens Solver

## Project Description
This project is a Django-based web application that provides a solution to the N-Queens problem. Users can input the number of queens they want, and the application will display a solution for a chessboard of that size.

## Features
- Interactive N-Queens solver
- User-friendly web interface with visualization
- Supports different board sizes (4x4, 8x8, etc.)

## Technologies Used
- Django
- Python
- HTML/CSS
- Bootstrap (for styling)

## Installation and Setup

### Prerequisites
- Python (version 3.6 or higher)
- Git (optional, for cloning the repository)

### Installation

#### Step 1: Clone the Repository
Open your terminal or command prompt and clone the repository using Git:
```bash
git clone https://github.com/Ilan-Goren/ASEProject.git
```
Alternatively, download the project as a ZIP file from GitHub and extract it.

#### Step 2: Navigate to the Project Directory
```bash
cd ASEProject
```

#### Step 3: Install Dependencies
Use the following command to install all the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### On Windows
1. Open Command Prompt and navigate to the project directory:
   ```cmd
   cd ASEProject
   ```
2. Run the Django development server:
   ```cmd
   python manage.py runserver
   ```

#### On macOS and Linux
1. Open Terminal and navigate to the project directory:
   ```bash
   cd ASEProject
   ```
2. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

### Access the Application
After running the server, you can access the web application by navigating to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.

## Usage
- Enter the desired number of queens in the input field.
- Click "Go to solution" to be directed to the solution page, which visualizes the N-Queens solution.
- Click "Solve it Yourself" to be directed to an N x N board page, where you can try to solve the puzzle.
- You can place a queen on the board by clicking on a cell in the board.
- You can also remove a queen by clicking on the already placed queen.
- Click on "Check Your Solution" to check your solution.
- Or you can click on "Get a possible solution if you couldn't find the solution"
## Contact
If you have any questions or suggestions, please reach out via GitHub.

