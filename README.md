# ASEProject - N-Queens and Polysphere Solvers

## Project Description
This project is a Django-based web application that provides solutions to both the N-Queens and Polysphere puzzles. Users can solve the classic N-Queens problem by specifying the board size, or explore possible solutions for the Polysphere puzzle using a user-friendly interface.

## Features
- **N-Queens Solver**: An interactive solver that supports various board sizes (e.g., 4x4, 8x8).
- **Polysphere Solver**: Displays all possible solutions for arranging pieces on a puzzle board.
- **User-Friendly Interface**: Visual, intuitive, and easy to use.
- **Puzzle Modes**: Options to solve puzzles yourself or view pre-generated solutions.

## Technologies Used
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, Bootstrap for styling
- **Optional Containerization**: Docker, Docker Compose

## Project Structure
- `ase_project/`: Core Django application code.
- `nqueens/`: Logic and views for the N-Queens puzzle.
- `polysphere/`: Logic and views for the Polysphere puzzle.
- `static/`: Static files including CSS, JavaScript, and images.
- `templates/`: HTML templates for rendering views.
- `Dockerfile`: Instructions for building a Docker image of the project.
- `docker-compose.yml`: Configuration for Docker Compose, setting up the application with a database.
- `manage.py`: Django's management script for running commands.

## Requirements
The project's dependencies are specified in `requirements.txt`. To install them, run:

    pip3 install -r requirements.txt

## Installation and Setup

### Prerequisites
- Python (version 3.6 or higher)
- Git (optional, for cloning the repository)
- Docker (optional, if you want to run the app with Docker)

### Installation

#### Step 1: Clone the Repository
To clone the repository, open your terminal or command prompt and run:

    git clone https://github.com/Ilan-Goren/ASEProject.git

Alternatively, you can download the project as a ZIP file from GitHub and extract it.

#### Step 2: Navigate to the Project Directory
In the terminal, navigate to the project directory:

    cd ASEProject

### Running the Application Locally

#### On Windows
1. Open Command Prompt and navigate to the project directory:

       cd ASEProject

2. Start the Django development server:

       python3 manage.py runserver

#### On macOS and Linux
1. Open Terminal and navigate to the project directory:

       cd ASEProject

2. Start the Django development server:

       python3 manage.py runserver

### Access the Application
Once the server is running, open a web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

## Running the Application with Docker

If you prefer to use Docker, follow these steps:

1. **Build and Run the Docker Container**
   
       docker-compose up --build

2. **Access the Application**
   Open your browser and go to `http://localhost:8000/`.

3. **Shut Down the Docker Environment**
   
       docker-compose down

## Usage

### N-Queens Solver
- Input the desired number of queens.
- Click "Go to solution" to view a pre-calculated solution for the board.
- Click "Solve it Yourself" to try solving the puzzle on your own.
- Place a queen on the board by clicking on a cell. Click an already placed queen to remove it.
- Use "Check Your Solution" to validate your placement or "Get a possible solution" for hints.

### Polysphere Solver
- Access the Polysphere solver from the application menu.
- Click "Start" to generate all possible solutions for a 5x11 board.
- View all generated solutions by clicking "Go see them."
- Use the filter to view specific solutions by providing a range.
- You can attempt to solve the puzzle yourself or use the auto-solve function to complete the board.

## Configuration

### Environment Variables
If you plan to deploy the application in a production environment, set up environment variables such as `SECRET_KEY` for Django. Create a `.env` file if necessary, with content similar to:

    export SECRET_KEY="your_secret_key"
    export DEBUG=True

### Docker Configuration
To configure the database or other services, edit `docker-compose.yml`. By default, the configuration uses PostgreSQL as the database service.

## Contributing
To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request for review.

## Contact
For any questions or suggestions, please reach out via GitHub.

[Polysphere Solver Documentation](https://github.com/user-attachments/files/17577804/polysphere.solver.explained.docx)
