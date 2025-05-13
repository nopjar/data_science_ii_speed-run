import leaderboard
import top_players


def main():
    leaderboard_data = leaderboard.main()
    top3 = leaderboard_data['data'][leaderboard_data['data']['#'].isin([1, 2, 3])]

    player_ids = top3['Player-ID'].tolist()
    top_data = top_players.main(player_ids)

    res = [leaderboard_data]
    res.extend(top_data)
    return res
