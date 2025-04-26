

"""
> 5* current pity
> 4* current pity
> list of 5 stars:
    - featured (char)
    - standard (char
> list of 4 stars:
    - featured (char)
    - standard (char + lc)
> list of 3 stars: light cone
> isGuaranteed 4 star
> isGuaranteed 5 star

retval:
> 5* after pity
> 4* after pity
> isGuaranteed 4 star
> isGuaranteed 5 star
> outcome

TODO: add rng according to UID
"""

import random

CHANCE_FIVE_STAR = 0.6
CHANCE_FOUR_STAR = 5.1
HARD_PITY_FIVE_STAR = 90
HARD_PITY_FOUR_STAR = 10
SOFT_PITY = 74

std_three = ['3*']
std_five = ['Himeko', 'Bronya', 'Clara', 'Welt', 'Gepard', 'Bailu', 'Yanqing', 'Seele', 'Blade', 'Fu Xuan']
std_four = ['STD 4 STAR']

def gacha(
    curr_four_pity: int = 0,
    curr_five_pity: int = 0,
    four_stars = None,
    five_star = '',
    is_four_guaranteed: bool = False,
    is_five_guaranteed: bool = False
):
    """
    :param curr_four_pity: Current 5-star pity
    :param curr_five_pity: Current 4-star pity
    :param four_stars: featured 4 stars in list
    :param five_star: featured 5 star
    :param is_four_guaranteed: if user is on 50/50 (4 star)
    :param is_five_guaranteed: if user is on 50/50 (5 star)
    :return:
    """
    if four_stars is None:
        four_stars = ['A', 'B', 'C']
    if five_star is None:
        five_star = 'X'

    outcome = None
    post_four_pity = curr_four_pity
    post_five_pity = curr_five_pity

    five_chance = 6 if curr_five_pity < 74 else ((curr_five_pity - 73) * 62.5) # chance gradually increases past SOFT PITY
    four_chance = 51 if curr_four_pity != 10 else 1001 # guarantee or bust

    # pull
    is_five = random.randint(1, 1000) <= five_chance

    # User rolls a 5 star
    if is_five:
        post_five_pity = 1
        if is_five_guaranteed:
            outcome = five_star
            is_five_guaranteed = False
        else:
            # Do 50/50 for 5-star if not guaranteed
            is_five_win = random.randint(1, 100) < 51
            if is_five_win:
                outcome = five_star
                is_five_guaranteed = False
            else:
                outcome = std_five[random.randint(0, len(std_five) - 1)]
                is_five_guaranteed = True

    # User does NOT roll a 5-star
    else:
        post_five_pity += 1 # increments 5-star pity
        is_four = random.randint(1, 1000) <= four_chance # check if user rolls a 4-star

        # user rolls a 4-star
        if is_four:
            post_four_pity = 1 # resets 4-star pity
            if is_four_guaranteed:
                outcome = four_stars[random.randint(0, 2)]
                is_four_guaranteed = False
            else:
                # Do 50/50 for 4-star if not guaranteed
                is_four_win = random.randint(1, 100) < 51
                if is_four_win:
                    outcome = four_stars[random.randint(0, 2)]
                    is_four_guaranteed = False
                else:
                    outcome = std_four[random.randint(0, len(std_four) - 1)]
                    is_four_guaranteed = True

        # user does NOT roll a 4-star either, resorts to 3-star
        else:
            post_four_pity += 1 # increments 4-star pity
            outcome = std_three[random.randint(0, len(std_three) - 1)] # choose a random 3-star LC

    return [outcome, post_four_pity, post_five_pity, is_four_guaranteed, is_five_guaranteed]



four_pity = 0
five_pity = 0
four_guaranteed = False
five_guaranteed = False


for i in range(100):
    p = gacha(four_pity, five_pity, ['Pela', 'Lynx', 'Gallagher'], 'Castorice', four_guaranteed, five_guaranteed)

    four_pity, five_pity = p[1], p[2]
    four_guaranteed, five_guaranteed = p[3], p[4]

    print(f'PULL #{i+1}: {p[0]} | [4* {p[1]}/10 | 5* {p[2]}/90]')

    # {'GUARANTEED' if p[3] else 'ON 50/50'}{'GUARANTEED' if p[4] else 'ON 50/50'}







