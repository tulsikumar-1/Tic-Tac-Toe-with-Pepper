/*
For the highlight (and text colorization too): it seems classList is not supported on old browsers for 2011,
so in the unlikely case it's not compatible with Pepper, check our TODO.md for an alternative
*/

console.log("Hello world");

function body_loaded() {
  
  const pages = document.getElementsByClassName("page");
  let exp1 = "3x";
  let boardMatrix = []; // Declare boardMatrix outside the function
  let board_array = []; // Declare board_array outside the function
  function updateBoardReferences() {
    if (exp1 === "3x") {
      console.log("board 3")
      boardMatrix = [
        [document.getElementById("t00"), document.getElementById("t01"), document.getElementById("t02")],
        [document.getElementById("t10"), document.getElementById("t11"), document.getElementById("t12")],
        [document.getElementById("t20"), document.getElementById("t21"), document.getElementById("t22")]
      ];

      board_array = [
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
    } else if (exp1 === "4x") {
      console.log("board 4")
      boardMatrix = [
        [document.getElementById("tt00"), document.getElementById("tt01"), document.getElementById("tt02"), document.getElementById("tt03")],
        [document.getElementById("tt10"), document.getElementById("tt11"), document.getElementById("tt12"), document.getElementById("tt13")],
        [document.getElementById("tt20"), document.getElementById("tt21"), document.getElementById("tt22"), document.getElementById("tt23")],
        [document.getElementById("tt30"), document.getElementById("tt31"), document.getElementById("tt32"), document.getElementById("tt33")]
      ];

      board_array = [
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
    for (let i = 0; i < boardMatrix.length; i++) {
      for (let j = 0; j < boardMatrix[i].length; j++) {
        boardMatrix[i][j].onclick = get_tile_click_handler(i, j);
      }
    }
  }

  
  let socket = new WebSocket("ws://" + window.location.host + "/ws");

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
       } 
      else if (tokens[1] == "show-image") {
        for (let i = 0; i < pages.length; i++) {
          pages[i].hidden = true;
        }
        document.getElementById("show-image").src="captured_image.jpg?"+1;
        document.getElementById("show-image").hidden = false;   
      } 
      else if (tokens[1] == "enter-profiling") {
        for (let i = 0; i < pages.length; i++) {
          pages[i].hidden = true;
        }
        document.getElementById("experience-select").hidden = false;
        
        
      } else if (tokens[1] == "pause-game") {
        document.getElementById("game-pause").hidden = false;
        document.getElementById("game-pause-warning").hidden = true;
        document.getElementById("game3").hidden = true;
        document.getElementById("game4").hidden = true
      }
      
       else if (tokens[1] == "pause-game-warning") {
        document.getElementById("game-pause-warning").hidden = false;
        if (exp1 === "3x") {
          document.getElementById("game3").hidden = true;
        } else {
          document.getElementById("game4").hidden = true;
        }
      } else if (tokens[1] == "resume-game") {
        document.getElementById("game-pause").hidden = true;
        if (exp1 === "3x") {
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

      if (hl.length != 9 && hl.length != 16) {
        console.error("[WS message] Highlight malformed, its length is not 9 or 16");
        return;
      }

      let matrix = boardMatrix.flat();

      for (let i = 0; i < hl.length; i++) {
        let c = hl[i];
        if ("Hh. ".indexOf(c) == -1) {
          console.error("[WS message] Highlight malformed, forbidden character");
        }
        c = c.replace("h", "H");
        // manage class for highlight
        if (c == "H") {
          matrix[i].classList.add("highlight");
        } else {
          matrix[i].classList.remove("highlight");
        }
      }

      return;
    }

    // if no recognizable prefix, it's a board message

    const boardLength = exp1 === "3x" ? 9 : 16;

    if (msg.length != boardLength) {
      console.error("[WS message] Message malformed, its length is not " + boardLength);
      return;
    }

    let matrix = boardMatrix.flat();

    for (let i = 0; i < msg.length; i++) {
      let c = msg[i];
      if ("XOxo. ".indexOf(c) == -1) {
        console.error("[WS message] Message malformed, forbidden character");
      }
      c = c.replace("x", "X");
      c = c.replace("o", "O");
      c = c.replace(".", " ");
      // manage classes for text colorization
      matrix[i].classList.remove("has-x");
      matrix[i].classList.remove("has-o");
      if (c == "X") {
        matrix[i].classList.add("has-x");
      }
      if (c == "O") {
        matrix[i].classList.add("has-o");
      }
      // Cool Unicode characters. May not work with Pepper.     ×∘ ○⨯ ◯
      c = c.replace("X", "⨯");
      c = c.replace("O", "○");
      matrix[i].innerText = c;
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

  function get_experience_clicked_handler(exp) {
    return () => {
      socket.send("game_type " + exp);
      console.log("game_type " + exp);
      document.getElementById("experience-select").hidden = true;
      exp1 = exp;
      updateBoardReferences();
      if (exp1 == "3x") {
        document.getElementById("game3").hidden = false;
      } else {
        document.getElementById("game4").hidden = false;
      }
    };
  }

  //experience buttons
  experience1_button = document.getElementById("beginner");
  experience2_button = document.getElementById("expert");
  //function on button click
  experience1_button.onclick = get_experience_clicked_handler("3x");
  experience2_button.onclick = get_experience_clicked_handler("4x");

  function get_tile_click_handler(row, col) {
    return () => {
      socket.send("click " + row + " " + col);
      console.log("click " + row + " " + col);
    };
  }

}

