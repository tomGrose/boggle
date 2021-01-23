let score = 0;
playCounter = 0;
let guessedWords = []

// Create a sixty second timer for the game
$( document ).ready(function() { setTimeout(gameEnd, 60000); });

$('form').submit( function(evt) {
    evt.preventDefault();
    getGuess();
})

// Recieve the guess, check to see if it is a duplicate. Send to server to see if it is valid
let getGuess = async function(){
    const guess = $("#guess-input").val();
    if (guessedWords.includes(guess)){
        displayResult("duplicate");
        return
    }
    guessedWords.push(guess);
    const result = await axios.get(`http://127.0.0.1:5000/guess`, {params: {user_guess: guess}});
    displayResult(result);
}

function displayResult(response){
    let resultData = response === "duplicate" ? "dupe" : response.data.result;
    let displayResult = "";

    if (resultData === "ok"){
        displayResult = "Good job!";
    } else if (resultData === "not-on-board"){
        displayResult = "Nice try!";
    } else if (resultData === "not-word"){
        displayResult = "That's not a real word!";
    } else if (resultData === "dupe"){
        displayResult = "You already guessed that!";
    }
    $('#result').text(displayResult);
    countScore(resultData)
    $('#score').text(score);
}

function countScore(result){
    if (result === "ok"){
        guess = $("#guess-input").val();
        score += guess.length;
    }
    $('#guess-form').trigger("reset");
}

async function updateStats(){
    const result = await axios.post(`http://127.0.0.1:5000/stats`, {high_score: score});
}


const gameEnd = function() {
    getGuess = function(){
        alert("You are out of time!");
        return;
    }
    gameEndUI();
    updateStats();
}

function gameEndUI() {
    $('#guess-form').toggle();
    $('#score-counter').toggle();
    $('#restart-btn').toggle();
    $('#result').text(`Game over! Your final score was: ${score}`);
}

$('#restart-btn').on("click", function(){
    location.reload();
})

