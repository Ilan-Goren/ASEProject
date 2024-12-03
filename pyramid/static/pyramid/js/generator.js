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
 * Starts the solver by initiating a POST request to start the generation process, hiding the start button, 
 * showing the "working" status message, and displaying the stop button after a delay.
 * 
 * Args:
 *   event (Event): The event triggered by clicking the start button.
 *
 * Notes:
 * - Prevents the default behavior of the button click event.
 * - Hides the start button and welcome status (wts), then shows the status for the solver (sfs).
 * - Sends a POST request to the backend ('start_generator') to begin the generation process.
 * - Updates the solutions upon receiving a response from the backend.
 * - Shows the stop button after a delay of 1 second.
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
 *
 * Notes:
 * - Clears the interval identified by `intervalID` to stop the periodic updates.
 * - Makes the start button visible again and hides the stop button.
 * - Sends a POST request to the backend ('stop_generator') to halt the generation process.
 * - Reloads the page if the server responds with a 200 status, or logs an error if the response status is 400.
 */
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

/* 
 * Periodically checks for the number of solutions generated and updates the display. 
 * If the generation process is complete, it stops the solver and updates the interface.
 *
 * Args: 
 *   None
 *
 * Notes:
 * - Uses `setInterval` to make periodic requests to the server for the solution count.
 * - If the server responds that the generation is completed, it stops the solver by calling `stopSolver()`.
 * - Otherwise, it updates the number of solutions found in the UI by modifying the text content of the element with ID 'solutions_found'.
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