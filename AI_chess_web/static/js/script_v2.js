document.addEventListener('DOMContentLoaded', function() {
    const chessboard = document.getElementById('new-chessboard');
    const statusDiv = document.getElementById('status');
    let gameId = null;

    function createBoard(fen) {
        chessboard.innerHTML = '';
        let isWhite = true;
        const rows = fen.split(' ')[0].split('/');
        for (let row of rows) {
            const tr = document.createElement('tr');
            for (let char of row) {
                if (!isNaN(char)) {
                    for (let i = 0; i < parseInt(char); i++) {
                        const td = document.createElement('td');
                        td.classList.add(isWhite ? 'white' : 'black');
                        tr.appendChild(td);
                        isWhite = !isWhite;
                    }
                } else {
                    const td = document.createElement('td');
                    td.classList.add(isWhite ? 'white' : 'black');
                    td.textContent = char;
                    tr.appendChild(td);
                    isWhite = !isWhite;
                }
            }
            isWhite = !isWhite;
            chessboard.appendChild(tr);
        }
    }

    function startNewGame() {
        fetch('http://localhost:8000/api/game/start/')
            .then(response => response.json())
            .then(data => {
                gameId = data.game_id;
                createBoard(data.fen);
                statusDiv.textContent = `Turn: ${data.turn === 'w' ? 'White' : 'Black'}`;
            });
    }

    document.getElementById('new-game').addEventListener('click', startNewGame);
    startNewGame();
});
