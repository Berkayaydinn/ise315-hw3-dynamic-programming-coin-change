import time


def greedy_largest_first(my_coins, money_needed):
    """
    My greedy approach: I always take the biggest coin that still fits.
    This is simple but it does not always give the best answer.
    """

    # I sort coins from big to small so I can try the largest one first
    coins_big_to_small = sorted(my_coins, reverse=True)

    remaining_money = money_needed
    greedy_result = []

    for one_coin in coins_big_to_small:
        # I keep using the same coin while it still fits
        while remaining_money >= one_coin:
            greedy_result.append(one_coin)
            remaining_money -= one_coin  # I subtract because I used this coin

    return greedy_result


def dp_min_coins_and_list(my_coins, money_needed):
    """
    My dynamic Programming solution.
    I calculate the minimum number of coins and also store which coins I used.
    """

    # I sort coins so I can stop early when coin value is too big
    coins_small_to_big = sorted(my_coins)

    # I use a very large number to represent impossible states
    # I thought it like a macro in C programmin language that is why it is upper case
    BIG_NUMBER = 10**9

    # min_coins[v] = minimum number of coins needed to make value v
    min_coins = [BIG_NUMBER] * (money_needed + 1)
    min_coins[0] = 0  # I know this because 0 money needs 0 coins

    # last_used[v] = which coin I used last to reach value v
    last_used = [-1] * (money_needed + 1)

    # I fill the DP table from 1 up to the target value
    for current_money in range(1, money_needed + 1):

        best_choice = BIG_NUMBER
        coin_i_used = -1

        # I try every coin as the last coin
        for one_coin in coins_small_to_big:
            if one_coin > current_money:
                break  # I stop because coins are sorted

            # I skip if the previous value was impossible
            if min_coins[current_money - one_coin] == BIG_NUMBER:
                continue

            # I add 1 coin because I am using one_coin now
            test_value = min_coins[current_money - one_coin] + 1

            # I keep the best (smallest) result
            if test_value < best_choice:
                best_choice = test_value
                coin_i_used = one_coin

        min_coins[current_money] = best_choice
        last_used[current_money] = coin_i_used

    # If still impossible, I return empty
    if min_coins[money_needed] == BIG_NUMBER:
        return None, []

    # Step 4: I rebuild the actual coin list by walking backwards
    final_coins = []
    walking_value = money_needed

    while walking_value > 0:
        chosen_coin = last_used[walking_value]
        if chosen_coin == -1:
            return None, []  # safety check

        final_coins.append(chosen_coin)
        walking_value -= chosen_coin  # I move to the previous value

    return min_coins[money_needed], final_coins


def run_test(my_coins, money_needed):
    greedy_answer = greedy_largest_first(my_coins, money_needed)
    dp_count, dp_answer = dp_min_coins_and_list(my_coins, money_needed)

    print("Coin set:", my_coins, "| Target:", money_needed)
    print("Greedy result:", greedy_answer, "->", len(greedy_answer), "coins")
    print("DP result:    ", dp_answer, "->", dp_count, "coins")
    print("-" * 60)


def runtime_test(my_coins, money_needed):
    # I use time.time() to measure how long DP takes
    start_time = time.time()
    dp_count, _ = dp_min_coins_and_list(my_coins, money_needed)
    end_time = time.time()

    print("Runtime test")
    print("Coin set:", my_coins)
    print("Target value:", money_needed)
    print("DP min coins:", dp_count)
    print("Time in seconds:", end_time - start_time)
    print("-" * 60)


if __name__ == "__main__":
    # These are non-canonical coin systems where greedy fails

    run_test([10, 6, 1], 12)
    run_test([1, 10, 25], 30)
    run_test([1, 3, 4], 6)

    # Big value test for runtime
    runtime_test([10, 6, 1], 10_000)
