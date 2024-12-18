/******************************************************************************************
                                GLOBAL VARIABLES
******************************************************************************************/

const pieces = document.querySelectorAll('.piece');
const cells = document.querySelectorAll('.cell');
let draggedPiece = null;
let highlightCells = [];    // To keep track of highlighted cells

const boardRows = 5;        // Number of board rows
const boardCols = 11;       // Number of board columns

const rowOffset = 1;        // Offset for dragging position
const colOffset = 1;        // Offset for dragging position


let intervalID;
let stopButton = document.getElementById('stop_button');
let startButton = document.getElementById('start_button');
let resetButton = document.getElementById('reset_button');
let see_solutions = document.getElementById('see_sols_button');

let sfs = document.querySelector('.s_f_s');
let wts = document.querySelector('.w_t_s');
let selectBoards = document.querySelector('.select_boards');
let boards = document.querySelector('.boards');

/******************************************************************************************
                                PIECE EVENT LISTENERS
******************************************************************************************/

pieces.forEach(piece => {
    piece.addEventListener('dragstart', () => {
        draggedPiece = piece;
        piece.classList.add('dragging');
        clearHighlight();
    });

    piece.addEventListener('dragend', () => {
        piece.classList.remove('dragging');
        clearHighlight();
    });

    // listens if piece is left clicked to rotate
    piece.addEventListener('click', (event) => {
        const action = 'rotate'; 
        const pieceKey = piece.dataset.pieceKey;
        sendPostRequest(action, { pieceKey });
    });
    // listens if piece is right clicked to flip
    piece.addEventListener('contextmenu', (event) => {
        event.preventDefault()
        const action = 'flip';
        const pieceKey = piece.dataset.pieceKey;
        sendPostRequest(action, { pieceKey });
    });
});

/******************************************************************************************
                                BOARD CELLS EVENT LISTENERS
******************************************************************************************/

cells.forEach(cell => {
    cell.addEventListener('click', () => {
        if (cell.classList.contains('filled')) {
            const cellRow = parseInt(cell.dataset.row, 10);
            const cellCol = parseInt(cell.dataset.col, 10);
            sendPostRequest('remove', { position: { row: cellRow, col: cellCol } });
        }
    });

    cell.addEventListener('dragover', (e) => {
        e.preventDefault(); // Prevent default to allow drop
    });

    cell.addEventListener('drop', (e) => {
        e.preventDefault();

        if (!draggedPiece) return;
        const pieceArray = JSON.parse(draggedPiece.dataset.pieceArray);
        const cellRow = parseInt(cell.dataset.row, 10);
        const cellCol = parseInt(cell.dataset.col, 10);

        // Check if the piece can be placed
        if (canPlacePiece(cellRow - rowOffset, cellCol - colOffset, pieceArray)) {
            placePiece(cellRow - rowOffset, cellCol - colOffset, pieceArray);
        } else {
            alert('You cannot place a piece there!');
        }

        clearHighlight();
    });

    cell.addEventListener('dragenter', () => {
        if (draggedPiece) {
            const pieceArray = JSON.parse(draggedPiece.dataset.pieceArray);
            const cellRow = parseInt(cell.dataset.row, 10);
            const cellCol = parseInt(cell.dataset.col, 10);
            highlightPlacement(cellRow - rowOffset, cellCol - colOffset, pieceArray);
        }
    });
});


/******************************************************************************************
                                SOLVER EVENT LISTENERS 
******************************************************************************************/

document.getElementById('startForm').addEventListener('submit', startSolver);
stopButton.addEventListener('click', stopSolver);

/******************************************************************************************
                                HELPER FUNCTIONS
******************************************************************************************/

// Function to highlight the placement area for the dragged piece
function highlightPlacement(startRow, startCol, pieceArray) {
    clearHighlight();
    const pieceRows = pieceArray.length;
    const pieceCols = pieceArray[0].length;

    for (let i = 0; i < pieceRows; i++) {
        for (let j = 0; j < pieceCols; j++) {
            if (pieceArray[i][j] === 1) {
                const targetRow = startRow + i ;
                const targetCol = startCol + j;

                if (targetRow >= 0 && targetRow < boardRows && targetCol >= 0 && targetCol < boardCols) {
                    const targetCellIndex = targetRow * boardCols + targetCol;
                    const targetCell = cells[targetCellIndex];

                    if (targetCell) {
                        targetCell.classList.add('highlight');
                        highlightCells.push(targetCell);
                    }
                }
            }
        }
    }
}

// Function to clear all highlights
function clearHighlight() {
    highlightCells.forEach(cell => {
        cell.classList.remove('highlight');
    });
    highlightCells = [];
}

// Checks if piece can be placed in specific position: uses the starting row and coloumn
function canPlacePiece(startRow, startCol, pieceArray) {
    const pieceRows = pieceArray.length;
    const pieceCols = pieceArray[0].length;

    for (let i = 0; i < pieceRows; i++) {
        for (let j = 0; j < pieceCols; j++) {
            if (pieceArray[i][j] === 1) {
                const targetRow = startRow + i;
                const targetCol = startCol + j;

                // Check if the target cell is within bounds
                if (targetRow < 0 || targetRow >= boardRows || targetCol < 0 || targetCol >= boardCols) {
                    return false;
                }

                // Check if the cell is already filled
                const targetCellIndex = targetRow * boardCols + targetCol;
                const targetCell = cells[targetCellIndex];

                if (targetCell.classList.contains('filled')) {
                    return false; // Cell is already filled
                }
            }
        }
    }
    return true;
}

function placePiece(startRow, startCol, pieceArray) {
    const pieceRows = pieceArray.length;
    const pieceCols = pieceArray[0].length;

    // Array to store the occupied cells
    const occupiedCells = [];

    for (let i = 0; i < pieceRows; i++) {
        for (let j = 0; j < pieceCols; j++) {
            if (pieceArray[i][j] === 1) {
                const targetRow = startRow + i;
                const targetCol = startCol + j;
                const targetCellIndex = targetRow * boardCols + targetCol;
                const targetCell = cells[targetCellIndex];

                if (targetCell) {
                    occupiedCells.push({ row: targetRow, col: targetCol });
                }
            }
        }
    }
    const data = {
        pieceKey: draggedPiece.dataset.pieceKey,    // Include piece key
        occupiedCells: occupiedCells                // Include occupied cells
    };

    sendPostRequest('place', data);
    clearHighlight();
}

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

// function for sending post request to piece_manipulate to handle a specific action
function sendPostRequest(action, data) {
    const allActions = {
        //dictionary that contains all actions
        rotate: 'rotate',
        flip: 'flip',
        remove: 'remove',
        place: 'place'
    };
    
    fetch('piece_manipulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: allActions[action],
            ...data
        })
    })
    .then(response => {
        if (response.status === 200) {
            window.location.reload(); // Reload the page if response is 200
        } else if (response.status === 400) {
            console.log('Error: js277');
        }
    })
}