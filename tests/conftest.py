import pytest
import datetime
from mlbgame.info import Division, Team, Standings
from mlbgame.game import GameScoreboard

NL_EAST_TEAMS = [
    {'vs_left': '21-24', 'vs_central': '18-14', 'home': '42-38', 'vs_right': '66-44', 'vs_division': '46-23', 'vs_east': '46-23', 'elim': '-', 'playoffs_flag_milb': '#', 'extra_inn': '6-8', 'x_wl_seas': '92-70', 'playoffs_flag_mlb': 'y', 'gb': '-', 'interleague': '8-12', 'division': 'National League East', 'is_wildcard_sw': 'Y', 'division_champ': 'Y', 'pct': 0.561, 'playoff_odds': 99.9, 'vs_west': '15-19', 'last_ten': '6-4', 'clinched_sw': 'Y', 'one_run': '22-12', 'points': '', 'place': 1, 'team_full': 'Atlanta Braves', 'team_abbrev': 'ATL', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Atlanta', 'l': 68, 'opp_runs': 638, 'sit_code': 'h0', 'w': 87, 'gb_wildcard': '', 'away': '45-30', 'x_wl': '88-67', 'division_odds': 99.9, 'streak': 'W4', 'wild_card': 'N', 'playoffs_sw': 'Y', 'elim_wildcard': '', 'file_code': 'atl', 'runs': 738, 'division_id': 204, 'team_id': 144},
    {'vs_left': '21-16', 'vs_central': '19-14', 'home': '47-31', 'vs_right': '57-60', 'vs_division': '32-40', 'vs_east': '32-40', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '8-6', 'x_wl_seas': '79-83', 'playoffs_flag_mlb': '', 'gb': 8.5, 'interleague': '12-8', 'division': 'National League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.506, 'playoff_odds': 0.2, 'vs_west': '15-14', 'last_ten': '4-6', 'clinched_sw': 'N', 'one_run': '23-17', 'points': '', 'place': 2, 'team_full': 'Philadelphia Phillies', 'team_abbrev': 'PHI', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Philadelphia', 'l': 76, 'opp_runs': 676, 'sit_code': 'h0', 'w': 78, 'gb_wildcard': 7.5, 'away': '31-45', 'x_wl': '75-79', 'division_odds': 0.2, 'streak': 'L3', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 1, 'file_code': 'phi', 'runs': 661, 'division_id': 204, 'team_id': 143},
    {'vs_left': '17-25', 'vs_central': '18-16', 'home': '38-39', 'vs_right': '61-52', 'vs_division': '38-34', 'vs_east': '38-34', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '4-10', 'x_wl_seas': '90-72', 'playoffs_flag_mlb': '', 'gb': 9.0, 'interleague': '9-11', 'division': 'National League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.503, 'playoff_odds': 0.0, 'vs_west': '13-16', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '18-24', 'points': '', 'place': 3, 'team_full': 'Washington Nationals', 'team_abbrev': 'WSH', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Washington', 'l': 77, 'opp_runs': 645, 'sit_code': 'h0', 'w': 78, 'gb_wildcard': 8.0, 'away': '40-38', 'x_wl': '86-69', 'division_odds': 0.0, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'was', 'runs': 726, 'division_id': 204, 'team_id': 120},
    {'vs_left': '17-24', 'vs_central': '13-20', 'home': '33-42', 'vs_right': '55-59', 'vs_division': '35-34', 'vs_east': '35-34', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '8-9', 'x_wl_seas': '78-84', 'playoffs_flag_mlb': '', 'gb': 15.0, 'interleague': '8-12', 'division': 'National League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.465, 'playoff_odds': 0.0, 'vs_west': '16-17', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '14-26', 'points': '', 'place': 4, 'team_full': 'New York Mets', 'team_abbrev': 'NYM', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'NY Mets', 'l': 83, 'opp_runs': 685, 'sit_code': 'h0', 'w': 72, 'gb_wildcard': 14.0, 'away': '39-41', 'x_wl': '74-81', 'division_odds': 0.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'nym', 'runs': 655, 'division_id': 204, 'team_id': 121},
    {'vs_left': '12-25', 'vs_central': '12-19', 'home': '37-43', 'vs_right': '49-68', 'vs_division': '25-45', 'vs_east': '25-45', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '9-5', 'x_wl_seas': '58-104', 'playoffs_flag_mlb': '', 'gb': 25.5, 'interleague': '9-11', 'division': 'National League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.396, 'playoff_odds': 0.0, 'vs_west': '15-18', 'last_ten': '4-6', 'clinched_sw': 'N', 'one_run': '19-19', 'points': '', 'place': 5, 'team_full': 'Miami Marlins', 'team_abbrev': 'MIA', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Miami', 'l': 93, 'opp_runs': 781, 'sit_code': 'h0', 'w': 61, 'gb_wildcard': 24.5, 'away': '24-50', 'x_wl': '55-99', 'division_odds': 0.0, 'streak': 'W2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'mia', 'runs': 565, 'division_id': 204, 'team_id': 146}
]
NL_CENTRAL_TEAMS = [
    {'vs_left': '21-13', 'vs_central': '37-32', 'home': '47-27', 'vs_right': '69-51', 'vs_division': '37-32', 'vs_east': '22-11', 'elim': '-', 'playoffs_flag_milb': '', 'extra_inn': '10-8', 'x_wl_seas': '93-69', 'playoffs_flag_mlb': '', 'gb': '-', 'interleague': '12-7', 'division': 'National League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'Y', 'pct': 0.584, 'playoff_odds': 100.0, 'vs_west': '19-14', 'last_ten': '6-4', 'clinched_sw': 'N', 'one_run': '25-24', 'points': '', 'place': 1, 'team_full': 'Chicago Cubs', 'team_abbrev': 'CHC', 'playoff_points_sw': 'N', 'wildcard_odds': 19.3, 'team_short': 'Chi Cubs', 'l': 64, 'opp_runs': 613, 'sit_code': 'h0', 'w': 90, 'gb_wildcard': '', 'away': '43-37', 'x_wl': '89-65', 'division_odds': 80.7, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': '', 'file_code': 'chc', 'runs': 724, 'division_id': 205, 'team_id': 112},
    {'vs_left': '21-19', 'vs_central': '35-37', 'home': '48-30', 'vs_right': '67-48', 'vs_division': '35-37', 'vs_east': '20-13', 'elim': 6, 'playoffs_flag_milb': '', 'extra_inn': '9-7', 'x_wl_seas': '88-74', 'playoffs_flag_mlb': '', 'gb': 2.5, 'interleague': '10-7', 'division': 'National League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.568, 'playoff_odds': 99.7, 'vs_west': '23-10', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '30-19', 'points': '', 'place': 2, 'team_full': 'Milwaukee Brewers', 'team_abbrev': 'MIL', 'playoff_points_sw': 'N', 'wildcard_odds': 81.3, 'team_short': 'Milwaukee', 'l': 67, 'opp_runs': 633, 'sit_code': 'h0', 'w': 88, 'gb_wildcard': 2.0, 'away': '40-37', 'x_wl': '84-71', 'division_odds': 18.4, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': '-', 'file_code': 'mil', 'runs': 695, 'division_id': 205, 'team_id': 158},
    {'vs_left': '25-19', 'vs_central': '40-30', 'home': '42-35', 'vs_right': '61-50', 'vs_division': '40-30', 'vs_east': '16-16', 'elim': 4, 'playoffs_flag_milb': '', 'extra_inn': '8-8', 'x_wl_seas': '90-72', 'playoffs_flag_mlb': '', 'gb': 4.5, 'interleague': '11-9', 'division': 'National League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.555, 'playoff_odds': 78.6, 'vs_west': '19-14', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '21-21', 'points': '', 'place': 3, 'team_full': 'St. Louis Cardinals', 'team_abbrev': 'STL', 'playoff_points_sw': 'N', 'wildcard_odds': 77.7, 'team_short': 'St. Louis', 'l': 69, 'opp_runs': 650, 'sit_code': 'h0', 'w': 86, 'gb_wildcard': '-', 'away': '44-34', 'x_wl': '86-69', 'division_odds': 0.8, 'streak': 'W2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': '-', 'file_code': 'stl', 'runs': 730, 'division_id': 205, 'team_id': 138},
    {'vs_left': '19-24', 'vs_central': '39-29', 'home': '44-35', 'vs_right': '59-51', 'vs_division': '39-29', 'vs_east': '12-20', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '6-4', 'x_wl_seas': '81-81', 'playoffs_flag_mlb': '', 'gb': 11.5, 'interleague': '15-5', 'division': 'National League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.51, 'playoff_odds': 0.0, 'vs_west': '12-21', 'last_ten': '7-3', 'clinched_sw': 'N', 'one_run': '28-21', 'points': '', 'place': 4, 'team_full': 'Pittsburgh Pirates', 'team_abbrev': 'PIT', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Pittsburgh', 'l': 75, 'opp_runs': 657, 'sit_code': 'h0', 'w': 78, 'gb_wildcard': 7.0, 'away': '34-40', 'x_wl': '76-77', 'division_odds': 0.0, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 2, 'file_code': 'pit', 'runs': 655, 'division_id': 205, 'team_id': 134},
    {'vs_left': '22-25', 'vs_central': '25-48', 'home': '36-40', 'vs_right': '44-65', 'vs_division': '25-48', 'vs_east': '13-20', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '7-11', 'x_wl_seas': '70-92', 'playoffs_flag_mlb': '', 'gb': 25.0, 'interleague': '10-8', 'division': 'National League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.423, 'playoff_odds': 0.0, 'vs_west': '18-14', 'last_ten': '3-7', 'clinched_sw': 'N', 'one_run': '10-27', 'points': '', 'place': 5, 'team_full': 'Cincinnati Reds', 'team_abbrev': 'CIN', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Cincinnati', 'l': 90, 'opp_runs': 789, 'sit_code': 'h0', 'w': 66, 'gb_wildcard': 20.5, 'away': '30-50', 'x_wl': '68-88', 'division_odds': 0.0, 'streak': 'L2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'cin', 'runs': 680, 'division_id': 205, 'team_id': 113}
]

NL_WEST_TEAMS = [
    {'vs_left': '36-25', 'vs_central': '16-18', 'home': '43-37', 'vs_right': '50-44', 'vs_division': '39-30', 'vs_east': '19-13', 'elim': '-', 'playoffs_flag_milb': '', 'extra_inn': '8-7', 'x_wl_seas': '98-64', 'playoffs_flag_mlb': '', 'gb': '-', 'interleague': '12-8', 'division': 'National League West', 'is_wildcard_sw': 'Y', 'division_champ': 'Y', 'pct': 0.555, 'playoff_odds': 93.8, 'vs_west': '39-30', 'last_ten': '8-2', 'clinched_sw': 'N', 'one_run': '22-21', 'points': '', 'place': 1, 'team_full': 'Los Angeles Dodgers', 'team_abbrev': 'LAD', 'playoff_points_sw': 'N', 'wildcard_odds': 3.7, 'team_short': 'LA Dodgers', 'l': 69, 'opp_runs': 586, 'sit_code': 'h0', 'w': 86, 'gb_wildcard': '', 'away': '43-32', 'x_wl': '94-61', 'division_odds': 90.1, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': '', 'file_code': 'la', 'runs': 745, 'division_id': 203, 'team_id': 119},
    {'vs_left': '33-27', 'vs_central': '14-18', 'home': '41-33', 'vs_right': '51-43', 'vs_division': '40-35', 'vs_east': '17-10', 'elim': 7, 'playoffs_flag_milb': '', 'extra_inn': '5-6', 'x_wl_seas': '81-81', 'playoffs_flag_mlb': '', 'gb': 1.5, 'interleague': '13-7', 'division': 'National League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.545, 'playoff_odds': 27.8, 'vs_west': '40-35', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '26-15', 'points': '', 'place': 2, 'team_full': 'Colorado Rockies', 'team_abbrev': 'COL', 'playoff_points_sw': 'N', 'wildcard_odds': 17.9, 'team_short': 'Colorado', 'l': 70, 'opp_runs': 719, 'sit_code': 'h0', 'w': 84, 'gb_wildcard': 1.5, 'away': '43-37', 'x_wl': '77-77', 'division_odds': 9.9, 'streak': 'W2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 7, 'file_code': 'col', 'runs': 718, 'division_id': 203, 'team_id': 115},
    {'vs_left': '28-26', 'vs_central': '16-16', 'home': '38-39', 'vs_right': '51-50', 'vs_division': '36-33', 'vs_east': '17-17', 'elim': 1, 'playoffs_flag_milb': '', 'extra_inn': '5-7', 'x_wl_seas': '87-75', 'playoffs_flag_mlb': '', 'gb': 7.0, 'interleague': '10-10', 'division': 'National League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.51, 'playoff_odds': 0.1, 'vs_west': '36-33', 'last_ten': '2-8', 'clinched_sw': 'N', 'one_run': '18-29', 'points': '', 'place': 3, 'team_full': 'Arizona Diamondbacks', 'team_abbrev': 'ARI', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Arizona', 'l': 76, 'opp_runs': 619, 'sit_code': 'h0', 'w': 79, 'gb_wildcard': 7.0, 'away': '41-37', 'x_wl': '83-72', 'division_odds': 0.1, 'streak': 'L2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 1, 'file_code': 'ari', 'runs': 668, 'division_id': 203, 'team_id': 109},
    {'vs_left': '29-32', 'vs_central': '11-21', 'home': '41-34', 'vs_right': '43-51', 'vs_division': '37-33', 'vs_east': '16-17', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '10-10', 'x_wl_seas': '74-88', 'playoffs_flag_mlb': '', 'gb': 14.0, 'interleague': '8-12', 'division': 'National League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.465, 'playoff_odds': 0.0, 'vs_west': '37-33', 'last_ten': '4-6', 'clinched_sw': 'N', 'one_run': '25-29', 'points': '', 'place': 4, 'team_full': 'San Francisco Giants', 'team_abbrev': 'SF', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'San Francisco', 'l': 83, 'opp_runs': 650, 'sit_code': 'h0', 'w': 72, 'gb_wildcard': 14.0, 'away': '31-49', 'x_wl': '70-85', 'division_odds': 0.0, 'streak': 'L3', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'sf', 'runs': 587, 'division_id': 203, 'team_id': 137},
    {'vs_left': '16-36', 'vs_central': '16-18', 'home': '29-49', 'vs_right': '46-57', 'vs_division': '24-45', 'vs_east': '15-17', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '3-10', 'x_wl_seas': '65-97', 'playoffs_flag_mlb': '', 'gb': 24.0, 'interleague': '7-13', 'division': 'National League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.4, 'playoff_odds': 0.0, 'vs_west': '24-45', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '19-19', 'points': '', 'place': 5, 'team_full': 'San Diego Padres', 'team_abbrev': 'SD', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'San Diego', 'l': 93, 'opp_runs': 736, 'sit_code': 'h0', 'w': 62, 'gb_wildcard': 24.0, 'away': '33-44', 'x_wl': '63-92', 'division_odds': 0.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'sd', 'runs': 594, 'division_id': 203, 'team_id': 135}
]

AL_EAST_TEAMS = [
    {'vs_left': '21-15', 'vs_central': '19-13', 'home': '54-21', 'vs_right': '84-35', 'vs_division': '49-21', 'vs_east': '49-21', 'elim': '-', 'playoffs_flag_milb': '#', 'extra_inn': '8-4', 'x_wl_seas': '103-59', 'playoffs_flag_mlb': 'y', 'gb': '-', 'interleague': '16-4', 'division': 'American League East', 'is_wildcard_sw': 'Y', 'division_champ': 'Y', 'pct': 0.677, 'playoff_odds': 100.0, 'vs_west': '21-12', 'last_ten': '6-4', 'clinched_sw': 'Y', 'one_run': '25-13', 'points': '', 'place': 1, 'team_full': 'Boston Red Sox', 'team_abbrev': 'BOS', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Boston', 'l': 50, 'opp_runs': 607, 'sit_code': 'h0', 'w': 105, 'gb_wildcard': '', 'away': '51-29', 'x_wl': '99-56', 'division_odds': 100.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'Y', 'elim_wildcard': '', 'file_code': 'bos', 'runs': 824, 'division_id': 201, 'team_id': 111},
    {'vs_left': '29-15', 'vs_central': '23-11', 'home': '53-27', 'vs_right': '66-44', 'vs_division': '39-29', 'vs_east': '39-29', 'elim': 'E', 'playoffs_flag_milb': '&', 'extra_inn': '9-5', 'x_wl_seas': '98-64', 'playoffs_flag_mlb': 'w', 'gb': 9.5, 'interleague': '11-9', 'division': 'American League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.617, 'playoff_odds': 100.0, 'vs_west': '22-10', 'last_ten': '5-5', 'clinched_sw': 'Y', 'one_run': '23-16', 'points': '', 'place': 2, 'team_full': 'New York Yankees', 'team_abbrev': 'NYY', 'playoff_points_sw': 'N', 'wildcard_odds': 100.0, 'team_short': 'NY Yankees', 'l': 59, 'opp_runs': 630, 'sit_code': 'h0', 'w': 95, 'gb_wildcard': 1.5, 'away': '42-32', 'x_wl': '93-61', 'division_odds': 0.0, 'streak': 'W2', 'wild_card': 'Y', 'playoffs_sw': 'N', 'elim_wildcard': '-', 'file_code': 'nyy', 'runs': 795, 'division_id': 201, 'team_id': 147},
    {'vs_left': '25-18', 'vs_central': '21-11', 'home': '48-26', 'vs_right': '61-50', 'vs_division': '37-31', 'vs_east': '37-31', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '5-7', 'x_wl_seas': '90-72', 'playoffs_flag_mlb': '', 'gb': 18.5, 'interleague': '7-13', 'division': 'American League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.558, 'playoff_odds': 0.0, 'vs_west': '21-13', 'last_ten': '7-3', 'clinched_sw': 'N', 'one_run': '26-30', 'points': '', 'place': 3, 'team_full': 'Tampa Bay Rays', 'team_abbrev': 'TB', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Tampa Bay', 'l': 68, 'opp_runs': 598, 'sit_code': 'h0', 'w': 86, 'gb_wildcard': 7.5, 'away': '38-42', 'x_wl': '86-68', 'division_odds': 0.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 1, 'file_code': 'tb', 'runs': 680, 'division_id': 201, 'team_id': 139},
    {'vs_left': '15-35', 'vs_central': '18-15', 'home': '39-38', 'vs_right': '56-49', 'vs_division': '29-43', 'vs_east': '29-43', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '10-6', 'x_wl_seas': '70-92', 'playoffs_flag_mlb': '', 'gb': 34.0, 'interleague': '13-7', 'division': 'American League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.458, 'playoff_odds': 0.0, 'vs_west': '11-19', 'last_ten': '6-4', 'clinched_sw': 'N', 'one_run': '22-16', 'points': '', 'place': 4, 'team_full': 'Toronto Blue Jays', 'team_abbrev': 'TOR', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Toronto', 'l': 84, 'opp_runs': 798, 'sit_code': 'h0', 'w': 71, 'gb_wildcard': 23.0, 'away': '32-46', 'x_wl': '67-88', 'division_odds': 0.0, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'tor', 'runs': 686, 'division_id': 201, 'team_id': 141},
    {'vs_left': '19-31', 'vs_central': '10-23', 'home': '27-50', 'vs_right': '25-79', 'vs_division': '21-51', 'vs_east': '21-51', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '4-9', 'x_wl_seas': '55-107', 'playoffs_flag_mlb': '', 'gb': 60.5, 'interleague': '7-13', 'division': 'American League East', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.286, 'playoff_odds': 0.0, 'vs_west': '6-23', 'last_ten': '3-7', 'clinched_sw': 'N', 'one_run': '12-27', 'points': '', 'place': 5, 'team_full': 'Baltimore Orioles', 'team_abbrev': 'BAL', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Baltimore', 'l': 110, 'opp_runs': 850, 'sit_code': 'h0', 'w': 44, 'gb_wildcard': 49.5, 'away': '17-60', 'x_wl': '52-102', 'division_odds': 0.0, 'streak': 'L2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'bal', 'runs': 591, 'division_id': 201, 'team_id': 110}
]

AL_CENTRAL_TEAMS = [
    {'vs_left': '20-21', 'vs_central': '45-24', 'home': '48-32', 'vs_right': '66-47', 'vs_division': '45-24', 'vs_east': '15-18', 'elim': '-', 'playoffs_flag_milb': '#', 'extra_inn': '3-8', 'x_wl_seas': '97-65', 'playoffs_flag_mlb': 'y', 'gb': '-', 'interleague': '12-8', 'division': 'American League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'Y', 'pct': 0.558, 'playoff_odds': 100.0, 'vs_west': '14-18', 'last_ten': '5-5', 'clinched_sw': 'Y', 'one_run': '20-22', 'points': '', 'place': 1, 'team_full': 'Cleveland Indians', 'team_abbrev': 'CLE', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Cleveland', 'l': 68, 'opp_runs': 620, 'sit_code': 'h0', 'w': 86, 'gb_wildcard': '', 'away': '38-36', 'x_wl': '92-62', 'division_odds': 100.0, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'Y', 'elim_wildcard': '', 'file_code': 'cle', 'runs': 775, 'division_id': 202, 'team_id': 114},
    {'vs_left': '18-25', 'vs_central': '36-33', 'home': '43-31', 'vs_right': '53-58', 'vs_division': '36-33', 'vs_east': '18-16', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '5-8', 'x_wl_seas': '74-88', 'playoffs_flag_mlb': '', 'gb': 15.0, 'interleague': '8-12', 'division': 'American League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.461, 'playoff_odds': 0.0, 'vs_west': '9-22', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '13-21', 'points': '', 'place': 2, 'team_full': 'Minnesota Twins', 'team_abbrev': 'MIN', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Minnesota', 'l': 83, 'opp_runs': 751, 'sit_code': 'h0', 'w': 71, 'gb_wildcard': 22.5, 'away': '28-52', 'x_wl': '70-84', 'division_odds': 0.0, 'streak': 'L2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'min', 'runs': 684, 'division_id': 202, 'team_id': 142},
    {'vs_left': '18-21', 'vs_central': '32-40', 'home': '38-42', 'vs_right': '45-71', 'vs_division': '32-40', 'vs_east': '15-17', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '5-5', 'x_wl_seas': '66-96', 'playoffs_flag_mlb': '', 'gb': 23.5, 'interleague': '6-11', 'division': 'American League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.406, 'playoff_odds': 0.0, 'vs_west': '10-24', 'last_ten': '4-6', 'clinched_sw': 'N', 'one_run': '22-27', 'points': '', 'place': 3, 'team_full': 'Detroit Tigers', 'team_abbrev': 'DET', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Detroit', 'l': 92, 'opp_runs': 748, 'sit_code': 'h0', 'w': 63, 'gb_wildcard': 31.0, 'away': '25-50', 'x_wl': '63-92', 'division_odds': 0.0, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'det', 'runs': 607, 'division_id': 202, 'team_id': 116},
    {'vs_left': '15-25', 'vs_central': '29-40', 'home': '29-48', 'vs_right': '46-68', 'vs_division': '29-40', 'vs_east': '16-16', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '5-5', 'x_wl_seas': '65-97', 'playoffs_flag_mlb': '', 'gb': 25.0, 'interleague': '6-13', 'division': 'American League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.396, 'playoff_odds': 0.0, 'vs_west': '10-24', 'last_ten': '5-5', 'clinched_sw': 'N', 'one_run': '14-23', 'points': '', 'place': 4, 'team_full': 'Chicago White Sox', 'team_abbrev': 'CWS', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Chi White Sox', 'l': 93, 'opp_runs': 797, 'sit_code': 'h0', 'w': 61, 'gb_wildcard': 32.5, 'away': '32-45', 'x_wl': '61-93', 'division_odds': 0.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'cws', 'runs': 636, 'division_id': 202, 'team_id': 145},
    {'vs_left': '17-30', 'vs_central': '33-38', 'home': '30-47', 'vs_right': '36-72', 'vs_division': '33-38', 'vs_east': '9-24', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '4-8', 'x_wl_seas': '61-101', 'playoffs_flag_mlb': '', 'gb': 33.5, 'interleague': '4-14', 'division': 'American League Central', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.342, 'playoff_odds': 0.0, 'vs_west': '7-26', 'last_ten': '4-6', 'clinched_sw': 'N', 'one_run': '16-29', 'points': '', 'place': 5, 'team_full': 'Kansas City Royals', 'team_abbrev': 'KC', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Kansas City', 'l': 102, 'opp_runs': 806, 'sit_code': 'h0', 'w': 53, 'gb_wildcard': 41.0, 'away': '23-55', 'x_wl': '58-97', 'division_odds': 0.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'kc', 'runs': 607, 'division_id': 202, 'team_id': 118}
]

AL_WEST_TEAMS = [
    {'vs_left': '36-23', 'vs_central': '25-7', 'home': '45-35', 'vs_right': '61-34', 'vs_division': '45-30', 'vs_east': '14-13', 'elim': '-', 'playoffs_flag_milb': '@', 'extra_inn': '5-6', 'x_wl_seas': '109-53', 'playoffs_flag_mlb': 'x', 'gb': '-', 'interleague': '13-7', 'division': 'American League West', 'is_wildcard_sw': 'Y', 'division_champ': 'Y', 'pct': 0.63, 'playoff_odds': 100.0, 'vs_west': '45-30', 'last_ten': '7-3', 'clinched_sw': 'Y', 'one_run': '22-24', 'points': '', 'place': 1, 'team_full': 'Houston Astros', 'team_abbrev': 'HOU', 'playoff_points_sw': 'N', 'wildcard_odds': 0.7, 'team_short': 'Houston', 'l': 57, 'opp_runs': 515, 'sit_code': 'h0', 'w': 97, 'gb_wildcard': '', 'away': '52-22', 'x_wl': '104-50', 'division_odds': 99.3, 'streak': 'W2', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': '', 'file_code': 'hou', 'runs': 770, 'division_id': 200, 'team_id': 117},
    {'vs_left': '30-25', 'vs_central': '26-7', 'home': '50-30', 'vs_right': '64-36', 'vs_division': '35-35', 'vs_east': '21-11', 'elim': 5, 'playoffs_flag_milb': '', 'extra_inn': '13-5', 'x_wl_seas': '95-67', 'playoffs_flag_mlb': '', 'gb': 3.5, 'interleague': '12-8', 'division': 'American League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.606, 'playoff_odds': 100.0, 'vs_west': '35-35', 'last_ten': '6-4', 'clinched_sw': 'N', 'one_run': '31-13', 'points': '', 'place': 2, 'team_full': 'Oakland Athletics', 'team_abbrev': 'OAK', 'playoff_points_sw': 'N', 'wildcard_odds': 99.3, 'team_short': 'Oakland', 'l': 61, 'opp_runs': 638, 'sit_code': 'h0', 'w': 94, 'gb_wildcard': '-', 'away': '44-31', 'x_wl': '91-64', 'division_odds': 0.7, 'streak': 'W4', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': '-', 'file_code': 'oak', 'runs': 774, 'division_id': 200, 'team_id': 133},
    {'vs_left': '28-23', 'vs_central': '23-9', 'home': '41-33', 'vs_right': '57-46', 'vs_division': '37-31', 'vs_east': '19-15', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '13-1', 'x_wl_seas': '78-84', 'playoffs_flag_mlb': '', 'gb': 12.0, 'interleague': '6-14', 'division': 'American League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.552, 'playoff_odds': 0.0, 'vs_west': '37-31', 'last_ten': '6-4', 'clinched_sw': 'N', 'one_run': '36-21', 'points': '', 'place': 3, 'team_full': 'Seattle Mariners', 'team_abbrev': 'SEA', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Seattle', 'l': 69, 'opp_runs': 671, 'sit_code': 'h0', 'w': 85, 'gb_wildcard': 8.5, 'away': '44-36', 'x_wl': '74-80', 'division_odds': 0.0, 'streak': 'W1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'sea', 'runs': 641, 'division_id': 200, 'team_id': 136},
    {'vs_left': '20-29', 'vs_central': '22-12', 'home': '37-38', 'vs_right': '55-51', 'vs_division': '32-37', 'vs_east': '11-21', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '4-7', 'x_wl_seas': '81-81', 'playoffs_flag_mlb': '', 'gb': 22.5, 'interleague': '10-10', 'division': 'American League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.484, 'playoff_odds': 0.0, 'vs_west': '32-37', 'last_ten': '3-7', 'clinched_sw': 'N', 'one_run': '23-15', 'points': '', 'place': 4, 'team_full': 'Los Angeles Angels', 'team_abbrev': 'LAA', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'LA Angels', 'l': 80, 'opp_runs': 695, 'sit_code': 'h0', 'w': 75, 'gb_wildcard': 19.0, 'away': '38-42', 'x_wl': '77-78', 'division_odds': 0.0, 'streak': 'L4', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'ana', 'runs': 692, 'division_id': 200, 'team_id': 108},
    {'vs_left': '20-31', 'vs_central': '18-15', 'home': '33-47', 'vs_right': '45-58', 'vs_division': '26-42', 'vs_east': '12-21', 'elim': 'E', 'playoffs_flag_milb': '', 'extra_inn': '7-6', 'x_wl_seas': '71-91', 'playoffs_flag_mlb': '', 'gb': 32.0, 'interleague': '9-11', 'division': 'American League West', 'is_wildcard_sw': 'Y', 'division_champ': 'N', 'pct': 0.422, 'playoff_odds': 0.0, 'vs_west': '26-42', 'last_ten': '3-7', 'clinched_sw': 'N', 'one_run': '12-17', 'points': '', 'place': 5, 'team_full': 'Texas Rangers', 'team_abbrev': 'TEX', 'playoff_points_sw': 'N', 'wildcard_odds': 0.0, 'team_short': 'Texas', 'l': 89, 'opp_runs': 816, 'sit_code': 'h0', 'w': 65, 'gb_wildcard': 28.5, 'away': '32-42', 'x_wl': '68-86', 'division_odds': 0.0, 'streak': 'L1', 'wild_card': 'N', 'playoffs_sw': 'N', 'elim_wildcard': 'E', 'file_code': 'tex', 'runs': 714, 'division_id': 200, 'team_id': 140}
]

DIVISIONS = [
    {'division': 'NL East', 'teams': NL_EAST_TEAMS},
    {'division': 'NL Central', 'teams': NL_CENTRAL_TEAMS},
    {'division': 'NL West', 'teams': NL_WEST_TEAMS},
    {'division': 'AL East', 'teams': AL_EAST_TEAMS},
    {'division': 'AL Central', 'teams': AL_CENTRAL_TEAMS},
    {'division': 'AL West', 'teams': AL_WEST_TEAMS}
]

STANDINGS = Standings(data={'standings_schedule_date': 'standings_schedule_date',
    'divisions': DIVISIONS})

GAMES = [
    GameScoreboard(data={'game_id': '2018_09_23_balmlb_nyamlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '01:05 pm', 'home_team': 'Yankees', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Orioles', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Alex Cobb', 'p_pitcher_home_wins': 5, 'p_pitcher_home_losses': 15, 'p_pitcher_away': 'J.A. Happ', 'p_pitcher_away_wins': 16, 'p_pitcher_away_losses': 6, 'game_id': '2018_09_23_b', 'game_start_time': '01:05 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_tbamlb_tormlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '01:07 pm', 'home_team': 'Blue Jays', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Rays', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Blake Snell', 'p_pitcher_home_wins': 20, 'p_pitcher_home_losses': 5, 'p_pitcher_away': 'Ryan Borucki', 'p_pitcher_away_wins': 4, 'p_pitcher_away_losses': 4, 'game_id': '2018_09_23_b', 'game_start_time': '01:07 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_cinmlb_miamlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '01:10 pm', 'home_team': 'Marlins', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Reds', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Michael Lorenzen', 'p_pitcher_home_wins': 3, 'p_pitcher_home_losses': 1, 'p_pitcher_away': 'Trevor Richards', 'p_pitcher_away_wins': 3, 'p_pitcher_away_losses': 9, 'game_id': '2018_09_23_b', 'game_start_time': '01:10 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_kcamlb_detmlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '01:10 pm', 'home_team': 'Tigers', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Royals', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Brad Keller', 'p_pitcher_home_wins': 8, 'p_pitcher_home_losses': 6, 'p_pitcher_away': 'Daniel Norris', 'p_pitcher_away_wins': 0, 'p_pitcher_away_losses': 5, 'game_id': '2018_09_23_b', 'game_start_time': '01:10 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_milmlb_pitmlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '01:35 pm', 'home_team': 'Pirates', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Brewers', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Wade Miley', 'p_pitcher_home_wins': 5, 'p_pitcher_home_losses': 2, 'p_pitcher_away': 'Nick Kingham', 'p_pitcher_away_wins': 5, 'p_pitcher_away_losses': 6, 'game_id': '2018_09_23_b', 'game_start_time': '01:35 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_nynmlb_wasmlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '01:35 pm', 'home_team': 'Nationals', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Mets', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Steven Matz', 'p_pitcher_home_wins': 5, 'p_pitcher_home_losses': 11, 'p_pitcher_away': 'Erick Fedde', 'p_pitcher_away_wins': 2, 'p_pitcher_away_losses': 3, 'game_id': '2018_09_23_b', 'game_start_time': '01:35 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_phimlb_atlmlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '01:35 pm', 'home_team': 'Braves', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Phillies', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Aaron Nola', 'p_pitcher_home_wins': 16, 'p_pitcher_home_losses': 5, 'p_pitcher_away': 'Anibal Sanchez', 'p_pitcher_away_wins': 6, 'p_pitcher_away_losses': 6, 'game_id': '2018_09_23_b', 'game_start_time': '01:35 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_chnmlb_chamlb_1', 'game_tag': 'sg_game', 'game_league': 'NA', 'game_status': 'PRE_GAME', 'game_start_time': '02:10 pm', 'home_team': 'White Sox', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Cubs', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Kyle Hendricks', 'p_pitcher_home_wins': 12, 'p_pitcher_home_losses': 11, 'p_pitcher_away': 'Carlos Rodon', 'p_pitcher_away_wins': 6, 'p_pitcher_away_losses': 6, 'game_id': '2018_09_23_b', 'game_start_time': '02:10 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_anamlb_houmlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '02:10 pm', 'home_team': 'Astros', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Angels', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Tyler Skaggs', 'p_pitcher_home_wins': 8, 'p_pitcher_home_losses': 8, 'p_pitcher_away': 'Charlie Morton', 'p_pitcher_away_wins': 15, 'p_pitcher_away_losses': 3, 'game_id': '2018_09_23_b', 'game_start_time': '02:10 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_sfnmlb_slnmlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '02:15 pm', 'home_team': 'Cardinals', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Giants', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Andrew Suarez', 'p_pitcher_home_wins': 7, 'p_pitcher_home_losses': 11, 'p_pitcher_away': 'Miles Mikolas', 'p_pitcher_away_wins': 16, 'p_pitcher_away_losses': 4, 'game_id': '2018_09_23_b', 'game_start_time': '02:15 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_seamlb_texmlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '03:05 pm', 'home_team': 'Rangers', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Mariners', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Wade LeBlanc', 'p_pitcher_home_wins': 8, 'p_pitcher_home_losses': 4, 'p_pitcher_away': 'Martin Perez', 'p_pitcher_away_wins': 2, 'p_pitcher_away_losses': 6, 'game_id': '2018_09_23_b', 'game_start_time': '03:05 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_minmlb_oakmlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '04:05 pm', 'home_team': 'Athletics', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Twins', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Kyle Gibson', 'p_pitcher_home_wins': 8, 'p_pitcher_home_losses': 13, 'p_pitcher_away': 'Trevor Cahill', 'p_pitcher_away_wins': 6, 'p_pitcher_away_losses': 3, 'game_id': '2018_09_23_b', 'game_start_time': '04:05 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_colmlb_arimlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '04:10 pm', 'home_team': 'D-backs', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Rockies', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Kyle Freeland', 'p_pitcher_home_wins': 15, 'p_pitcher_home_losses': 7, 'p_pitcher_away': 'Zack Godley', 'p_pitcher_away_wins': 14, 'p_pitcher_away_losses': 10, 'game_id': '2018_09_23_b', 'game_start_time': '04:10 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_sdnmlb_lanmlb_1', 'game_tag': 'sg_game', 'game_league': 'NN', 'game_status': 'PRE_GAME', 'game_start_time': '04:10 pm', 'home_team': 'Dodgers', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Padres', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Joey Lucchesi', 'p_pitcher_home_wins': 8, 'p_pitcher_home_losses': 8, 'p_pitcher_away': 'Hyun-Jin Ryu', 'p_pitcher_away_wins': 5, 'p_pitcher_away_losses': 3, 'game_id': '2018_09_23_b', 'game_start_time': '04:10 pm'}),

    GameScoreboard(data={'game_id': '2018_09_23_bosmlb_clemlb_1', 'game_tag': 'sg_game', 'game_league': 'AA', 'game_status': 'PRE_GAME', 'game_start_time': '07:05 pm', 'home_team': 'Indians', 'home_team_runs': 0, 'home_team_hits': 0, 'home_team_errors': 0, 'away_team': 'Red Sox', 'away_team_runs': 0, 'away_team_hits': 0, 'away_team_errors': 0, 'p_pitcher_home': 'Hector Velazquez', 'p_pitcher_home_wins': 7, 'p_pitcher_home_losses': 2, 'p_pitcher_away': 'Adam Plutko', 'p_pitcher_away_wins': 4, 'p_pitcher_away_losses': 5, 'game_id': '2018_09_23_b', 'game_start_time': '07:05 pm'})

]

@pytest.fixture
def static_standings():
    return STANDINGS

@pytest.fixture
def static_games():
    return GAMES