document.addEventListener("DOMContentLoaded", function() {
    // Navigation between Home and Solver
    const startGameBtn = document.getElementById("start-game-btn");
    const homeSection = document.getElementById("home");
    const solverSection = document.getElementById("solver");

    startGameBtn.addEventListener("click", function() {
        homeSection.style.display = "none";
        solverSection.style.display = "block";
    });

    // Game canvas setup
    const canvas = document.getElementById("game-canvas");
    const ctx = canvas.getContext("2d");

    // Define different shapes
    let shapes = [
        { blocks: [{ x: 200, y: 160 }, { x: 240, y: 160 }, { x: 240, y: 200 }, { x: 280, y: 200 }], color: 'blue' }, // L-Shape
        { blocks: [{ x: 360, y: 160 }, { x: 400, y: 160 }, { x: 440, y: 160 }, { x: 400, y: 200 }], color: 'red' },  // T-Shape
        { blocks: [{ x: 520, y: 200 }, { x: 560, y: 200 }, { x: 560, y: 240 }, { x: 600, y: 240 }], color: 'green' }, // Z-Shape
        { blocks: [{ x: 680, y: 200 }, { x: 720, y: 200 }, { x: 680, y: 240 }, { x: 720, y: 240 }], color: 'yellow' }  // Square
    ];

    // Currently selected shape index
    let selectedShapeIndex = 0;

    // Draw the selected shape on the canvas
    function drawShape() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
        let shape = shapes[selectedShapeIndex];
        ctx.fillStyle = shape.color;
        for (let block of shape.blocks) {
            ctx.fillRect(block.x, block.y, 80, 80);
        }
    }

    // Draw the initial shape
    drawShape();

    // Rotate the selected shape 90 degrees clockwise
    function rotateShape() {
        const shape = shapes[selectedShapeIndex];
        const pivot = shape.blocks[0]; // Use the first block as the pivot point
        shape.blocks = shape.blocks.map(block => {
            const offsetX = block.x - pivot.x;
            const offsetY = block.y - pivot.y;
            return {
                x: pivot.x - offsetY,
                y: pivot.y + offsetX
            };
        });
        drawShape();
    }

    // Flip the selected shape horizontally
    function flipShape() {
        const shape = shapes[selectedShapeIndex];
        const pivot = shape.blocks[0]; // Use the first block as the pivot point
        shape.blocks = shape.blocks.map(block => {
            const offsetX = block.x - pivot.x;
            return {
                x: pivot.x - offsetX,
                y: block.y
            };
        });
        drawShape();
    }

    // Movement logic for the shape
    function moveShape(direction) {
        for (let block of shapes[selectedShapeIndex].blocks) {
            switch (direction) {
                case 'up':
                    block.y -= 80; // Move by the size of the grid cell
                    break;
                case 'down':
                    block.y += 80;
                    break;
                case 'left':
                    block.x -= 80;
                    break;
                case 'right':
                    block.x += 80;
                    break;
            }
        }
        drawShape();
    }

    // Event listeners for movement buttons
    document.getElementById("move-up-btn").addEventListener("click", function() {
        moveShape('up');
    });
    document.getElementById("move-down-btn").addEventListener("click", function() {
        moveShape('down');
    });
    document.getElementById("move-left-btn").addEventListener("click", function() {
        moveShape('left');
    });
    document.getElementById("move-right-btn").addEventListener("click", function() {
        moveShape('right');
    });

    // Rotate button event handler
    document.getElementById("rotate-btn").addEventListener("click", function() {
        rotateShape();
    });

    // Flip button event handler
    document.getElementById("flip-btn").addEventListener("click", function() {
        flipShape();
    });

    // Calculate button event handler
    document.getElementById("calculate-btn").addEventListener("click", function() {
        // Trigger backend logic
        fetch('/calculate-solution/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // CSRF token is required for POST requests in Django
            },
            body: JSON.stringify({ shape: shapes[selectedShapeIndex] })
        })
        .then(response => response.json())
        .then(data => {
            const resultMessage = document.getElementById("result-message");
            if (data.solvable) {
                resultMessage.textContent = "This arrangement is solvable!";
                resultMessage.style.color = "green";
            } else {
                resultMessage.textContent = "This arrangement is not solvable.";
                resultMessage.style.color = "red";
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Utility function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Event listener for changing shape
    const shapeSelect = document.getElementById("shape-select");
    shapeSelect.addEventListener("change", function() {
        selectedShapeIndex = parseInt(shapeSelect.value);
        drawShape();
    });
});
