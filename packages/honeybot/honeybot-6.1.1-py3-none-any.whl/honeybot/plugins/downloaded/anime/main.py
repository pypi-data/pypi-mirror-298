"""
[anime.py]
Anime Plugin

[Author]
Christos Kontos

[About]
This plugin provides detailed information about anime from the top 100 list.
Users can query anime based on rank to get information like name, score, release date, and ranking.

[Commands]
>>> .anime rank <<ranking>> <<info_type>>
Returns the anime information based on rank (1 to 100) and the requested info type (name, score, release_date, ranking).
>>> .anime rank <<ranking>> all
Returns all details (name, score, release date, and ranking) of the anime at the specified rank.
"""

top_anime_data = [
    {'title': 'Sousou no Frieren', 'score': 9.33, 'aired': {'from': 'Sep 2023'}},
    {'title': 'Fullmetal Alchemist: Brotherhood', 'score': 9.09, 'aired': {'from': 'Apr 2009'}},
    {'title': 'Steins;Gate', 'score': 9.07, 'aired': {'from': 'Apr 2011'}},
    {'title': 'Gintama°', 'score': 9.06, 'aired': {'from': 'Apr 2015'}},
    {'title': 'Shingeki no Kyojin Season 3 Part 2', 'score': 9.05, 'aired': {'from': 'Apr 2019'}},
    {'title': 'Monogatari Series: Off & Monster Season', 'score': 9.04, 'aired': {'from': 'Jul 2024'}},
    {'title': 'Gintama: The Final', 'score': 9.04, 'aired': {'from': 'Jan 2021'}},
    {'title': "Gintama'", 'score': 9.03, 'aired': {'from': 'Apr 2011'}},
    {'title': 'Hunter x Hunter (2011)', 'score': 9.03, 'aired': {'from': 'Oct 2011'}},
    {'title': 'Ginga Eiyuu Densetsu', 'score': 9.02, 'aired': {'from': 'Jan 1988'}},
    {'title': "Gintama': Enchousen", 'score': 9.02, 'aired': {'from': 'Oct 2012'}},
    {'title': 'Bleach: Sennen Kessen-hen', 'score': 9.01, 'aired': {'from': 'Oct 2022'}},
    {'title': 'Kaguya-sama wa Kokurasetai: Ultra Romantic', 'score': 9.0, 'aired': {'from': 'Apr 2022'}},
    {'title': 'Gintama.', 'score': 8.98, 'aired': {'from': 'Jan 2017'}},
    {'title': 'Fruits Basket: The Final', 'score': 8.97, 'aired': {'from': 'Apr 2021'}},
    {'title': 'Clannad: After Story', 'score': 8.93, 'aired': {'from': 'Oct 2008'}},
    {'title': 'Gintama', 'score': 8.93, 'aired': {'from': 'Apr 2006'}},
    {'title': 'Koe no Katachi', 'score': 8.93, 'aired': {'from': 'Sep 2016'}},
    {'title': '3-gatsu no Lion 2nd Season', 'score': 8.91, 'aired': {'from': 'Oct 2017'}},
    {'title': 'Code Geass: Hangyaku no Lelouch R2', 'score': 8.91, 'aired': {'from': 'Apr 2008'}},
    {'title': 'Gintama Movie 2: Kanketsu-hen - Yorozuya yo Eien Nare', 'score': 8.9, 'aired': {'from': 'Jul 2013'}},
    {'title': 'Kusuriya no Hitorigoto', 'score': 8.89, 'aired': {'from': 'Oct 2023'}},
    {'title': 'Monster', 'score': 8.88, 'aired': {'from': 'Apr 2004'}},
    {'title': 'Shingeki no Kyojin: The Final Season - Kanketsu-hen', 'score': 8.88, 'aired': {'from': 'Mar 2023'}},
    {'title': 'Gintama.: Shirogane no Tamashii-hen - Kouhan-sen', 'score': 8.88, 'aired': {'from': 'Jul 2018'}},
    {'title': 'Owarimonogatari 2nd Season', 'score': 8.87, 'aired': {'from': 'Aug 2017'}},
    {'title': 'Violet Evergarden Movie', 'score': 8.86, 'aired': {'from': 'Sep 2020'}},
    {'title': 'Kimi no Na wa.', 'score': 8.83, 'aired': {'from': 'Aug 2016'}},
    {'title': 'Kingdom 3rd Season', 'score': 8.83, 'aired': {'from': 'Apr 2020'}},
    {'title': 'Gintama.: Shirogane no Tamashii-hen', 'score': 8.81, 'aired': {'from': 'Jan 2018'}},
    {'title': 'Vinland Saga Season 2', 'score': 8.81, 'aired': {'from': 'Jan 2023'}},
    {'title': 'Jujutsu Kaisen 2nd Season', 'score': 8.8, 'aired': {'from': 'Jul 2023'}},
    {'title': 'Boku no Kokoro no Yabai Yatsu 2nd Season', 'score': 8.8, 'aired': {'from': 'Jan 2024'}},
    {'title': 'Mob Psycho 100 II', 'score': 8.79, 'aired': {'from': 'Jan 2019'}},
    {'title': 'Kizumonogatari III: Reiketsu-hen', 'score': 8.78, 'aired': {'from': 'Jan 2017'}},
    {'title': 'Shingeki no Kyojin: The Final Season', 'score': 8.78, 'aired': {'from': 'Dec 2020'}},
    {'title': 'Sen to Chihiro no Kamikakushi', 'score': 8.77, 'aired': {'from': 'Jul 2001'}},
    {'title': 'Bocchi the Rock!', 'score': 8.77, 'aired': {'from': 'Oct 2022'}},
    {'title': 'Haikyuu!! Karasuno Koukou vs. Shiratorizawa Gakuen Koukou', 'score': 8.77,
     'aired': {'from': 'Oct 2016'}},
    {'title': 'Hajime no Ippo', 'score': 8.77, 'aired': {'from': 'Oct 2000'}},
    {'title': 'Shingeki no Kyojin: The Final Season Part 2', 'score': 8.76, 'aired': {'from': 'Jan 2022'}},
    {'title': 'Vinland Saga', 'score': 8.76, 'aired': {'from': 'Jul 2019'}},
    {'title': 'Kaguya-sama wa Kokurasetai: First Kiss wa Owaranai', 'score': 8.76, 'aired': {'from': 'Dec 2022'}},
    {'title': 'Monogatari Series: Second Season', 'score': 8.76, 'aired': {'from': 'Jul 2013'}},
    {'title': 'Cowboy Bebop', 'score': 8.75, 'aired': {'from': 'Apr 1998'}},
    {'title': 'The First Slam Dunk', 'score': 8.75, 'aired': {'from': 'Dec 2022'}},
    {'title': 'Kimetsu no Yaiba: Yuukaku-hen', 'score': 8.74, 'aired': {'from': 'Dec 2021'}},
    {'title': 'Kingdom 4th Season', 'score': 8.74, 'aired': {'from': 'Apr 2022'}},
    {'title': 'Look Back', 'score': 8.74, 'aired': {'from': 'Jun 2024'}},
    {'title': 'Hibike! Euphonium 3', 'score': 8.74, 'aired': {'from': 'Apr 2024'}},
    {'title': 'Ashita no Joe 2', 'score': 8.73, 'aired': {'from': 'Oct 1980'}},
    {'title': 'Shiguang Dailiren', 'score': 8.73, 'aired': {'from': 'Apr 2021'}},
    {'title': 'Kingdom 5th Season', 'score': 8.73, 'aired': {'from': 'Jan 2024'}},
    {'title': 'Mushishi Zoku Shou 2nd Season', 'score': 8.72, 'aired': {'from': 'Oct 2014'}},
    {'title': 'One Piece', 'score': 8.72, 'aired': {'from': 'Oct 1999'}},
    {'title': 'Mob Psycho 100 III', 'score': 8.71, 'aired': {'from': 'Oct 2022'}},
    {'title': '86 Part 2', 'score': 8.71, 'aired': {'from': 'Oct 2021'}},
    {'title': 'Shouwa Genroku Rakugo Shinjuu: Sukeroku Futatabi-hen', 'score': 8.71, 'aired': {'from': 'Jan 2017'}},
    {'title': 'Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuioku-hen', 'score': 8.7, 'aired': {'from': 'Feb 1999'}},
    {'title': 'Bleach: Sennen Kessen-hen - Ketsubetsu-tan', 'score': 8.7, 'aired': {'from': 'Jul 2023'}},
    {'title': 'Code Geass: Hangyaku no Lelouch', 'score': 8.7, 'aired': {'from': 'Oct 2006'}},
    {'title': 'Great Teacher Onizuka', 'score': 8.69, 'aired': {'from': 'Jun 1999'}},
    {'title': 'Mushishi Zoku Shou', 'score': 8.69, 'aired': {'from': 'Apr 2014'}},
    {'title': 'Mo Dao Zu Shi: Wanjie Pian', 'score': 8.68, 'aired': {'from': 'Aug 2021'}},
    {'title': 'Violet Evergarden', 'score': 8.68, 'aired': {'from': 'Jan 2018'}},
    {'title': 'Tian Guan Cifu Er', 'score': 8.67, 'aired': {'from': 'Oct 2023'}},
    {'title': 'Hajime no Ippo: New Challenger', 'score': 8.67, 'aired': {'from': 'Jan 2009'}},
    {'title': 'Howl no Ugoku Shiro', 'score': 8.67, 'aired': {'from': 'Nov 2004'}},
    {'title': 'Haikyuu!! Movie: Gomisuteba no Kessen', 'score': 8.66, 'aired': {'from': 'Feb 2024'}},
    {'title': 'Mononoke Hime', 'score': 8.66, 'aired': {'from': 'Jul 1997'}},
    {'title': 'Odd Taxi', 'score': 8.66, 'aired': {'from': 'Apr 2021'}},
    {'title': 'Mushishi', 'score': 8.65, 'aired': {'from': 'Oct 2005'}},
    {'title': 'Mushoku Tensei: Isekai Ittara Honki Dasu Part 2', 'score': 8.65, 'aired': {'from': 'Oct 2021'}},
    {'title': "Fate/stay night Movie: Heaven's Feel - III. Spring Song", 'score': 8.65, 'aired': {'from': 'Aug 2020'}},
    {'title': 'Bungou Stray Dogs 5th Season', 'score': 8.64, 'aired': {'from': 'Jul 2023'}},
    {'title': 'Made in Abyss', 'score': 8.64, 'aired': {'from': 'Jul 2017'}},
    {'title': 'Natsume Yuujinchou Shi', 'score': 8.64, 'aired': {'from': 'Jan 2012'}},
    {'title': 'Shigatsu wa Kimi no Uso', 'score': 8.64, 'aired': {'from': 'Oct 2014'}},
    {'title': 'Shiguang Dailiren II', 'score': 8.63, 'aired': {'from': 'Jul 2023'}},
    {'title': 'Shingeki no Kyojin Season 3', 'score': 8.63, 'aired': {'from': 'Jul 2018'}},
    {'title': 'Tengen Toppa Gurren Lagann', 'score': 8.63, 'aired': {'from': 'Apr 2007'}},
    {'title': 'Kaguya-sama wa Kokurasetai? Tensai-tachi no Renai Zunousen', 'score': 8.63,
     'aired': {'from': 'Apr 2020'}},
    {'title': 'Made in Abyss: Retsujitsu no Ougonkyou', 'score': 8.62, 'aired': {'from': 'Jul 2022'}},
    {'title': 'Ping Pong the Animation', 'score': 8.62, 'aired': {'from': 'Apr 2014'}},
    {'title': '"Oshi no Ko"', 'score': 8.62, 'aired': {'from': 'Apr 2023'}},
    {'title': 'Death Note', 'score': 8.62, 'aired': {'from': 'Oct 2006'}},
    {'title': 'Haikyuu!! Second Season', 'score': 8.62, 'aired': {'from': 'Oct 2015'}},
    {'title': 'Dungeon Meshi', 'score': 8.61, 'aired': {'from': 'Jan 2024'}},
    {'title': 'Made in Abyss Movie 3: Fukaki Tamashii no Reimei', 'score': 8.61, 'aired': {'from': 'Jan 2020'}},
    {'title': 'Natsume Yuujinchou Roku', 'score': 8.61, 'aired': {'from': 'Apr 2017'}},
    {'title': 'Cyberpunk: Edgerunners', 'score': 8.6, 'aired': {'from': 'Sep 2022'}},
    {'title': 'Hajime no Ippo: Rising', 'score': 8.6, 'aired': {'from': 'Oct 2013'}},
    {'title': 'Suzumiya Haruhi no Shoushitsu', 'score': 8.6, 'aired': {'from': 'Feb 2010'}},
    {'title': 'Shin Evangelion Movie:||', 'score': 8.59, 'aired': {'from': 'Mar 2021'}},
    {'title': 'Kenpuu Denki Berserk', 'score': 8.59, 'aired': {'from': 'Oct 1997'}},
    {'title': 'Kimi ni Todoke 3rd Season', 'score': 8.59, 'aired': {'from': 'Aug 2024'}},
    {'title': 'Mushishi Zoku Shou: Suzu no Shizuku', 'score': 8.59, 'aired': {'from': 'May 2015'}},
    {'title': 'Seishun Buta Yarou wa Yumemiru Shoujo no Yume wo Minai', 'score': 8.59, 'aired': {'from': 'Jun 2019'}},
    {'title': 'JoJo no Kimyou na Bouken Part 5: Ougon no Kaze', 'score': 8.58, 'aired': {'from': 'Oct 2018'}},
    {'title': 'Jujutsu Kaisen', 'score': 8.58, 'aired': {'from': 'Oct 2020'}},
]

class Plugin:
    def __init__(self):
        self.top_anime_data = top_anime_data
        self.MAX_MESSAGE_LENGTH = 400  # Adjust this value as needed

    def __get_anime_info(self, rank, info_type):
        if rank < 1 or rank > len(self.top_anime_data):
            return f"Rank must be between 1 and {len(self.top_anime_data)}."

        try:
            anime = self.top_anime_data[rank - 1]
            title = anime["title"]
            score = anime["score"]
            release_date = anime["aired"]["from"][:10]

            if info_type == "name":
                return title
            elif info_type == "score":
                return f"Score: {score}"
            elif info_type == "release_date":
                return f"Release Date: {release_date}"
            elif info_type == "all":
                return f"Title: {title} | Score: {score} | Release Date: {release_date}"
            else:
                return "Invalid info type. Please use 'name', 'score', 'release_date', or 'all'."
        except IndexError:
            return "Anime data is not available for the given rank."

    def run(self, incoming, methods, info, bot_info):
        try:
            command_parts = info["args"][1].split()  # Split the second element (the command) by spaces

            if info["command"] == "PRIVMSG":
                if command_parts[0] == ".anime" and len(command_parts) > 2 and command_parts[1] == "rank":
                    try:
                        rank = int(command_parts[2])
                        info_type = command_parts[3] if len(command_parts) > 3 else "all"
                        anime_info = self.__get_anime_info(rank, info_type)
                        methods["send"](info["address"], anime_info)
                    except (IndexError, ValueError) as e:
                        methods["send"](info["address"], "Invalid command. Use: .anime rank <<ranking>> <<info_type>>")
        except Exception as e:
            print("Something went wrong. There is a Plugin Error: ", e)