/******************************************************************************************
                                GLOBAL VARIABLES
******************************************************************************************/

let intervalID;
let stopButton = document.getElementById('stopButton');
let startButton = document.getElementById('startButton');
let see_solutions = document.getElementById('see_sols_button');

let sfs = document.querySelector('.s_f_s');
let wts = document.querySelector('.w_t_s');
// let selectBoards = document.querySelector('.select_boards');


/******************************************************************************************
                                SOLVER EVENT LISTENERS 
******************************************************************************************/

document.getElementById('startGeneratorForm').addEventListener('submit', startSolver);
stopButton.addEventListener('click', stopSolver);

/******************************************************************************************
                                    MAIN FUNCTIONS
******************************************************************************************/

// Start solver function
function startSolver(event) {
    event.preventDefault();
    stopButton.style.display = 'inline-block';
    startButton.style.display = 'none';
    wts.style.display = 'none';
    sfs.style.display = 'block';

    fetch('start_generator', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            updateSolutions();
        });
}


// Update solutions function
function updateSolutions() {
    intervalID = setInterval(() => {
        fetch('get-solution-count')
            .then(response => response.json())
            .then(data => {
                document.getElementById('solutions_found').innerText = data.length;
            })
    }, 50); // Update every 50 ms
}

// Stop solver function
function stopSolver() {
    clearInterval(intervalID); // Stop the interval
    startButton.style.display = 'inline-block'; // Hide stop button
    stopButton.style.display = 'none'; // Hide stop button

    fetch('stop_generator', { method: 'POST' })
        .then(response => {
            if (response.status === 200) {
                window.location.reload(); // Reload the page if response is 200
            } else if (response.status === 400) {
                console.log('Error: js248'); // Alert the user if the response status is 400
            }
        })
}