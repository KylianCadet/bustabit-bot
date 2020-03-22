  var config = {
    wager: {
      value: 100,
      type: 'balance',
      label: 'Base bet'
    },
    payout: {
      value: 2,
      type: 'multiplier',
      label: 'Coeff to wait for'
    },
    // limit_script_balance: {
    //   value: 100000,
    //   type: 'balance',
    //   label: 'Maximum lose'
    // }
  };
  // https://mtihc.github.io/bustabit-script-simulator/
  let wantedProfitInBits = config.wager.value / 100;
  let netProfit = 0;
  let baseList = [];
  let currentGamesPlayed = 0;
  let maxBet = 0;
  let balanceNeeded = 0;
  let wins = 0;
  let loses = 0;
  let currentlyPlaying = true;
  let SPLIT_INTO = 3;
  var MAX_LOSE = 0;
  var SESSION_NET_PROFIT = 0;
  var SESSION_MAX_BALANCE_NEEDED = 0;
  var ALL_GAMES = [];
  var SESSION_TIMES_ENTERED = 0;
  addLast50();
  var SMALL_SESSION_NET_PROFIT = 0;
  // generateLastNGames(engine.history.first().hash, 100);

  function addLast50() {
    var LATEST_50_GAMES = engine.history.toArray();
    // logTime(`LATEST_50 length ${LATEST_50_GAMES.length}`)
    for (let i = 0; i <= LATEST_50_GAMES.length - 1; i++) {
      ALL_GAMES.unshift(LATEST_50_GAMES[i].bust);
    }
    ALL_GAMES.push(engine.history.first().bust)
    for (var i = 0; i < ALL_GAMES.length - 1; i++) {
      // logTime(`id ${i} ${ALL_GAMES[i]}`);
    }
  }

  function getLastNWinPercentage(n, targetPayout) {
    let wins = 0;
    let loses = 0;
    let elements_used = 0
    for (let i = ALL_GAMES.length - 1; i > -1 && i > ALL_GAMES.length - 1 - n; i--) {
      elements_used++;
      if (ALL_GAMES[i] < targetPayout) {
        loses++;
      } else {
        wins++;
      }
    }
    let percentage = (wins / elements_used) * 100
    logTime(`L${elements_used} wins: ${percentage} %`);
    return percentage;
  }


  initScript();


  function getCurrentBetLightGuide() {
    let currentMultiplier = 0;
    let currentBet = null;
    if (netProfit >= 0 && currentGamesPlayed > 0) {
      return currentBet;
    }
    if (baseList.length >= 2) {
      currentMultiplier = baseList[0] + baseList[baseList.length - 1];
      currentBet = (currentMultiplier * config.wager.value);
    } else if (baseList.length === 1) {
      currentMultiplier = baseList[0];
      currentBet = (currentMultiplier * config.wager.value) * 2;
    } else {
      currentMultiplier = null;
    }
    return currentBet;
  }

  function initScript() {

    logTime(`Starting in game ${engine.history.first().id}`);
    // Want to earn: ` + wantedProfitInBits + ' bits. Splliting into: ' + SPLIT_INTO);
    SESSION_TIMES_ENTERED += 1;
    // let wanted_statistics = [800, 700, 600, 500, 400, 300, 200, 150, 100, 50, 40, 30, 20, 10];
    // wanted_statistics.forEach(function (element) {
    //   getLastNWinPercentage(element, 2);
    // })
    logTime('------------------------------------------------')
    // TO DO: Uncomment
    // for (let i = 1; i <= SPLIT_INTO; i++) {
    //   baseList.push(Math.round(wantedProfitInBits / SPLIT_INTO) * 100)
    // }
    baseList = [1, 2, 3];
    netProfit = 0;
    currentGamesPlayed = 0;
    maxBet = 0;
    balanceNeeded = 0;
    wins = 0;
    loses = 0;
    currentlyPlaying = true;
    SMALL_SESSION_NET_PROFIT = 0;
  }

  // Try to bet immediately when script starts
  if (engine.gameState === "GAME_STARTING") {
    makeBet();
  }

  engine.on('GAME_STARTING', onGameStarted);
  engine.on('GAME_ENDED', onGameEnded);

  function onGameStarted() {
    if (!currentlyPlaying) {
      initScript();
    }
    let currentBet = getCurrentBetLightGuide();

    if (!currentBet) {
      currentlyPlaying = false;
      printEndStatus();
      // engine.on('GAME_STARTING', function(){});
      initScript();
    }
    makeBet();
  }

  function onGameEnded() {
    ALL_GAMES.push(engine.history.first().bust);
    let lastGame = engine.history.first();
    // If we wagered, it means we played
    if (!lastGame.wager) {
      return;
    }
    let lastBet = getCurrentBetLightGuide();

    if (lastGame.cashedAt) {
      let profit = Math.round(((lastBet * config.payout.value) - lastBet) / 100);
      netProfit += profit;
      SESSION_NET_PROFIT += profit;
      SMALL_SESSION_NET_PROFIT += profit
      logTime(`Won ${profit} bits`);
      if (baseList.length > 1) {
        baseList.splice(baseList.length - 1, 1);
      }
      baseList.splice(0, 1);
      wins += 1;
    } else {
      var lost = lastBet / 100;
      logTime(`Lost ${lost} bits`);
      netProfit -= lost;
      SESSION_NET_PROFIT -= lost;
      baseList.push(lastBet / config.wager.value);
      loses += 1;
    }
    currentGamesPlayed += 1;
    // logTime(`Net profit: ${netProfit} Current bet: ${getCurrentBetLightGuide() / 100}`);
    let currentBalanceNeeded = netProfit + ((getCurrentBetLightGuide() / 100) * -1);
    if (currentBalanceNeeded < balanceNeeded) {
      balanceNeeded = currentBalanceNeeded;
    }

    if (currentBalanceNeeded < SESSION_MAX_BALANCE_NEEDED) {
      SESSION_MAX_BALANCE_NEEDED = currentBalanceNeeded;
    }

    logTime('Net profit: ' + netProfit + ' bits. Left to play: ' + baseList.length);
  }

  function printEndStatus() {
    logTime(`Game ended id: ${engine.history.first().id}. Played: ` + currentGamesPlayed + ' Net profit: ' + netProfit + ' bits. Balance needed: ' + balanceNeeded * -1 + ' bits Max bet: ' + maxBet / 100 + ' bits. Wins: ' + (wins / (wins + loses) * 100) + ' % Loses: ' + (loses / (wins + loses) * 100) + ' %');
    logTime(`SESSION NET PROFIT ${SESSION_NET_PROFIT} bits, SESSION MAX BALANCE NEEDED ${SESSION_MAX_BALANCE_NEEDED} bits, SESSION TIMES ENTERED ${SESSION_TIMES_ENTERED}`)
  }

  function makeBet() {
    let currentBet = getCurrentBetLightGuide();
    if (!currentBet) {
      printEndStatus();
      return;
    }
    engine.bet(currentBet, config.payout.value);
    if (currentBet > maxBet) {
      maxBet = currentBet;
    }
    logTime('betting ' + Math.round(currentBet / 100) + ' on ' + config.payout.value + ' x');
  }

  function logTime(msg) {
    let today = new Date();
    let calendarDate = `${today.getDate()}-${today.getMonth() + 1}-${today.getFullYear()}`;
    let now = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
    log(`${now} ${msg}`);
  }