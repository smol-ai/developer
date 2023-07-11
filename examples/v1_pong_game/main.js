// Define the canvas, paddles, ball and score
const canvas = document.getElementById("gameArea");
const ctx = canvas.getContext("2d");
let playerPaddle = { x: 0, y: 200, width: 10, height: 100 };
let aiPaddle = { x: 390, y: 200, width: 10, height: 100 };
let ball = { x: 200, y: 200, radius: 5, dx: 2, dy: 2 };
let score = { player: 0, ai: 0 };

// Initialize the game state
function startGame() {
    playerPaddle.y = 200;
    aiPaddle.y = 200;
    ball.x = 200;
    ball.y = 200;
    ball.dx = 2;
    ball.dy = 2;
    score.player = 0;
    score.ai = 0;
}

// Listen for mouse movement to control the player's paddle
canvas.addEventListener("mousemove", playerMove);

// Control the player's paddle based on mouse movement
function playerMove(event) {
    let rect = canvas.getBoundingClientRect();
    playerPaddle.y = event.clientY - rect.top - playerPaddle.height / 2;
}

// Control the AI paddle based on the ball's position
function aiMove() {
    let targetY = ball.y - (aiPaddle.height - ball.radius) / 2;
    aiPaddle.y += (targetY - aiPaddle.y) * 0.1;
}

// Check for collisions between the ball and the paddles or the boundaries of the canvas
function checkCollision() {
    // Ball and player paddle
    if (ball.y + ball.radius > playerPaddle.y && ball.y - ball.radius < playerPaddle.y + playerPaddle.height && ball.dx < 0) {
        if (ball.x - ball.radius < playerPaddle.x + playerPaddle.width) {
            ball.dx *= -1;
            increaseBallSpeed();
        }
    }

    // Ball and AI paddle
    if (ball.y + ball.radius > aiPaddle.y && ball.y - ball.radius < aiPaddle.y + aiPaddle.height && ball.dx > 0) {
        if (ball.x + ball.radius > aiPaddle.x) {
            ball.dx *= -1;
            increaseBallSpeed();
        }
    }

    // Ball and top or bottom
    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        ball.dy *= -1;
    }
}

// Update the score based on ball-paddle collisions
function updateScore() {
    if (ball.x + ball.radius > canvas.width) {
        score.player++;
        startGame();
    } else if (ball.x - ball.radius < 0) {
        score.ai++;
        startGame();
    }
}

// Increase the ball's speed every time it bounces off a paddle
function increaseBallSpeed() {
    ball.dx *= 1.1;
    ball.dy *= 1.1;
}

// Update the game state at every frame
function updateGame() {
    // Move the ball
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Move the AI paddle
    aiMove();

    // Check for collisions
    checkCollision();

    // Update the score
    updateScore();

    // Render the game state
    drawGame();

    // Schedule the next update
    requestAnimationFrame(updateGame);
}

// Render the game state
function drawGame() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the paddles
    ctx.fillStyle = "yellow";
    ctx.fillRect(playerPaddle.x, playerPaddle.y, playerPaddle.width, playerPaddle.height);
    ctx.fillRect(aiPaddle.x, aiPaddle.y, aiPaddle.width, aiPaddle.height);

    // Draw the ball
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
    ctx.fillStyle = "red";
    ctx.fill();

    // Draw the score
    ctx.font = "30px Arial";
    ctx.fillText(score.player, 50, 50);
    ctx.fillText(score.ai, canvas.width - 50, 50);
}

// Start the game
startGame();
updateGame();