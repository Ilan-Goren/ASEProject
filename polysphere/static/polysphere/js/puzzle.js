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

    // Left-click event listener
    piece.addEventListener('click', () => {
        const pieceKey = piece.dataset.pieceKey;
        const data = {
            pieceKey: pieceKey
        };

        // Send POST request to rotate the piece
        fetch('rotate_piece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Error rotating piece:', response.statusText);
            }
        });
    });

    // Right-click event listener
    piece.addEventListener('contextmenu', (event) => {
        event.preventDefault(); // Prevent the default context menu from appearing

        const pieceKey = piece.dataset.pieceKey;
        const data = {
            pieceKey: pieceKey
        };

        // Send POST request to flip the piece
        fetch('flip_piece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Error flipping piece:', response.statusText);
            }
        });
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

            // Prepare data for the POST request
            const data = {
                position: { row: cellRow, col: cellCol }
            };

            // Send POST request to the server
            fetch('remove_piece', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Error placing piece:', response.statusText);
                }
            })
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

    // Send POST request to the server
    fetch('place_piece', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('POST request for placing piece not successful');
        }
    })
    
    clearHighlight();                              // Clear highlights after placing
}

// function generateSolutions() {
//     document.getElementById('stop_button').style.display = 'inline-block';
//     document.getElementById('start_button').style.display = 'none';
//     document.querySelector('.s_f_s').style.display = 'block';

//     fetch('/get-list-length/')
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById("list-length").innerText = "Current length: " + data.length;
//         })
//         .catch(error => console.log("Error fetching list length:", error));

// setInterval(updateListLength, 3000);  // Update every 3 seconds
// }