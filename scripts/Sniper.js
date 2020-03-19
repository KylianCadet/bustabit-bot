var config = {
    target: { value: '', type: 'text', label: 'User to follow' },
    maxBet: { value: 1e8, type: 'balance', label: 'Max Bet' }
};


engine.on('BET_PLACED', bet => {
    if (bet.uname.toLowerCase() === config.target.value.toLowerCase()) {
        if (userInfo.balance < 100) {
            stop('Your balance is too low to bet.');
        }

        log('Spotted', bet.uname, 'betting', bet.wager / 100, 'bit(s) with a', bet.payout + 'x payout.');

        const bettableBalance = Math.floor(userInfo.balance / 100) * 100;
        const wager = Math.min(bettableBalance, bet.wager, config.maxBet.value);

        if (engine.gameState != 'GAME_STARTING') {
            // do not queue the bet if the current game is no longer accepting bets
            return;
        }

        engine.bet(wager, bet.payout); // aim at target's payout
    }
});

engine.on('CASHED_OUT', cashOut => {
    if (cashOut.uname.toLowerCase() === config.target.value.toLowerCase()) {
        log('Spotted', cashOut.uname, 'cashing out at', cashOut.cashedAt + 'x.');

        if (engine.currentlyPlaying()) {
            engine.cashOut();
        }
    }
})