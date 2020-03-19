var config = {
    languages: {
        value: 'en', type: 'radio', label: 'Speech language',
        options: {
            en: { value: 'en-US', type: 'noop', label: 'English' },
            fr: { value: 'fr-FR', type: 'noop', label: 'Français' },
            es: { value: 'es-ES', type: 'noop', label: 'Español' },
        }
    },
    sayGameStarting: { value: false, type: 'checkbox', label: 'narrate GAME_STARTING events?' },
    sayGameStarted: { value: true, type: 'checkbox', label: 'narrate GAME_STARTED events?' },
    sayGameEnded: { value: true, type: 'checkbox', label: 'narrate GAME_ENDED events?' },
    sayBetPlaced: { value: true, type: 'checkbox', label: 'narrate own BET_PLACED events?' },
    sayCashedOut: { value: true, type: 'checkbox', label: 'narrate own CASHED_OUT events?' },
    sayGameTick: { value: true, type: 'checkbox', label: 'narrate GAME_TICK events?' },
    otherUsers: { value: "", type: 'text', label: 'Other users (comma separated)', optional: true },
    sayOtherBets: { value: false, type: 'checkbox', label: "narrate other users' bets?" },
    sayOtherCashOuts: { value: true, type: 'checkbox', label: "narrate other users' cash-outs?" },
};

// The speech's priority
const LOW_PRIORITY = 0,
    MEDIUM_PRIORITY = 1,
    HIGH_PRIORITY = 2;

// The speech's speed
const NORMAL_RATE = 1.1,
    FAST_RATE = 1.3;

var previousPriority = 0;
var previousTick = 0;
var previousSpeech = "";
var otherUsers = [];

// Game events

engine.on('GAME_STARTING', () => {
    if (!config.sayGameStarting.value) return;
    say("game starting", LOW_PRIORITY)
});

engine.on('GAME_STARTED', () => {
    if (!config.sayGameStarted.value) return;
    say("game started", HIGH_PRIORITY);
});

engine.on('GAME_ENDED', () => {
    if (!config.sayGameEnded.value) return;
    say("busted at " + previousTick, HIGH_PRIORITY);
});

engine.on('BET_PLACED', bet => {
    if (!config.sayBetPlaced.value) return;
    if (bet.uname === userInfo.uname) {
        say("bet " + bet.wager / 100 + " bits", MEDIUM_PRIORITY);
    }

    // do not mark others' bets as prioritary so that we can hear ours!
    if (shouldSayBet(bet.uname)) {
        say(bet.uname + " bet " + bet.wager / 100 + " bits", LOW_PRIORITY);
    }
});

engine.on('CASHED_OUT', cashOut => {
    if (!config.sayCashedOut.value) return;
    if (cashOut.uname === userInfo.uname) {
        say("cashed out at " + cashOut.cashedAt, HIGH_PRIORITY);
    }

    // mark others' cash-outs as medium priority so that we can hear ours!
    if (shouldSayCashOut(cashOut.uname)) {
        say(cashOut.uname + "cashed out at " + cashOut.cashedAt, MEDIUM_PRIORITY);
    }
});

engine.on('GAME_TICK', tick => {
    previousTick = tick;
    if (!config.sayGameTick.value) return;

    let amount = '';
    let speed = 0;
    // adjust decimals and speed according to multiplier
    switch (true) {
        case (tick <= 10):
            amount = tick.toFixed(1);
            speed = NORMAL_RATE;
            break;
        case (tick <= 100):
            amount = tick.toFixed();
            speed = NORMAL_RATE;
        case (tick <= 1000):
            amount = tick.toFixed();
            speed = FAST_RATE;
            break;
        case (tick <= 10000):
            amount = Math.round(tick / 100) * 100;
            speed = FAST_RATE;
            break;
        default:
            amount = Math.round(tick / 1000) * 1000;
            speed = FAST_RATE;
    }

    if (previousSpeech !== amount) {
        say(amount, LOW_PRIORITY, speed);
    }

    // do not say the same number twice
    previousSpeech = amount;
});

/**
 * say() uses the Web Speech API to add speech synthesis to the script:
 * https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis
 */
const say = (speech, priority, speed = NORMAL_RATE) => {
    if (typeof speechSynthesis === 'undefined') {
        log("Your browser does not support speech synthesis :(")
        return;
    }

    if (speechSynthesis.speaking) {
        if (priority === LOW_PRIORITY || priority < previousPriority) {
            return;
        }
        // stop any lower priority ongoing speech
        speechSynthesis.cancel();
    }
    previousPriority = priority;

    var utterance = new SpeechSynthesisUtterance();
    utterance.lang = config.languages.value;
    utterance.rate = speed;
    utterance.text = speech;
    speechSynthesis.speak(utterance);
};

const shouldSayBet = uname => {
    return config.sayOtherBets.value && otherUsers.indexOf(uname) > -1;
}

const shouldSayCashOut = uname => {
    return config.sayOtherCashOuts.value && otherUsers.indexOf(uname) > -1;
}

(function convertUsersToArray(users) {
    if (typeof users === 'string') {
        if (users.indexOf(',') !== -1) {
            otherUsers = users.split(',');
            otherUsers.forEach(function (v, i) {
                otherUsers[i] = v.replace(/\s/g, '');
            });
        } else {
            otherUsers.push(users);
        }
    }
})(config.otherUsers.value);