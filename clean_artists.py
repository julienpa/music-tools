#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import sys

from mutagen.id3 import TIT2, TPE1
import mutagen

# initial checks to see if correct params have been supplied
if len(sys.argv) < 2 or len(sys.argv[1]) == 0:
    print('Params error, usage: `%s ~/Documents/folder/`' % os.path.splitext(os.path.basename(__file__))[0])
    exit()

music_folder = sys.argv[1]
print('Folder:', music_folder)

if music_folder[-1:] != '/':
    print('Folder must end with `/`')
    exit()

renamed = 0
files = glob.glob(music_folder + '*.mp3')
print('Files: %s to process\n' % len(files))

for filename in files:
    file = mutagen.File(filename)

    # initial values
    title = file.tags.getall('TIT2')[0].text[0]
    artist = file.tags.getall('TPE1')[0].text[0]

    # transform values
    if 'feat.' not in artist:
        continue
    new_title = title + ' (feat. ' + artist.split('feat.')[1].strip() + ')'
    new_artist = artist.split('feat.')[0].strip()
    print(new_title)
    renamed += 1

    # update file
    file.tags.add(TIT2(text=[new_title]))
    file.tags.add(TPE1(text=[new_artist]))
    file.save()

print('\nRenamed %s files' % renamed)
