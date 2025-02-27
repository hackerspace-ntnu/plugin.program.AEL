# -*- coding: utf-8 -*-

# Advanced Emulator Launcher miscellaneous functions

# Copyright (c) 2016-2019 Wintermute0110 <wintermute0110@gmail.com>
# Portions (c) 2010-2015 Angelscry and others
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

#
# Utility functions which does not depend on Kodi modules (except log_* functions)
#

# --- Python standard library ---
from __future__ import unicode_literals
import collections
import sys
import os
import shutil
import time
import random
import hashlib
import urlparse
import re
import string
import fnmatch
import HTMLParser
import zlib

# --- Kodi modules ---
# >> FileName class uses xbmc.translatePath()
from utils_kodi import *

# --- AEL modules ---
# >> utils.py and utils_kodi.py must not depend on any other AEL module to avoid circular dependencies.

# OS utils
# >> Determine platform
# >> See http://stackoverflow.com/questions/446209/possible-values-from-sys-platform
def is_windows():
    return sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'cygwin'

def is_osx():
    return sys.platform.startswith('darwin')

def is_linux():
    return sys.platform.startswith('linux') and not is_android()

def is_android():
    if not sys.platform.startswith('linux'): return False

    return 'ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ or 'XBMC_ANDROID_APK' in os.environ

# -------------------------------------------------------------------------------------------------
# Strings and text
# -------------------------------------------------------------------------------------------------
# Limits the length of a string for printing. If max_length == -1 do nothing (string has no
# length limit). The string is trimmed by cutting it and adding three dots ... at the end.
# Including these three dots the length of the returned string is max_length or less.
# Example: 'asdfasdfdasf' -> 'asdfsda...'
#
# @param string: [str] String to be trimmed.
# @param max_length: [int] Integer maximum length of the string.
# @return [str] Trimmed string.
def text_limit_string(string, max_length):
    if max_length > 5 and len(string) > max_length:
        string = string[0:max_length-3] + '...'
    return string

# Given a Category/Launcher name clean it so the cleaned srt can be used as a filename.
# 1) Convert any non-printable character into '_'
# 2) Convert spaces ' ' into '_'
def text_title_to_filename_str(title_str):
    cleaned_str_1 = ''.join([i if i in string.printable else '_' for i in title_str])
    cleaned_str_2 = cleaned_str_1.replace(' ', '_')
    return cleaned_str_2

#
# Writes a XML text tag line, indented 2 spaces by default.
# Both tag_name and tag_text must be Unicode strings.
# Returns an Unicode string.
#
def XML_text(tag_name, tag_text, num_spaces = 2):
    if tag_text:
        tag_text = text_escape_XML(tag_text)
        line = '{0}<{1}>{2}</{3}>\n'.format(' ' * num_spaces, tag_name, tag_text, tag_name)
    else:
        # >> Empty tag    
        line = '{0}<{1} />\n'.format(' ' * num_spaces, tag_name)

    return line

def text_str_2_Uni(string):
    # print(type(string))
    if type(string).__name__ == 'unicode':
        unicode_str = string
    elif type(string).__name__ == 'str':
        unicode_str = string.decode('utf-8', errors = 'replace')
    else:
        print('TypeError: ' + type(string).__name__)
        raise TypeError
    # print(type(unicode_str))

    return unicode_str

# Renders a list of list of strings table into a CSV list of strings.
# The list of strings must be joined with '\n'.join()
def text_render_table_CSV_slist(table_str):
    rows = len(table_str)
    cols = len(table_str[0])
    table_str_list = []
    for i in range(1, rows):
        row_str = ''
        for j in range(cols):
            if j < cols - 1:
                row_str += '{},'.format(table_str[i][j])
            else:
                row_str += '{}'.format(table_str[i][j])
        table_str_list.append(row_str)

    return table_str_list

#
# First row            column aligment 'right' or 'left'
# Second row           column titles
# Third and next rows  table data
#
# Returns a list of strings that must be joined with '\n'.join()
#
def text_render_table_str(table_str):
    rows = len(table_str)
    cols = len(table_str[0])
    table_str_list = []
    col_sizes = text_get_table_str_col_sizes(table_str, rows, cols)
    col_padding = table_str[0]

    # --- Table header ---
    row_str = ''
    for j in range(cols):
        if j < cols - 1:
            row_str += text_print_padded_left(table_str[1][j], col_sizes[j]) + '  '
        else:
            row_str += text_print_padded_left(table_str[1][j], col_sizes[j])
    table_str_list.append(row_str)
    # >> Table -----
    total_size = sum(col_sizes) + 2*(cols-1)
    table_str_list.append('{0}'.format('-' * total_size))

    # --- Data rows ---
    for i in range(2, rows):
        row_str = ''
        for j in range(cols):
            if j < cols - 1:
                if col_padding[j] == 'right':
                    row_str += text_print_padded_right(table_str[i][j], col_sizes[j]) + '  '
                else:
                    row_str += text_print_padded_left(table_str[i][j], col_sizes[j]) + '  '
            else:
                if col_padding[j] == 'right':
                    row_str += text_print_padded_right(table_str[i][j], col_sizes[j])
                else:
                    row_str += text_print_padded_left(table_str[i][j], col_sizes[j])
        table_str_list.append(row_str)

    return table_str_list

#
# First row             column aligment 'right' or 'left'
# Second and next rows  table data
#
def text_render_table_str_NO_HEADER(table_str):
    rows = len(table_str)
    cols = len(table_str[0])
    table_str_list = []
    # >> Ignore row 0 when computing sizes.
    col_sizes = text_get_table_str_col_sizes(table_str, rows, cols)
    col_padding = table_str[0]

    # --- Data rows ---
    for i in range(1, rows):
        row_str = ''
        for j in range(cols):
            if j < cols - 1:
                if col_padding[j] == 'right':
                    row_str += text_print_padded_right(table_str[i][j], col_sizes[j]) + '  '
                else:
                    row_str += text_print_padded_left(table_str[i][j], col_sizes[j]) + '  '
            else:
                if col_padding[j] == 'right':
                    row_str += text_print_padded_right(table_str[i][j], col_sizes[j])
                else:
                    row_str += text_print_padded_left(table_str[i][j], col_sizes[j])
        table_str_list.append(row_str)

    return table_str_list

#
# Removed Kodi colour tags before computing size (substitute by ''):
#   A) [COLOR skyblue]
#   B) [/COLOR]
#
def text_get_table_str_col_sizes(table_str, rows, cols):
    col_sizes = [0] * cols
    for j in range(cols):
        col_max_size = 0
        for i in range(1, rows):
            cell_str = re.sub(r'\[COLOR \w+?\]', '', table_str[i][j])
            cell_str = re.sub(r'\[/COLOR\]', '', cell_str)
            str_size = len('{0}'.format(cell_str))
            if str_size > col_max_size: col_max_size = str_size
        col_sizes[j] = col_max_size

    return col_sizes

def text_str_list_size(str_list):
    max_str_size = 0
    for str_item in str_list:
        str_size = len('{0}'.format(str_item))
        if str_size > max_str_size: max_str_size = str_size

    return max_str_size

def text_str_dic_max_size(dictionary_list, dic_key, title_str = ''):
    max_str_size = 0
    for item in dictionary_list:
        str_size = len('{0}'.format(item[dic_key]))
        if str_size > max_str_size: max_str_size = str_size
    if title_str:
        str_size = len(title_str)
        if str_size > max_str_size: max_str_size = str_size

    return max_str_size

def text_print_padded_left(str, str_max_size):
    formatted_str = '{0}'.format(str)
    padded_str =  formatted_str + ' ' * (str_max_size - len(formatted_str))

    return padded_str

def text_print_padded_right(str, str_max_size):
    formatted_str = '{0}'.format(str)
    padded_str = ' ' * (str_max_size - len(formatted_str)) + formatted_str

    return padded_str

def text_remove_color_tags_slist(slist):
    # Iterate list of strings and remove the following tags
    # 1) [COLOR colorname]
    # 2) [/COLOR]
    #
    # Modifying list already seen is OK when iterating the list. Do not change the size of the
    # list when iterating.
    for i, s in enumerate(slist):
        modified = False
        s_temp = s

        # >> Remove [COLOR colorname]
        m = re.search('(\[COLOR \w+?\])', s_temp)
        if m:
            s_temp = s_temp.replace(m.group(1), '')
            modified = True

        # >> Remove [/COLOR]
        if s_temp.find('[/COLOR]') >= 0:
            s_temp = s_temp.replace('[/COLOR]', '')
            modified = True

        # >> Update list
        if modified:
            slist[i] = s_temp

# Some XML encoding of special characters:
#   {'\n': '&#10;', '\r': '&#13;', '\t':'&#9;'}
#
# See http://stackoverflow.com/questions/1091945/what-characters-do-i-need-to-escape-in-xml-documents
# See https://wiki.python.org/moin/EscapingXml
# See https://github.com/python/cpython/blob/master/Lib/xml/sax/saxutils.py
# See http://stackoverflow.com/questions/2265966/xml-carriage-return-encoding
#
def text_escape_XML(data_str):
    # Ampersand MUST BE replaced FIRST
    data_str = data_str.replace('&', '&amp;')
    data_str = data_str.replace('>', '&gt;')
    data_str = data_str.replace('<', '&lt;')

    data_str = data_str.replace("'", '&apos;')
    data_str = data_str.replace('"', '&quot;')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('\n', '&#10;')
    data_str = data_str.replace('\r', '&#13;')
    data_str = data_str.replace('\t', '&#9;')

    return data_str

def text_unescape_XML(data_str):
    data_str = data_str.replace('&quot;', '"')
    data_str = data_str.replace('&apos;', "'")

    data_str = data_str.replace('&lt;', '<')
    data_str = data_str.replace('&gt;', '>')
    # Ampersand MUST BE replaced LAST
    data_str = data_str.replace('&amp;', '&')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('&#10;', '\n')
    data_str = data_str.replace('&#13;', '\r')
    data_str = data_str.replace('&#9;', '\t')
    
    return data_str

#
# Unquote an HTML string. Replaces %xx with Unicode characters.
# http://www.w3schools.com/tags/ref_urlencode.asp
#
def text_decode_HTML(s):
    s = s.replace('%25', '%') # >> Must be done first
    s = s.replace('%20', ' ')
    s = s.replace('%23', '#')
    s = s.replace('%26', '&')
    s = s.replace('%28', '(')
    s = s.replace('%29', ')')
    s = s.replace('%2C', ',')
    s = s.replace('%2F', '/')
    s = s.replace('%3B', ';')
    s = s.replace('%3A', ':')
    s = s.replace('%3D', '=')
    s = s.replace('%3F', '?')

    return s

#
# Decodes HTML <br> tags and HTML entities (&xxx;) into Unicode characters.
# See https://stackoverflow.com/questions/2087370/decode-html-entities-in-python-string
#
def text_unescape_HTML(s):
    __debug_text_unescape_HTML = False
    if __debug_text_unescape_HTML:
        log_debug('text_unescape_HTML() input  "{0}"'.format(s))

    # --- Replace HTML tag characters by their Unicode equivalent ---
    s = s.replace('<br>',   '\n')
    s = s.replace('<br/>',  '\n')
    s = s.replace('<br />', '\n')

    # --- HTML entities ---
    # s = s.replace('&lt;',   '<')
    # s = s.replace('&gt;',   '>')
    # s = s.replace('&quot;', '"')
    # s = s.replace('&nbsp;', ' ')
    # s = s.replace('&copy;', '©')
    # s = s.replace('&amp;',  '&') # >> Must be done last

    # --- HTML Unicode entities ---
    # s = s.replace('&#039;', "'")
    # s = s.replace('&#149;', "•")
    # s = s.replace('&#x22;', '"')
    # s = s.replace('&#x26;', '&')
    # s = s.replace('&#x27;', "'")

    # s = s.replace('&#x101;', "ā")
    # s = s.replace('&#x113;', "ē")
    # s = s.replace('&#x12b;', "ī")
    # s = s.replace('&#x12B;', "ī")
    # s = s.replace('&#x14d;', "ō")
    # s = s.replace('&#x14D;', "ō")
    # s = s.replace('&#x16b;', "ū")
    # s = s.replace('&#x16B;', "ū")

    # >> Use HTMLParser module to decode HTML entities.
    s = HTMLParser.HTMLParser().unescape(s)

    if __debug_text_unescape_HTML:
        log_debug('text_unescape_HTML() output "{0}"'.format(s))

    return s

# Remove HTML tags from string.
def text_remove_HTML_tags(s):
    p = re.compile('<.*?>')
    s = p.sub('', s)

    return s

def text_unescape_and_untag_HTML(s):
    s = text_unescape_HTML(s)
    s = text_remove_HTML_tags(s)

    return s

def text_dump_str_to_file(filename, full_string):
    log_debug('Dumping file "{0}"'.format(filename))
    file_obj = open(filename, 'w')
    file_obj.write(full_string.encode('utf-8'))
    file_obj.close()

# -------------------------------------------------------------------------------------------------
# ROM name cleaning and formatting
# -------------------------------------------------------------------------------------------------
#
# This function is used to clean the ROM name to be used as search string for the scraper.
#
# 1) Cleans ROM tags: [BIOS], (Europe), (Rev A), ...
# 2) Substitutes some characters by spaces
#
def text_format_ROM_name_for_scraping(title):
    title = re.sub('\[.*?\]', '', title)
    title = re.sub('\(.*?\)', '', title)
    title = re.sub('\{.*?\}', '', title)
    
    title = title.replace('_', '')
    title = title.replace('-', '')
    title = title.replace(':', '')
    title = title.replace('.', '')
    title = title.strip()

    return title

#
# Format ROM file name when scraping is disabled.
# 1) Remove No-Intro/TOSEC tags (), [], {} at the end of the file
#
# title      -> Unicode string
# clean_tags -> bool
#
# Returns a Unicode string.
#
def text_format_ROM_title(title, clean_tags):
    #
    # Regexp to decompose a string in tokens
    #
    if clean_tags:
        reg_exp = '\[.+?\]\s?|\(.+?\)\s?|\{.+?\}|[^\[\(\{]+'
        tokens = re.findall(reg_exp, title)
        str_list = []
        for token in tokens:
            stripped_token = token.strip()
            if (stripped_token[0] == '[' or stripped_token[0] == '(' or stripped_token[0] == '{') and \
               stripped_token != '[BIOS]':
                continue
            str_list.append(stripped_token)
        cleaned_title = ' '.join(str_list)
    else:
        cleaned_title = title

    # if format_title:
    #     if (title.startswith("The ")): new_title = title.replace("The ","", 1)+", The"
    #     if (title.startswith("A ")): new_title = title.replace("A ","", 1)+", A"
    #     if (title.startswith("An ")): new_title = title.replace("An ","", 1)+", An"
    # else:
    #     if (title.endswith(", The")): new_title = "The "+"".join(title.rsplit(", The", 1))
    #     if (title.endswith(", A")): new_title = "A "+"".join(title.rsplit(", A", 1))
    #     if (title.endswith(", An")): new_title = "An "+"".join(title.rsplit(", An", 1))

    return cleaned_title

# -------------------------------------------------------------------------------------------------
# Multidisc ROM support
# -------------------------------------------------------------------------------------------------
def text_get_ROM_basename_tokens(basename_str):
    DEBUG_TOKEN_PARSER = False

    # --- Parse ROM base_noext/basename_str into tokens ---
    reg_exp = '\[.+?\]|\(.+?\)|\{.+?\}|[^\[\(\{]+'
    tokens_raw = re.findall(reg_exp, basename_str)
    if DEBUG_TOKEN_PARSER:
        log_debug('text_get_ROM_basename_tokens() tokens_raw   {0}'.format(tokens_raw))

    # >> Strip tokens
    tokens_strip = list()
    for token in tokens_raw: tokens_strip.append(token.strip())
    if DEBUG_TOKEN_PARSER:
        log_debug('text_get_ROM_basename_tokens() tokens_strip {0}'.format(tokens_strip))

    # >> Remove empty tokens ''
    tokens_clean = list()
    for token in tokens_strip: 
        if token: tokens_clean.append(token)
    if DEBUG_TOKEN_PARSER:        
        log_debug('text_get_ROM_basename_tokens() tokens_clean {0}'.format(tokens_clean))

    # >> Remove '-' tokens from Trurip multidisc names
    tokens = list()
    for token in tokens_clean:
        if token == '-': continue
        tokens.append(token)
    if DEBUG_TOKEN_PARSER:
        log_debug('text_get_ROM_basename_tokens() tokens       {0}'.format(tokens))

    return tokens

class MultiDiscInfo:
    def __init__(self, ROM_FN):
        self.ROM_FN      = ROM_FN
        self.isMultiDisc = False
        self.setName     = ''
        self.discName    = ROM_FN.getBase()
        self.extension   = ROM_FN.getExt()
        self.order       = 0

def text_get_multidisc_info(ROM_FN):
    MDSet = MultiDiscInfo(ROM_FN)
    
    # --- Parse ROM base_noext into tokens ---
    tokens = text_get_ROM_basename_tokens(ROM_FN.getBase_noext())

    # --- Check if ROM belongs to a multidisc set and get set name and order ---
    # Algortihm:
    # 1) Iterate list of tokens
    # 2) If a token marks a multidisk ROM extract set order
    # 3) Define the set basename by removing the multidisk token
    MultDiscFound = False
    for index, token in enumerate(tokens):
        # --- Redump ---
        matchObj = re.match(r'\(Dis[ck] ([0-9]+)\)', token)
        if matchObj:
            log_debug('text_get_multidisc_info() ### Matched Redump multidisc ROM ###')
            tokens_idx = range(0, len(tokens))
            tokens_idx.remove(index)
            tokens_nodisc_idx = list(tokens_idx)
            tokens_mdisc = [tokens[x] for x in tokens_nodisc_idx]
            MultDiscFound = True
            break

        # --- TOSEC/Trurip ---
        matchObj = re.match(r'\(Dis[ck] ([0-9]+) of ([0-9]+)\)', token)
        if matchObj:
            log_debug('text_get_multidisc_info() ### Matched TOSEC/Trurip multidisc ROM ###')
            tokens_idx = range(0, len(tokens))
            tokens_idx.remove(index)
            tokens_nodisc_idx = list(tokens_idx)
            # log_debug('text_get_multidisc_info() tokens_idx         = {0}'.format(tokens_idx))
            # log_debug('text_get_multidisc_info() index              = {0}'.format(index))
            # log_debug('text_get_multidisc_info() tokens_nodisc_idx  = {0}'.format(tokens_nodisc_idx))
            tokens_mdisc = [tokens[x] for x in tokens_nodisc_idx]
            MultDiscFound = True
            break

    if MultDiscFound:
        MDSet.isMultiDisc = True
        MDSet.setName = ' '.join(tokens_mdisc) + MDSet.extension
        MDSet.order = int(matchObj.group(1))
        log_debug('text_get_multidisc_info() base_noext   "{0}"'.format(ROM_FN.getBase_noext()))
        log_debug('text_get_multidisc_info() tokens       {0}'.format(tokens))
        log_debug('text_get_multidisc_info() tokens_mdisc {0}'.format(tokens_mdisc))
        log_debug('text_get_multidisc_info() setName      "{0}"'.format(MDSet.setName))
        log_debug('text_get_multidisc_info() discName     "{0}"'.format(MDSet.discName))
        log_debug('text_get_multidisc_info() extension    "{0}"'.format(MDSet.extension))
        log_debug('text_get_multidisc_info() order        {0}'.format(MDSet.order))

    return MDSet

# -------------------------------------------------------------------------------------------------
# URLs
# -------------------------------------------------------------------------------------------------
#
# Get extension of URL. Returns '' if not found. Examples: 'png', 'jpg', 'gif'.
#
def text_get_URL_extension(url):
    path = urlparse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    if ext[0] == '.': ext = ext[1:] # Remove initial dot

    return ext

#
# Defaults to 'jpg' if URL extension cannot be determined
#
def text_get_image_URL_extension(url):
    path = urlparse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    if ext[0] == '.': ext = ext[1:] # Remove initial dot
    ret = 'jpg' if ext == '' else ext

    return ret

# -------------------------------------------------------------------------------------------------
# File cache
# -------------------------------------------------------------------------------------------------
file_cache = {}
def misc_add_file_cache(dir_str):
    global file_cache

    # >> Create a set with all the files in the directory
    if not dir_str:
        log_debug('misc_add_file_cache() Empty dir_str. Exiting')
        return
    dir_FN = FileName(dir_str)
    # log_debug('misc_add_file_cache() Scanning OP "{0}"'.format(dir_FN.getOriginalPath()))
    log_debug('misc_add_file_cache() Scanning  P "{0}"'.format(dir_FN.getPath()))
    file_list = os.listdir(dir_FN.getPath())
    file_set = set(file_list)
    # for file in file_set: log_debug('File "{0}"'.format(file))
    log_debug('misc_add_file_cache() Adding {0} files to cache'.format(len(file_set)))
    file_cache[dir_str] = file_set

#
# See misc_look_for_file() documentation below.
#
def misc_search_file_cache(dir_str, filename_noext, file_exts):
    # log_debug('misc_search_file_cache() Searching in  "{0}"'.format(dir_str))
    current_cache_set = file_cache[dir_str]
    for ext in file_exts:
        file_base = filename_noext + '.' + ext
        # log_debug('misc_search_file_cache() file_Base = "{0}"'.format(file_base))
        if file_base in current_cache_set:
            # log_debug('misc_search_file_cache() Found in cache')
            return FileName(dir_str).pjoin(file_base)

    return None

# -------------------------------------------------------------------------------------------------
# Misc stuff
# -------------------------------------------------------------------------------------------------
#
# Given the image path, image filename with no extension and a list of file extensions search for 
# a file.
#
# rootPath       -> FileName object
# filename_noext -> Unicode string
# file_exts      -> list of extenstions with no dot [ 'zip', 'rar' ]
#
# Returns a FileName object if a valid filename is found.
# Returns None if no file was found.
#
def misc_look_for_file(rootPath, filename_noext, file_exts):
    for ext in file_exts:
        file_path = rootPath.pjoin(filename_noext + '.' + ext)
        if file_path.exists():
            return file_path

    return None

#
# Generates a random an unique MD5 hash and returns a string with the hash
#
def misc_generate_random_SID():
    t1 = time.time()
    t2 = t1 + random.getrandbits(32)
    base = hashlib.md5( str(t1 + t2) )
    sid = base.hexdigest()

    return sid

#
# Lazy function (generator) to read a file piece by piece. Default chunk size: 8k.
#
def misc_read_file_in_chunks(file_object, chunk_size = 8192):
    while True:
        data = file_object.read(chunk_size)
        if not data: break
        yield data

#
# Calculates CRC, MD5 and SHA1 of a file in an efficient way.
# Returns a dictionary with the checksums or None in case of error.
#
# https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
# https://stackoverflow.com/questions/1742866/compute-crc-of-file-in-python 
#
def misc_calculate_file_checksums(full_file_path):
    log_debug('Computing checksums "{}"'.format(full_file_path))
    try:
        f = open(full_file_path, 'rb')
        crc_prev = 0
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        for piece in misc_read_file_in_chunks(f):
            crc_prev = zlib.crc32(piece, crc_prev)
            md5.update(piece)
            sha1.update(piece)
        crc_digest = '{:08X}'.format(crc_prev & 0xFFFFFFFF)
        md5_digest = md5.hexdigest()
        sha1_digest = sha1.hexdigest()
        size = os.path.getsize(full_file_path)
    except:
        log_debug('(Exception) In misc_calculate_file_checksums()')
        log_debug('Returning None')
        return None
    checksums = {
        'crc'  : crc_digest.upper(),
        'md5'  : md5_digest.upper(),
        'sha1' : sha1_digest.upper(),
        'size' : size,
    }

    return checksums

# This function not finished yet.
def misc_read_bytes_in_chunks(file_bytes, chunk_size = 8192):
    file_length = len(file_bytes)
    block_number = 0
    while True:
        start_index = None
        end_index = None
        data = file_bytes[start_index:end_index]
        yield data

def misc_calculate_stream_checksums(file_bytes):
    log_debug('Computing checksums of bytes stream...'.format(len(file_bytes)))
    crc_prev = 0
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    # Process bytes stream block by block
    # for piece in misc_read_bytes_in_chunks(file_bytes):
    #     crc_prev = zlib.crc32(piece, crc_prev)
    #     md5.update(piece)
    #     sha1.update(piece)
    # Process bytes in one go
    crc_prev = zlib.crc32(file_bytes, crc_prev)
    md5.update(file_bytes)
    sha1.update(file_bytes)
    crc_digest = '{:08X}'.format(crc_prev & 0xFFFFFFFF)
    md5_digest = md5.hexdigest()
    sha1_digest = sha1.hexdigest()
    size = len(file_bytes)

    checksums = {
        'crc'  : crc_digest.upper(),
        'md5'  : md5_digest.upper(),
        'sha1' : sha1_digest.upper(),
        'size' : size,
    }

    return checksums

# Replace an item in dictionary. If dict_in is an OrderedDict then keep original order.
# Returns a dict or OrderedDict
def misc_replace_fav(dict_in, old_item_key, new_item_key, new_value):
    if type(dict_in) is dict:
        dict_in.pop(old_item_key)
        dict_in[new_item_key] = new_value
        return dict_in
    elif type(dict_in) is collections.OrderedDict:
        # In this case create a new OrderedDict to respect original order.
        # This implementation is slow and naive but I don't care, OrderedDict are only use
        # when editing ROM Collections.
        dict_out = collections.OrderedDict()
        for key in dict_in:
            if key == old_item_key:
                dict_out[new_item_key] = new_value
            else:
                dict_out[key] = dict_in[key]
        return dict_out
    else:
        raise TypeError

# -------------------------------------------------------------------------------------------------
# Filesystem helper class
# This class always takes and returns Unicode string paths. Decoding to UTF-8 must be done in
# caller code.
# A) Transform paths like smb://server/directory/ into \\server\directory\
# B) Use xbmc.translatePath() for paths starting with special://
# -------------------------------------------------------------------------------------------------
class FileName:
    # pathString must be a Unicode string object
    def __init__(self, pathString):
        self.originalPath = pathString
        self.path         = pathString
        
        # --- Path transformation ---
        if self.originalPath.lower().startswith('smb:'):
            self.path = self.path.replace('smb:', '')
            self.path = self.path.replace('SMB:', '')
            self.path = self.path.replace('//', '\\\\')
            self.path = self.path.replace('/', '\\')

        elif self.originalPath.lower().startswith('special:'):
            self.path = xbmc.translatePath(self.path)

    def _join_raw(self, arg):
        self.path         = os.path.join(self.path, arg)
        self.originalPath = os.path.join(self.originalPath, arg)

        return self

    # Appends a string to path. Returns self FileName object
    def append(self, arg):
        self.path         = self.path + arg
        self.originalPath = self.originalPath + arg

        return self

    # >> Joins paths. Returns a new FileName object
    def pjoin(self, *args):
        child = FileName(self.originalPath)
        for arg in args:
            child._join_raw(arg)

        return child

    # Behaves like os.path.join()
    #
    # See http://blog.teamtreehouse.com/operator-overloading-python
    # other is a FileName object. other originalPath is expected to be a subdirectory (path
    # transformation not required)
    def __add__(self, other):
        current_path = self.originalPath
        if type(other) is FileName:  other_path = other.originalPath
        elif type(other) is unicode: other_path = other
        elif type(other) is str:     other_path = other.decode('utf-8')
        else: raise NameError('Unknown type for overloaded + in FileName object')
        new_path = os.path.join(current_path, other_path)
        child    = FileName(new_path)

        return child

    def escapeQuotes(self):
        self.path = self.path.replace("'", "\\'")
        self.path = self.path.replace('"', '\\"')

    # ---------------------------------------------------------------------------------------------
    # Decomposes a file name path or directory into its constituents
    #   FileName.getOriginalPath()  Full path                                     /home/Wintermute/Sonic.zip
    #   FileName.getPath()          Full path                                     /home/Wintermute/Sonic.zip
    #   FileName.getPath_noext()    Full path with no extension                   /home/Wintermute/Sonic
    #   FileName.getDir()           Directory name of file. Does not end in '/'   /home/Wintermute/
    #   FileName.getBase()          File name with no path                        Sonic.zip
    #   FileName.getBase_noext()    File name with no path and no extension       Sonic
    #   FileName.getExt()           File extension                                .zip
    # ---------------------------------------------------------------------------------------------
    def getOriginalPath(self):
        return self.originalPath

    def getPath(self):
        return self.path

    def getPath_noext(self):
        root, ext = os.path.splitext(self.path)

        return root

    def getDir(self):
        return os.path.dirname(self.path)

    def getBase(self):
        return os.path.basename(self.path)

    def getBase_noext(self):
        basename  = os.path.basename(self.path)
        root, ext = os.path.splitext(basename)
        
        return root

    def getExt(self):
        root, ext = os.path.splitext(self.path)
        
        return ext

    # ---------------------------------------------------------------------------------------------
    # Scanner functions
    # ---------------------------------------------------------------------------------------------
    def scanFilesInPath(self, mask):
        files = []
        filenames = os.listdir(self.path)
        for filename in fnmatch.filter(filenames, mask):
            files.append(os.path.join(self.path, filename))

        return files

    def scanFilesInPathAsPaths(self, mask):
        files = []
        filenames = os.listdir(self.path)
        for filename in fnmatch.filter(filenames, mask):
            files.append(FileName(os.path.join(self.path, filename)))

        return files

    def recursiveScanFilesInPath(self, mask):
        files = []
        for root, dirs, foundfiles in os.walk(self.path):
            for filename in fnmatch.filter(foundfiles, mask):
                files.append(os.path.join(root, filename))

        return files

    # ---------------------------------------------------------------------------------------------
    # Filesystem functions
    # ---------------------------------------------------------------------------------------------
    def stat(self):
        return os.stat(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def isdir(self):
        return os.path.isdir(self.path)
        
    def isfile(self):
        return os.path.isfile(self.path)

    def makedirs(self):
        if not os.path.exists(self.path): 
            os.makedirs(self.path)

    # os.remove() and os.unlink() are exactly the same.
    def unlink(self):
        os.unlink(self.path)

    def rename(self, to):
        os.rename(self.path, to.getPath())

# -------------------------------------------------------------------------------------------------
# Utilities to test scrapers
# -------------------------------------------------------------------------------------------------
# Candidates
NAME_L      = 65
SCORE_L     = 5
ID_L        = 55
PLATFORM_L  = 20
SPLATFORM_L = 20
URL_L       = 70

# Metadata
TITLE_L     = 50
YEAR_L      = 4
GENRE_L     = 20
DEVELOPER_L = 10
NPLAYERS_L  = 10
ESRB_L      = 20
PLOT_L      = 70

# Assets
ASSET_ID_L        = 10
ASSET_NAME_L      = 60
ASSET_URL_THUMB_L = 100

# PUT functions to print things returned by Scraper object (which are common to all scrapers)
# into util.py, to be resused by all scraper tests.
def print_candidate_list(results):
    p_str = "{0} {1} {2} {3} {4}"
    print('Found {0} candidate/s'.format(len(results)))
    print(p_str.format(
        'Display name'.ljust(NAME_L), 'Score'.ljust(SCORE_L),
        'Id'.ljust(ID_L), 'Platform'.ljust(PLATFORM_L), 'SPlatform'.ljust(SPLATFORM_L)))
    print(p_str.format(
        '-'*NAME_L, '-'*SCORE_L, '-'*ID_L, '-'*PLATFORM_L, '-'*SPLATFORM_L))
    for game in results:
        display_name = text_limit_string(game['display_name'], NAME_L)
        score = text_limit_string(str(game['order']), SCORE_L)
        id = text_limit_string(str(game['id']), ID_L)
        platform = text_limit_string(str(game['platform']), PLATFORM_L)
        splatform = text_limit_string(str(game['scraper_platform']), SPLATFORM_L)
        print(p_str.format(
            display_name.ljust(NAME_L), score.ljust(SCORE_L), id.ljust(ID_L),
            platform.ljust(PLATFORM_L), splatform.ljust(SPLATFORM_L)))
    print('')

def print_game_metadata(metadata):
    title     = text_limit_string(metadata['title'], TITLE_L)
    year      = metadata['year']
    genre     = text_limit_string(metadata['genre'], GENRE_L)
    developer = text_limit_string(metadata['developer'], DEVELOPER_L)
    nplayers  = text_limit_string(metadata['nplayers'], NPLAYERS_L)
    esrb      = text_limit_string(metadata['esrb'], ESRB_L)
    plot      = text_limit_string(metadata['plot'], PLOT_L)

    p_str = "{0} {1} {2} {3} {4} {5} {6}"
    print('Displaying metadata for title "{0}"'.format(title))
    print(p_str.format(
        'Title'.ljust(TITLE_L), 'Year'.ljust(YEAR_L), 'Genre'.ljust(GENRE_L),
        'Developer'.ljust(DEVELOPER_L), 'NPlayers'.ljust(NPLAYERS_L), 'ESRB'.ljust(ESRB_L),
        'Plot'.ljust(PLOT_L)))
    print(p_str.format(
        '-'*TITLE_L, '-'*YEAR_L, '-'*GENRE_L, '-'*DEVELOPER_L, '-'*NPLAYERS_L, '-'*ESRB_L, '-'*PLOT_L))
    print(p_str.format(
        title.ljust(TITLE_L), year.ljust(YEAR_L), genre.ljust(GENRE_L), developer.ljust(DEVELOPER_L),
        nplayers.ljust(NPLAYERS_L), esrb.ljust(ESRB_L), plot.ljust(PLOT_L) ))
    print('')

def print_game_assets(image_list):
    # print('Found {0} image/s'.format(len(image_list)))
    p_str = "{0} {1} {2}"
    print(p_str.format(
        'Asset ID'.ljust(ASSET_ID_L), 'Name'.ljust(ASSET_NAME_L),
        'URL thumb'.ljust(ASSET_URL_THUMB_L)))
    print(p_str.format('-'*ASSET_ID_L, '-'*ASSET_NAME_L, '-'*ASSET_URL_THUMB_L))
    for image in image_list:
        id           = text_limit_string(str(image['asset_ID']), ASSET_ID_L)
        display_name = text_limit_string(image['display_name'], ASSET_NAME_L)
        url_thumb    = text_limit_string(image['url_thumb'], ASSET_URL_THUMB_L)
        print(p_str.format(
            id.ljust(ASSET_ID_L), display_name.ljust(ASSET_NAME_L),
            url_thumb.ljust(ASSET_URL_THUMB_L)))
    print('')
