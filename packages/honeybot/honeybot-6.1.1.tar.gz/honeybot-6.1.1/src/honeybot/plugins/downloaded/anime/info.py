NAME = "anime.py"

ORIGINAL_AUTHORS = ["Christos Kontos"]

ABOUT = """
This plugin provides detailed information about anime from the top 100 list.
Users can query anime based on rank to get information like name, score, release date, and ranking.
"""

COMMANDS = """
>>> .anime rank <<ranking>> <<info_type>>
Returns the anime information based on rank (1 to 100) and the requested info type (name, score, release_date, ranking).
>>> .anime rank <<ranking>> all
Returns all details (name, score, release date, and ranking) of the anime at the specified rank.
"""
