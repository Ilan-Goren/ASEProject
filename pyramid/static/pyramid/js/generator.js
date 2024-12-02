/******************************************************************************************
                                GLOBAL VARIABLES
******************************************************************************************/

let intervalID;
let stopButton = document.getElementById('stopButton');
let startButton = document.getElementById('startButton');
let see_solutions = document.getElementById('see_sols_button');
// let startGenerator = document.getElementById('startGeneratorForm')

let sfs = document.querySelector('.s_f_s');
let wts = document.querySelector('.w_t_s');
// let selectBoards = document.querySelector('.select_boards');


/******************************************************************************************
                                SOLVER EVENT LISTENERS 
******************************************************************************************/

startButton.addEventListener('click', startSolver);
stopButton.addEventListener('click', stopSolver);

/******************************************************************************************
                                    MAIN FUNCTIONS
******************************************************************************************/

// Start solver function
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