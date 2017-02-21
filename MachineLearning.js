"use strict";

var threshold = 100;

function ScorePredictor(teamA, teamB) {
    var sumA = teamA.reduce(function (a, b) {
        return a + b;
    }, 0);
    var sumB = teamB.reduce(function (a, b) {
        return a + b;
    }, 0);
    var avgA = sumA / teamA.length;
    var avgB = sumB / teamB.length;
    var avg_diff = Math.abs(avgA - avgB);
    if (avg_diff < 0.27) {
        return 0;
    }

    avg_diff = avg_diff * 2;
    if (avg_diff < 1.5 && avg_diff > 1.75) {
        avg_diff = 1.4;
    }
    var score_diff = Math.round(avg_diff);
    if (avgA > avgB) {
        return score_diff;
    } else {
        return (0 - score_diff);
    }
}

function CalculateAdjustment(teamA, teamB, score_diff_a) {
    var score_diff_c = ScorePredictor(teamA, teamB);
    var adjustment = (score_diff_a - score_diff_c) / 7;
    return adjustment;
}

function ErrorPerGame(game_instances, player_rating) {
    var total_err = 0;
    var curr_instance;
    var PID;
    for (var i = 0; i < game_instances.length; i++) {
        curr_instance = game_instances[i];
        var teamA = [];
        var teamB = [];
        for (var j = 0; j < curr_instance.TeamA.length; j++) {
            PID = curr_instance.TeamA[j];
            teamA.push(player_rating[PID].rating);
        }
        for (var k = 0; k < curr_instance.TeamB.length; k++) {
            PID = curr_instance.TeamB[k];
            teamB.push(player_rating[PID].rating);
        }
        var SD_act = Math.abs(curr_instance.ScoreA - curr_instance.ScoreB);
        var SD_cal = Math.abs(ScorePredictor(teamA, teamB));
        total_err += Math.abs(SD_act - SD_cal);
    }
    var output = "Total Error:" + total_err + "\nPlayerRatings:";
    for (var aaa in player_rating) {
        if (player_rating.hasOwnProperty(aaa)) {
            output += aaa + " " + player_rating[aaa].rating + ", ";
        }
    }
    console.log(output);
    return total_err / i;
}

function Rescale(old_ratings)
{
    // 1: Rescale
    var tmp1 = [];
    var max1 = Math.max.apply(null, old_ratings);
    var min1 = Math.min.apply(null, old_ratings);
    var diff1 = max1 - min1;
    var i;
    if (diff1 > 10) {
        for (i = 0; i < old_ratings.length; i++) {
            tmp1.push(old_ratings[i] * 10 / diff1);
        }
    }
    else {
        tmp1 = old_ratings;
    }

    // 2: Re-centre to 5
    var tmp2 = [];
    var sum = tmp1.reduce(function (a, b) {
        return a + b;
    }, 0);
    var avg = sum / tmp1.length;
    var diff2 = avg - 5;
    var j;
    for (j = 0; j < tmp1.length; j++) {
        tmp2.push(tmp1[j] - diff2);
    }

    // 3: shift to fit within 0 to 10
    var new_ratings = [];
    var max3 = Math.max.apply(null, tmp2);
    var min3 = Math.min.apply(null, tmp2);
    var diff3;
    var k;
    if (max3 > 10) {
        diff3 = max3 - 10;
        for (k = 0; k < tmp2.length; k++) {
            new_ratings.push(Math.round((tmp2[k] - diff3) * 10) / 10);
        }
    }
    else if (min3 < 0) {
        diff3 = 0 - min3;
        for (k = 0; k < tmp2.length; k++) {
            new_ratings.push(Math.round((tmp2[k] + diff3) * 10) / 10);
        }
    }
    else {
        for (k = 0; k < tmp2.length; k++) {
            new_ratings.push(Math.round(tmp2[k] * 10) / 10);
        }
    }

    return new_ratings;
}

function CloneOrUpdate(sourceObj) {
    var target = {};
    for (var PID in sourceObj) {
        if (target.hasOwnProperty(PID) === false) {
            target[PID] = {rating: sourceObj[PID].rating};
        } else {
            target[PID].rating = sourceObj[PID].rating;
        }
    }
    return target;
}

function InferRatings(ratings_prev, game_instances) {
    var optimal_set = { min_error: 1000000000, player_ratings: {} };
    var keep_running = true;
    var iteration = 0;
    var PlayerRatings = CloneOrUpdate(ratings_prev);
    var PlayerRatings_prev = {};
    var PID;

    while (keep_running) {
        var rating_table = {};
        for (var i = 0; i < game_instances.length; i++) {
            var curr_instance = game_instances[i];

            var teamA = [];
            for (var j = 0; j < curr_instance.TeamA.length; j++) {
                PID = curr_instance.TeamA[j];
                if (PlayerRatings.hasOwnProperty(PID) === false) {
                    PlayerRatings[PID] = { rating: 5 };
                }
                if (rating_table.hasOwnProperty(PID) === false) {
                    rating_table[PID] = { sum: 0, counter: 0 };
                }
                teamA.push(PlayerRatings[PID].rating);
            }

            var teamB = [];
            for (var k = 0; k < curr_instance.TeamB.length; k++) {
                PID = curr_instance.TeamB[k];
                if (PlayerRatings.hasOwnProperty(PID) === false) {
                    PlayerRatings[PID] = { rating: 5 };
                }
                if (rating_table.hasOwnProperty(PID) === false) {
                    rating_table[PID] = { sum: 0, counter: 0 };
                }
                teamB.push(PlayerRatings[PID].rating);
            }

            var adj = CalculateAdjustment(teamA, teamB, (curr_instance.ScoreA - curr_instance.ScoreB));
            for (var j = 0; j < curr_instance.TeamA.length; j++) {
                PID = curr_instance.TeamA[j];
                rating_table[PID].sum += PlayerRatings[PID].rating + adj;
                rating_table[PID].counter += 1;
            }
            for (var k = 0; k < curr_instance.TeamB.length; k++) {
                PID = curr_instance.TeamB[k];
                rating_table[PID].sum += PlayerRatings[PID].rating - adj;
                rating_table[PID].counter += 1;
            }
        }

        var arr = [];
        for (PID in rating_table) {
            if (rating_table.hasOwnProperty(PID)) {
                var tmp_rating = rating_table[PID].sum / rating_table[PID].counter;
                arr.push(tmp_rating);
            }
        }
        var new_arr = Rescale(arr);
        var index = 0;
        for (PID in rating_table) {
            if (rating_table.hasOwnProperty(PID)) {
                PlayerRatings[PID].rating = new_arr[index];
                index++;
            }
        }
        var error_per_game = ErrorPerGame(game_instances, PlayerRatings);
        if (error_per_game <= optimal_set.min_error) {
            optimal_set.min_error = error_per_game;
            optimal_set.player_ratings = CloneOrUpdate(PlayerRatings);
        }

        var still_updating = false;
        for (PID in PlayerRatings) {
            if (PlayerRatings_prev.hasOwnProperty(PID) === false) {
                still_updating = true;
                break;
            }
            if (PlayerRatings[PID].rating != PlayerRatings_prev[PID].rating) {
                still_updating = true;
                break;
            }
        }
        if (still_updating === false) {
            console.log("converges");
            keep_running = false;
        } else if (optimal_set.min_error === 0) {
            console.log("0 error");
            keep_running = false;
        } else if (iteration === threshold) {
            console.log("threshold");
            keep_running = false;
        }

        iteration += 1;
        PlayerRatings_prev = CloneOrUpdate(PlayerRatings);
    }
    return optimal_set.player_ratings;
}



// SIMULATION

class GameInstance {
    constructor(gameID, teamA, teamB, scoreA, scoreB) {
        this.GameID = gameID;
        this.TeamA = teamA;
        this.TeamB = teamB;
        this.ScoreA = scoreA;
        this.ScoreB = scoreB;
    }
}

function simulation() {
/*    const g1 = new GameInstance(1, ["Jonathan5", "Jessica10", "Joeseph9", "Max14", "John4", "Tom11"], ["Martin16", "Khoman6", "Joeseph9", "Jeffrey1", "Ryan18", "Sherman12", "Vivien3"], 0, 1);
    
    const g2 = new GameInstance(2, ["Max14", "Marcus17", "John4", "Frank8", "Michael7", "Jose15", "Chris20"], ["Martin16", "Khoman6", "Joeseph9", "Jeffrey1", "Ryan18", "Sherman12", "Vivien3"], 0, 1);
    const g3 = new GameInstance(3, ["Marcus17", "Ryan18", "Vivien3", "Max14"], ["Tom11", "Sherman12", "John4", "Frank8"], 0, 0);
    const g4 = new GameInstance(4, ["Marcus17", "Ryan18", "Vivien3", "Max14"], ["Tom11", "Sherman12", "John4", "Frank8"], 0, 0);
    const g5 = new GameInstance(5, ["Jeffrey1", "Michael7", "Sherman12", "Tom11", "Danny19"], ["Jose15", "Max14", "Alex2", "Ryan18", "Joeseph9"], 0, 0);
    const g6 = new GameInstance(6, ["Jeffrey1", "Michael7", "Sherman12", "Tom11", "Danny19"], ["Jose15", "Max14", "Alex2", "Ryan18", "Joeseph9"], 1, 0);
    const g7 = new GameInstance(7, ["Jessica10", "Frank8", "Jose15", "Danny19"], ["Alex2", "Tom11", "Sherman12", "Jonathan5"], 6, 0);
    const g8 = new GameInstance(8, ["Jessica10", "Frank8", "Jose15", "Danny19"], ["Alex2", "Tom11", "Sherman12", "Jonathan5"], 7, 0);
    const g9 = new GameInstance(9, ["Joeseph9", "John4", "Jose15", "Sherman12", "Ryan18", "Vivien3"], ["Jessica10", "Martin16", "Max14", "Marcus17", "Jonathan5", "Chris20"], 2, 0);
    const g10 = new GameInstance(10, ["Joeseph9", "John4", "Jose15", "Sherman12", "Ryan18", "Vivien3"], ["Jessica10", "Martin16", "Max14", "Marcus17", "Jonathan5", "Chris20"], 1, 0);
    const g11 = new GameInstance(11, ["Sherman12", "Khoman6", "John4", "Michael7", "Alex2", "Tom11", "Ryan18", "Jose15"], ["Jonathan5", "Jeffrey1", "Danny19", "Chris20", "Karen13", "Max14", "Frank8", "Martin16"], 0, 5);
    const g12 = new GameInstance(12, ["Sherman12", "Khoman6", "John4", "Michael7", "Alex2", "Tom11", "Ryan18", "Jose15"], ["Jonathan5", "Jeffrey1", "Danny19", "Chris20", "Karen13", "Max14", "Frank8", "Martin16"], 0, 3);
    const g13 = new GameInstance(13, ["Marcus17", "Sherman12", "Frank8", "Martin16"], ["Max14", "Ryan18", "Karen13", "Danny19"], 0, 3);
    const g14 = new GameInstance(14, ["Marcus17", "Sherman12", "Frank8", "Martin16"], ["Max14", "Ryan18", "Karen13", "Danny19"], 0, 1);
    const g15 = new GameInstance(15, ["Jonathan5", "Max14", "Ryan18", "Joeseph9", "Jeffrey1"], ["Karen13", "Sherman12", "Frank8", "Martin16", "Michael7"], 0, 0);
    const g16 = new GameInstance(16, ["Jonathan5", "Max14", "Ryan18", "Joeseph9", "Jeffrey1"], ["Karen13", "Sherman12", "Frank8", "Martin16", "Michael7"], 0, 1);
    const g17 = new GameInstance(17, ["Khoman6", "Jonathan5", "Jose15", "Jeffrey1", "Marcus17", "Vivien3", "John4"], ["Chris20", "Karen13", "Frank8", "Joeseph9", "Alex2", "Tom11", "Jessica10"], 4, 0);
   const g18 = new GameInstance(18, ["Khoman6", "Jonathan5", "Jose15", "Jeffrey1", "Marcus17", "Vivien3", "John4"], ["Chris20", "Karen13", "Frank8", "Joeseph9", "Alex2", "Tom11", "Jessica10"], 2, 0);
    const g19 = new GameInstance(19, ["Martin16", "Jonathan5", "Ryan18", "Alex2"], ["Khoman6", "Sherman12", "Jessica10", "Tom11"], 0, 0);
    const g20 = new GameInstance(20, ["Martin16", "Jonathan5", "Ryan18", "Alex2"], ["Khoman6", "Sherman12", "Jessica10", "Tom11"], 1, 0);
    var game_instances = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19, g20];
*/
    const g24 = new GameInstance(24, ["Frank8", "Ryan18", "Martin16", "Karen13", "Tom11"], ["Jose15", "Marcus17", "Danny19", "Jessica10", "Michael7"], 0, 2);
    const g34 = new GameInstance(34, ["Jose15", "Ryan18", "Vivien3", "Jeffrey1", "Karen13", "Jonathan5", "Tom11"], ["Marcus17", "Chris20", "Khoman6", "Michael7", "Max14", "Danny19"], 7, 1);
    var game_instances = [g24, g34];

    var player_ratings = InferRatings({}, game_instances);

    var output = "\n\n\n";
    for (var PID in player_ratings) {
        if (player_ratings.hasOwnProperty(PID)) {
            output += PID + " " + player_ratings[PID].rating + "\n";
        }
    }
    console.log(output);
}

simulation();
