// Define AI's paddle speed
var aiSpeed = 2;

// Define AI's error rate
var aiError = 0.05;

/**
 * Function to make a decision on the direction to move the AI paddle based on the ball's position and the error factor.
 * @param {object} ball - The ball object
 * @param {object} aiPaddle - The AI paddle object
 */
function aiDecision(ball, aiPaddle) {
    // If ball is above the AI paddle and random number is greater than error rate, move the paddle up
    if (ball.y < aiPaddle.y && Math.random() > aiError) {
        aiPaddle.y -= aiSpeed;
    }

    // If ball is below the AI paddle and random number is greater than error rate, move the paddle down
    else if (ball.y > aiPaddle.y && Math.random() > aiError) {
        aiPaddle.y += aiSpeed;
    }
}
