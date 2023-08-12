/*
For the highlight (and text colorization too): it seems classList is not supported on old browsers for 2011,
so in the unlikely case it's not compatible with Pepper, check our TODO.md for an alternative
*/

console.log("Hello world");

function body_loaded() {
  var gameType
  const pages = document.getElementsByClassName("page");

  let boardMatrix = [];
  let boardArray = [];

  const socket = new WebSocket("ws://" + window.location.host + "/ws");

  function updateBoardReferences() {
    if (gameType === "3x") {
      socket.send("board 3")
      const boardMatrix = [
        [document.getElementById("t00"), document.getElementById("t01"), document.getElementById("t02")],
        [document.getElementById("t10"), document.getElementById("t11"), document.getElementById("t12")],
        [document.getElementById("t20"), document.getElementById("t21"), document.getElementById("t22")]
      ];

      const boardArray = [
        document.getElementById("t00"),
        document.getElementById("t01"),
        document.getElementById("t02"),
        document.getElementById("t10"),
        document.getElementById("t11"),
        document.getElementById("t12"),
        document.getElementById("t20"),
        document.getElementById("t21"),
        document.getElementById("t22")
      ];
    } else if (gameType === "4x") {
      socket.send("board 4")
      const boardMatrix = [
        [document.getElementById("tt00"), document.getElementById("tt01"), document.getElementById("tt02"), document.getElementById("tt03")],
        [document.getElementById("tt10"), document.getElementById("tt11"), document.getElementById("tt12"), document.getElementById("t13")],
        [document.getElementById("tt20"), document.getElementById("tt21"), document.getElementById("tt22"), document.getElementById("t23")],
        [document.getElementById("tt30"), document.getElementById("tt31"), document.getElementById("tt32"), document.getElementById("tt33")]
      ];

      const boardArray = [
        document.getElementById("tt00"),
        document.getElementById("tt01"),
        document.getElementById("tt02"),
        document.getElementById("tt03"),
        document.getElementById("tt10"),
        document.getElementById("tt11"),
        document.getElementById("tt12"),
        document.getElementById("tt13"),
        document.getElementById("tt20"),
        document.getElementById("tt21"),
        document.getElementById("tt22"),
        document.getElementById("tt23"),
        document.getElementById("tt30"),
        document.getElementById("tt31"),
        document.getElementById("tt32"),
        document.getElementById("tt33")
      ];
    }
  }

 

  socket.onopen = function(e) {
    console.log("[WS open] Connection established");
    // console.log("Sending to server");
    // socket.send("Hello world");
  };

  socket.onmessage = function(event) {
    const msg = event.data;
    console.log(`[WS message] Data received from server: ${msg}`);

    // check if it's an event message
    tokens = msg.split(" ");
    if (tokens[0] == "event") {
      if (tokens[1] == "user-approached") {
        document.getElementById("idle").hidden = true;
        document.getElementById("idle-approached").hidden = false;
      } else if (tokens[1] == "enter-profiling") {
        document.getElementById("idle-approached").hidden = true;
        document.getElementById("experience-select").hidden = false;
      } else if (tokens[1] == "pause-game") {
        document.getElementById("game-pause").hidden = false;
        document.getElementById("game-pause-warning").hidden = true;
        if (gameType === "3x") {
          document.getElementById("game3").hidden = true;
        } else {
          document.getElementById("game4").hidden = true;
        }
      } else if (tokens[1] == "pause-game-warning") {
        document.getElementById("game-pause-warning").hidden = false;
      } else if (tokens[1] == "resume-game") {
        document.getElementById("game-pause").hidden = true;
        if (gameType === "3x") {
          document.getElementById("game3").hidden = false;
        } else {
          document.getElementById("game4").hidden = false;
        }
      } else if (tokens[1] == "interaction-end") {
        for (let i = 0; i < pages.length; i++) {
          pages[i].hidden = true;
        }
        document.getElementById("idle").hidden = false;
      } else if (tokens[1] == "loading-start") {
        console.log("Loading Start");
        socket.send("Loading Start");
        for (let i = 0; i < pages.length; i++) {
          pages[i].hidden = true;
        }
        document.getElementById("loading").hidden = false;
      } else if (tokens[1] == "loading-complete3") {
        console.log("Loading Complete");
        document.getElementById("loading").hidden = true;
        document.getElementById("game3").hidden = false;
        document.getElementById("game4").hidden = true;
      } else if (tokens[1] == "loading-complete4") {
        console.log("Loading Complete");
        document.getElementById("loading").hidden = true;
        document.getElementById("game4").hidden = false;
        document.getElementById("game3").hidden = true;
      } else {
        console.error("[WS message] Event unrecognized.");
      }
      return;
    }

    // or it may be a highlight message
    else if (tokens[0] == "highlight") {
      let hl = tokens[1];

      if (hl.length != 9) {
        console.error("[WS message] Highlight malformed, its length is not 9");
        return;
      }

      for (let i = 0; i < hl.length; i++) {
        let c = hl[i];
        if ("Hh. ".indexOf(c) == -1) {
          console.error("[WS message] Highlight malformed, forbidden character");
        }
        c = c.replace("h", "H");
        // manage class for highlight
        if (c == "H") {
          boardArray[i].classList.add("highlight");
        } else {
          boardArray[i].classList.remove("highlight");
        }
      }

      return;
    }

    // if no recognizable prefix, it's a board message

    if (msg.length != 9) {
      console.error("[WS message] Message malformed, its length is not 9");
      return;
    }

    for (let i = 0; i < msg.length; i++) {
      let c = msg[i];
      if ("XOxo. ".indexOf(c) == -1) {
        console.error("[WS message] Message malformed, forbidden character");
      }
      c = c.replace("x", "X");
      c = c.replace("o", "O");
      c = c.replace(".", " ");
      // manage classes for text colorization
      boardArray[i].classList.remove("has-x");
      boardArray[i].classList.remove("has-o");
      if (c == "X") {
        boardArray[i].classList.add("has-x");
      }
      if (c == "O") {
        boardArray[i].classList.add("has-o");
      }
      // Cool Unicode characters. May not work with Pepper.     ×∘ ○⨯ ◯
      c = c.replace("X", "⨯");
      c = c.replace("O", "○");
      boardArray[i].innerText = c;
    }
  };

  socket.onclose = function(event) {
    if (event.wasClean) {
      console.log(`[WS close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
      // e.g. server process killed
      console.log("[WS close] Connection died");
    }
  };

  socket.onerror = function(error) {
    console.error(`[WS error] ${error.message}`);
  };

  function getExperienceClickedHandler(exp) {
    return () => {
      console.log("game_type " + exp);
      socket.send("game_type " + exp)
      document.getElementById("experience-select").hidden = true;
      if (exp === "3x") {
        gameType = "3x";
        updateBoardReferences();
        document.getElementById("game3").hidden = false;
        document.getElementById("game4").hidden = true;
      } else {
        gameType = "4x";
        updateBoardReferences();
        document.getElementById("game3").hidden = true;
        document.getElementById("game4").hidden = false;
      }
    };
  }

  //experience buttons
  const experience1Button = document.getElementById("beginner");
  const experience2Button = document.getElementById("expert");
  //function on button click
  experience1Button.onclick = getExperienceClickedHandler("3x");
  experience2Button.onclick = getExperienceClickedHandler("4x");

  function getTileClickHandler(row, col) {
    return () => {
      socket.send("click " + row + " " + col);
      console.log("click " + row + " " + col);
    };
  }

  for (let i = 0; i < boardMatrix.length; i++) {
    for (let j = 0; j < boardMatrix[i].length; j++) {
      boardMatrix[i][j].onclick = getTileClickHandler(i, j);
    }
  }
}

