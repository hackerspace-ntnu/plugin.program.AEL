#!/usr/bin/python -B
# -*- coding: utf-8 -*-

# Test AEL ScreenScraper metadata scraper.
#
# * ScreenScraper works bad for ISO-based platforms. Why?
# * For Playstation games, changing rom_type = 'rom' to 'iso' does not help.
# * jeuRecherche works well, returns several candidates, but ignores the ROM name. For
#   example, searching for FF7 ISO first result returned is FF4.
#

# --- Python standard library ---
from __future__ import unicode_literals
import os
import pprint
import sys

# --- AEL modules ---
if __name__ == "__main__" and __package__ is None:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print('Adding to sys.path {0}'.format(path))
    sys.path.append(path)
from resources.scrap import *
from resources.utils import *
import common

# --- main ---------------------------------------------------------------------------------------
print('*** Fetching candidate game list ********************************************************')
set_log_level(LOG_DEBUG)

# --- Create scraper object ---
scraper_obj = ScreenScraper(common.settings)
scraper_obj.set_verbose_mode(False)
scraper_obj.set_debug_file_dump(True, os.path.join(os.path.dirname(__file__), 'assets'))
scraper_obj.set_debug_checksums(True, '414FA339', '9db5682a4d778ca2cb79580bdb67083f',
    '48c98f7e5a6e736d790ab740dfc3f51a61abe2b5', 123456)
status_dic = kodi_new_status_dic('Scraper test was OK')

# --- Choose data for testing ---
# search_term, rombase, platform = common.games['metroid']
# search_term, rombase, platform = common.games['mworld']
search_term, rombase, platform = common.games['sonic']
# search_term, rombase, platform = common.games['chakan']
# search_term, rombase, platform = common.games['console_wrong_title']
# search_term, rombase, platform = common.games['console_wrong_platform']

# --- Debug call to test API function jeuRecherche.php ---
# scraper_obj.debug_game_search(*common.games['ff7'], status_dic = status_dic)

# --- Get candidates, print them and set first candidate ---
rom_FN = FileName(rombase)
rom_checksums_FN = FileName(rombase)
if scraper_obj.check_candidates_cache(rom_FN, platform):
    print('>>>> Game "{}" "{}" in disk cache.'.format(rom_FN.getBase(), platform))
else:
    print('>>>> Game "{}" "{}" not in disk cache.'.format(rom_FN.getBase(), platform))
candidate_list = scraper_obj.get_candidates(search_term, rom_FN, rom_checksums_FN, platform, status_dic)
# pprint.pprint(candidate_list)
common.handle_get_candidates(candidate_list, status_dic)
print_candidate_list(candidate_list)
scraper_obj.set_candidate(rom_FN, platform, candidate_list[0])

# --- Print metadata of first candidate ----------------------------------------------------------
print('*** Fetching game metadata **************************************************************')
metadata = scraper_obj.get_metadata(status_dic)
# pprint.pprint(metadata)
print_game_metadata(metadata)
scraper_obj.flush_disk_cache()
