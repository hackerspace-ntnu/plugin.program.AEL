# -*- coding: utf-8 -*-
#
# Advanced Emulator Launcher platform constants.
# This module has no external dependencies.
#

# Copyright (c) 2016-2019 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# --- Python standard library ---
from __future__ import unicode_literals

# -------------------------------------------------------------------------------------------------
# A universal addon error reporting exception
# This exception is raised to report errors in the GUI.
# Unhandled exceptions must not raise AddonError() so the addon crashes and the traceback is
# printed in the Kodi log file.
# -------------------------------------------------------------------------------------------------
# Top-level GUI code looks like this
# try:
#     autoconfig_export_category(category, export_FN)
# except AddonError as E:
#     kodi_notify_warn('{0}'.format(E))
# else:
#     kodi_notify('Exported Category "{0}" XML config'.format(category['m_name']))
#
# Low-level code looks like this
# def autoconfig_export_category(category, export_FN):
#     try:
#         do_something_that_may_fail()
#     except OSError:
#         log_error('(OSError) Cannot write {0} file'.format(export_FN.getBase()))
#         # Message to be printed in the GUI
#         raise AddonError('Error writing file (OSError)')
#
class AddonError(Exception):
    def __init__(self, err_str): self.err_str = err_str
    def __str__(self): return self.err_str

# -------------------------------------------------------------------------------------------------
# Addon constants
# -------------------------------------------------------------------------------------------------
# --- Misc "constants" ---
KIND_CATEGORY    = 1
KIND_COLLECTION  = 2
KIND_LAUNCHER    = 3
KIND_ROM         = 4
PLOT_STR_MAXSIZE = 40
RETROPLAYER_LAUNCHER_APP_NAME = 'retroplayer_launcher_app'
LNK_LAUNCHER_APP_NAME         = 'lnk_launcher_app'

# --- Special Cateogry/Launcher IDs ---
VCATEGORY_ADDONROOT_ID   = 'root_category'
VCATEGORY_FAVOURITES_ID  = 'vcategory_favourites'
VCATEGORY_COLLECTIONS_ID = 'vcategory_collections'
VCATEGORY_RECENT_ID      = 'vcategory_recent'
VCATEGORY_MOST_PLAYED_ID = 'vcategory_most_played'
VCATEGORY_TITLE_ID       = 'vcategory_title'
VCATEGORY_YEARS_ID       = 'vcategory_year'
VCATEGORY_GENRE_ID       = 'vcategory_genre'
VCATEGORY_DEVELOPER_ID   = 'vcategory_developer'
VCATEGORY_NPLAYERS_ID    = 'vcategory_nplayer'
VCATEGORY_ESRB_ID        = 'vcategory_esrb'
VCATEGORY_RATING_ID      = 'vcategory_rating'
VCATEGORY_CATEGORY_ID    = 'vcategory_category'
VCATEGORY_OFF_SCRAPER_ID = 'vcategory_offline_scraper'
VLAUNCHER_FAVOURITES_ID  = 'vlauncher_favourites'
VLAUNCHER_RECENT_ID      = 'vlauncher_recent'
VLAUNCHER_MOST_PLAYED_ID = 'vlauncher_most_played'

# --- Content type property to be used by skins ---
AEL_CONTENT_WINDOW_ID          = 10000
AEL_CONTENT_LABEL              = 'AEL_Content'
AEL_CONTENT_VALUE_LAUNCHERS    = 'launchers'
AEL_CONTENT_VALUE_ROMS         = 'roms'
AEL_CONTENT_VALUE_CATEGORY     = 'category'
AEL_CONTENT_VALUE_STD_LAUNCHER = 'std_launcher'
AEL_CONTENT_VALUE_ROM_LAUNCHER = 'rom_launcher'
AEL_CONTENT_VALUE_ROM          = 'rom'
AEL_CONTENT_VALUE_NONE         = ''

AEL_LAUNCHER_NAME_LABEL        = 'AEL_Launch_Name'
AEL_LAUNCHER_ICON_LABEL        = 'AEL_Launch_Icon'
AEL_LAUNCHER_CLEARLOGO_LABEL   = 'AEL_Launch_Clearlogo'

# Value is the number of items inside a launcher.
AEL_NUMITEMS_LABEL             = 'AEL_NumItems'

# --- ROM flags used by skins to display status icons ---
AEL_INFAV_BOOL_LABEL                 = 'AEL_InFav'
AEL_INFAV_BOOL_VALUE_TRUE            = 'InFav_True'
AEL_INFAV_BOOL_VALUE_FALSE           = 'InFav_False'
AEL_MULTIDISC_BOOL_LABEL             = 'AEL_MultiDisc'
AEL_MULTIDISC_BOOL_VALUE_TRUE        = 'MultiDisc_True'
AEL_MULTIDISC_BOOL_VALUE_FALSE       = 'MultiDisc_False'
AEL_FAV_STAT_LABEL                   = 'AEL_Fav_stat'
AEL_FAV_STAT_VALUE_OK                = 'Fav_OK'
AEL_FAV_STAT_VALUE_UNLINKED_ROM      = 'Fav_UnlinkedROM'
AEL_FAV_STAT_VALUE_UNLINKED_LAUNCHER = 'Fav_UnlinkedLauncher'
AEL_FAV_STAT_VALUE_BROKEN            = 'Fav_Broken'
AEL_FAV_STAT_VALUE_NONE              = 'Fav_None'
AEL_NOINTRO_STAT_LABEL               = 'AEL_NoIntro_stat'
AEL_NOINTRO_STAT_VALUE_HAVE          = 'NoIntro_Have'
AEL_NOINTRO_STAT_VALUE_MISS          = 'NoIntro_Miss'
AEL_NOINTRO_STAT_VALUE_UNKNOWN       = 'NoIntro_Unknown'
AEL_NOINTRO_STAT_VALUE_NONE          = 'NoIntro_None'
AEL_PCLONE_STAT_LABEL                = 'AEL_PClone_stat'
AEL_PCLONE_STAT_VALUE_PARENT         = 'PClone_Parent'
AEL_PCLONE_STAT_VALUE_CLONE          = 'PClone_Clone'
AEL_PCLONE_STAT_VALUE_NONE           = 'PClone_None'

# --- ID of the fake ROM parent of all Unknown ROMs ---
UNKNOWN_ROMS_PARENT_ID = 'Unknown_ROMs_Parent'

# -------------------------------------------------------------------------------------------------
# Metadata
# -------------------------------------------------------------------------------------------------
# launcher['nointro_display_mode'] values default NOINTRO_DMODE_ALL
NOINTRO_DMODE_ALL       = 'All ROMs'
NOINTRO_DMODE_HAVE      = 'Have ROMs'
NOINTRO_DMODE_HAVE_UNK  = 'Have or Unknown ROMs'
NOINTRO_DMODE_HAVE_MISS = 'Have or Missing ROMs'
NOINTRO_DMODE_MISS      = 'Missing ROMs'
NOINTRO_DMODE_MISS_UNK  = 'Missing or Unknown ROMs'
NOINTRO_DMODE_UNK       = 'Unknown ROMs'
NOINTRO_DMODE_LIST = [
    NOINTRO_DMODE_ALL,
    NOINTRO_DMODE_HAVE,
    NOINTRO_DMODE_HAVE_UNK, 
    NOINTRO_DMODE_HAVE_MISS,
    NOINTRO_DMODE_MISS,
    NOINTRO_DMODE_MISS_UNK,
    NOINTRO_DMODE_UNK
]

# launcher['launcher_display_mode'] values default LAUNCHER_DMODE_FLAT
LAUNCHER_DMODE_FLAT   = 'Flat mode'
LAUNCHER_DMODE_PCLONE = 'Parent/Clone mode'
LAUNCHER_DMODE_1G1R   = '1G1R mode'
LAUNCHER_DMODE_LIST = [
    LAUNCHER_DMODE_FLAT,
    LAUNCHER_DMODE_PCLONE,
    LAUNCHER_DMODE_1G1R
]

# Mandatory variables in XML:
# id              string MD5 hash
# name            string ROM name
# finished        bool default False
# nointro_status  string ['Have', 'Miss', 'Added', 'Unknown', 'None'] default 'None'
NOINTRO_STATUS_HAVE    = 'Have'
NOINTRO_STATUS_MISS    = 'Miss'
NOINTRO_STATUS_UNKNOWN = 'Unknown'
NOINTRO_STATUS_NONE    = 'None'
NOINTRO_STATUS_LIST = [
    NOINTRO_STATUS_HAVE,
    NOINTRO_STATUS_MISS,
    NOINTRO_STATUS_UNKNOWN,
    NOINTRO_STATUS_NONE
]

PCLONE_STATUS_PARENT = 'Parent'
PCLONE_STATUS_CLONE  = 'Clone'
PCLONE_STATUS_NONE   = 'None'
PCLONE_STATUS_LIST = [
    PCLONE_STATUS_PARENT,
    PCLONE_STATUS_CLONE,
    PCLONE_STATUS_NONE
]

# m_esrb string ESRB_LIST default ESRB_PENDING
ESRB_PENDING     = 'RP (Rating Pending)'
ESRB_EARLY       = 'EC (Early Childhood)'
ESRB_EVERYONE    = 'E (Everyone)'
ESRB_EVERYONE_10 = 'E10+ (Everyone 10+)'
ESRB_TEEN        = 'T (Teen)'
ESRB_MATURE      = 'M (Mature)'
ESRB_ADULTS_ONLY = 'AO (Adults Only)'
ESRB_LIST = [
    ESRB_PENDING,
    ESRB_EARLY,
    ESRB_EVERYONE,
    ESRB_EVERYONE_10,
    ESRB_TEEN,
    ESRB_MATURE,
    ESRB_ADULTS_ONLY
]

# m_nplayers values default ''
NP_NOT_SET = ''
NP_1P      = '1P'
NP_2P_SIM  = '2P sim'
NP_2P_ALT  = '2P alt'
NP_3P_SIM  = '3P sim'
NP_3P_ALT  = '3P alt'
NP_4P_SIM  = '4P sim'
NP_4P_ALT  = '4P alt'
NP_6P_SIM  = '6P sim'
NP_6P_ALT  = '6P alt'
NP_8P_SIM  = '8P sim'
NP_8P_ALT  = '8P alt'
NPLAYERS_LIST = [
    NP_1P,
    NP_2P_SIM,
    NP_2P_ALT,
    NP_3P_SIM,
    NP_3P_ALT,
    NP_4P_SIM,
    NP_4P_ALT,
    NP_6P_SIM,
    NP_6P_ALT,
    NP_8P_SIM,
    NP_8P_ALT,
]

# Use unique string as IDs.
META_TITLE_ID     = 'title'
META_YEAR_ID      = 'year'
META_GENRE_ID     = 'genre'
META_DEVELOPER_ID = 'developer'
META_NPLAYERS_ID  = 'nplayers'
META_ESRB_ID      = 'esrb'
META_RATING_ID    = 'rating'
META_PLOT_ID      = 'plot'

DEFAULT_META_TITLE     = ''
DEFAULT_META_YEAR      = ''
DEFAULT_META_GENRE     = ''
DEFAULT_META_DEVELOPER = ''
DEFAULT_META_NPLAYERS  = ''
DEFAULT_META_ESRB      = ESRB_PENDING
DEFAULT_META_RATING    = ''
DEFAULT_META_PLOT      = ''

# -------------------------------------------------------------------------------------------------
# Assets
# -------------------------------------------------------------------------------------------------
# --- Kodi standard artwork types. Mappable to any other artwork type including itself ---
# # Use unique string as IDs. Then, if asset order changes the IDs are the same.
ASSET_ICON_ID       = 'icon'
ASSET_FANART_ID     = 'fanart'
ASSET_CLEARLOGO_ID  = 'clearlogo'
ASSET_POSTER_ID     = 'poster'
ASSET_BANNER_ID     = 'banner' # Marquee in MAME
ASSET_TRAILER_ID    = 'trailer'
# --- AEL artwork types ---
# What about supporting BOXSPINE and composite box (fron, spine and back in one image).
ASSET_TITLE_ID      = 'title'
ASSET_SNAP_ID       = 'snap'
ASSET_BOXFRONT_ID   = 'boxfront'  # Cabinet in MAME
ASSET_BOXBACK_ID    = 'boxback'   # CPanel in MAME
ASSET_3DBOX_ID      = '3dbox'
ASSET_CARTRIDGE_ID  = 'cartridge' # PCB in MAME
ASSET_FLYER_ID      = 'flyer'
ASSET_MAP_ID        = 'map'
ASSET_MANUAL_ID     = 'manual'
ASSET_CONTROLLER_ID = 'controller'

#
# The order of this list must match order in dialog.select() in the GUI, or bad things will happen.
#
CATEGORY_ASSET_ID_LIST = [
    ASSET_ICON_ID,
    ASSET_FANART_ID,
    ASSET_BANNER_ID,
    ASSET_CLEARLOGO_ID,
    ASSET_POSTER_ID,
    ASSET_TRAILER_ID,
]
COLLECTION_ASSET_ID_LIST = CATEGORY_ASSET_ID_LIST

LAUNCHER_ASSET_ID_LIST = [
    ASSET_ICON_ID,
    ASSET_FANART_ID,
    ASSET_BANNER_ID,
    ASSET_CLEARLOGO_ID,
    ASSET_POSTER_ID,
    ASSET_CONTROLLER_ID,
    ASSET_TRAILER_ID,
]

ROM_ASSET_ID_LIST = [
    ASSET_FANART_ID,
    ASSET_BANNER_ID,
    ASSET_CLEARLOGO_ID,
    ASSET_TITLE_ID,
    ASSET_SNAP_ID,
    ASSET_BOXFRONT_ID,
    ASSET_BOXBACK_ID,
    ASSET_3DBOX_ID,
    ASSET_CARTRIDGE_ID,
    ASSET_FLYER_ID,
    ASSET_MAP_ID,
    ASSET_MANUAL_ID,
    ASSET_TRAILER_ID,
]

# --- Addon will search these file extensions for assets ---
# Check http://kodi.wiki/view/advancedsettings.xml#videoextensions
IMAGE_EXTENSION_LIST   = ['png', 'jpg', 'gif', 'bmp']
MANUAL_EXTENSION_LIST  = ['pdf', 'cbz', 'cbr']
TRAILER_EXTENSION_LIST = ['mov', 'divx', 'xvid', 'wmv', 'avi', 'mpg', 'mpeg', 'mp4', 'mkv', 'avc']

# --- Scrapers -----------------------------------------------------------------------------------
# --- Options ---
# Use True only for development.
SCRAPER_CACHE_HUMAN_JSON = True

# --- IDs ---
SCRAPER_NULL_ID          = 10
SCRAPER_AEL_OFFLINE_ID   = 20
SCRAPER_THEGAMESDB_ID    = 30
SCRAPER_MOBYGAMES_ID     = 40
SCRAPER_SCREENSCRAPER_ID = 50
SCRAPER_GAMEFAQS_ID      = 60 # Disabled at the moment.
SCRAPER_ARCADEDB_ID      = 70
SCRAPER_LIBRETRO_ID      = 80 # Not coded yet.

# List of enabled scrapers. If a scraper ID is in this list then a unique scraper object
# will be instantiated and cached in the global ScraperFactory object.
# To disable an scraper just remove it from this list.
SCRAPER_LIST = [
    SCRAPER_NULL_ID,
    SCRAPER_AEL_OFFLINE_ID,
    SCRAPER_THEGAMESDB_ID,
    SCRAPER_MOBYGAMES_ID,
    SCRAPER_SCREENSCRAPER_ID,
    SCRAPER_ARCADEDB_ID,
]

# Make sure this matches the scraper list in settings.xml or bad things will happen.
SCRAP_METADATA_SETTINGS_LIST = [
    SCRAPER_AEL_OFFLINE_ID,
    SCRAPER_THEGAMESDB_ID,
    SCRAPER_SCREENSCRAPER_ID,
    SCRAPER_MOBYGAMES_ID,
]

SCRAP_ASSET_SETTINGS_LIST = [
    SCRAPER_THEGAMESDB_ID,
    SCRAPER_SCREENSCRAPER_ID,
    SCRAPER_MOBYGAMES_ID,
]

SCRAP_METADATA_MAME_SETTINGS_LIST = [
    SCRAPER_AEL_OFFLINE_ID,
    SCRAPER_ARCADEDB_ID,
    SCRAPER_THEGAMESDB_ID,
    SCRAPER_SCREENSCRAPER_ID,
    SCRAPER_MOBYGAMES_ID,
]

SCRAP_ASSET_MAME_SETTINGS_LIST = [
    SCRAPER_ARCADEDB_ID,
    SCRAPER_THEGAMESDB_ID,
    SCRAPER_SCREENSCRAPER_ID,
    SCRAPER_MOBYGAMES_ID,
]
