// This is the Flat bet script from the bustabit site
// Replace this file by your own bot

var config = {
  wager: {
    value: 100, type: 'balance', label: 'wager'
  },
  payout: {
    value: 2, type: 'multiplier', label: 'payout' }
};

// Try to bet immediately when script starts
if (engine.gameState === "GAME_STARTING") {
  makeBet();
}

engine.on('GAME_STARTING', onGameStarted);
engine.on('GAME_ENDED', onGameEnded);

function onGameStarted() {
  makeBet();
}

function onGameEnded() {
  var lastGame = engine.history.first();

  // If we wagered, it means we played
  if (!lastGame.wager) {
    return;
  }

  if (lastGame.cashedAt) {
    var profit = Math.round((config.wager.value * config.payout.value - config.wager.value) / 100)
    log('we won', profit, 'bits');
  } else {
    log('we lost', Math.round(config.wager.value / 100), 'bits');
  }
}

function makeBet() {
  engine.bet(config.wager.value, config.payout.value);
  log('betting', Math.round(config.wager.value / 100), 'on', config.payout.value, 'x');
}