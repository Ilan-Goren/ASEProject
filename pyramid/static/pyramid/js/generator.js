/******************************************************************************************
                                 GLOBAL VARIABLES
******************************************************************************************/

let intervalID;
let stopButton = document.getElementById('stopButton');
let startButton = document.getElementById('startButton');
let see_solutions = document.getElementById('see_sols_button');

let sfs = document.querySelector('.s_f_s');
let wts = document.querySelector('.w_t_s');

/******************************************************************************************
                                SOLVER EVENT LISTENERS 
******************************************************************************************/

startButton.addEventListener('click', startSolver);
stopButton.addEventListener('click', stopSolver);

/******************************************************************************************
                                    MAIN FUNCTIONS
******************************************************************************************/

/* 
 * Starts the solver by initiating a POST request to start the generation process, hiding the start button
 * 
 * Args:
 *   event (Event): The event triggered by clicking the start button.
 */
function startSolver(event) {
    event.preventDefault();
    startButton.style.display = 'none';
    wts.style.display = 'none';
    sfs.style.display = 'block';

    fetch('start_generator', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            updateSolutions();
        });

    // Delay the display of the stop button by 3 seconds
    setTimeout(() => {
        stopButton.style.display = 'inline-block';
    }, 1000);
}

/* 
 * Stops the solver by clearing the interval, hiding the stop button, and sending a POST request to stop the generation process.
 * Reloads the page if the backend responds with a 200 status code, or logs an error message if the status is 400.
 *
 * Args: 
 *   None
 */
function stopSolver() {
    clearInterval(intervalID); // Stop the interval
    startButton.style.display = 'inline-block'; // Hide stop button
    stopButton.style.display = 'none'; // Hide stop button

    fetch('stop_generator', { method: 'POST' })
        .finally(() => {
            window.location.reload(); // Reload the page
        });
}

/* 
 * Periodically checks for the number of solutions generated and updates the display. 
 * If the generation process is complete, it stops the solver and updates the interface.
 *
 * Args: 
 *   None
 */
function updateSolutions() {
    intervalID = setInterval(() => {
        fetch('get-solution-count')
            .then(response => response.json())
            .then(data => {
                if (data.Done === "Generation completed") {
                    stopSolver();
                } else {
                    document.getElementById('solutions_found').innerText = data.length;
                }
            })
    }, 100);
}