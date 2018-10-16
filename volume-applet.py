#!/usr/bin/env python

import pulsectl
import argparse


from subprocess import call


pulse = pulsectl.Pulse('headphones')

parser = argparse.ArgumentParser(description="A pulseaudio control script")

parser.add_argument('--raisevol','-r', default=False, type=float,
        help="decimal value to raise volume (0.01-1.00)",required=False)
parser.add_argument('--lowervol','-l', default=False, type=float,
        help="decimal value to lower volume (0.01-1.00)",required=False)
parser.add_argument('--mute', '-m', default=False, action='store_true',
        help="toggle mute",required=False)
parser.add_argument('--volume', '-v',default=False, action='store_true',
        help="return current volume",required=False)
parser.add_argument('--change','-c',default=False, action='store_true',
        help="change audio output device",required=False)
parser.add_argument('--printvol','-p',default=False, action='store_true',
        help="print volume",required=False)

args = parser.parse_args()

icons = {
        'mute': '',
        'low': '',
        'med': '',
        'high': '',
        }

with open('config', 'r') as f:
    headphones = f.readline().strip()

def signalBar():
    call(['pkill', '-RTMIN+1', 'i3blocks'])

def getSink(device):
    for sink in pulse.sink_list():
        if headphones in str(sink):
            return sink

def raiseVolume(sink, vol=0.05):
    if checkMute(sink):
        unmute(sink)
    if (int(getVolume(sink)[:-1]) + vol*100) > 100:
        maxIncrease = (100 - (int(getVolume(sink)[:-1])))/100
        if maxIncrease >= 0:
            pulse.volume_change_all_chans(sink, +maxIncrease)
            signalBar()
    else:
        pulse.volume_change_all_chans(sink, +vol)
        signalBar()

def lowerVolume(sink, vol=0.05):
    if checkMute(sink):
        unmute(sink)
    pulse.volume_change_all_chans(sink, -vol)
    signalBar()

def checkMute(sink):
    index = str(sink).find('mute=')
    muted = str(sink)[index+5]
    if muted == '0':
        return False
    else:
        return True

def mute(sink):
    pulse.mute(sink)
    signalBar()

def unmute(sink):
    pulse.mute(sink, 0)
    signalBar()

def showVolume(sink):
    if checkMute(sink):
        return icons['mute']
    else:
        visual = int(getVolume(sink)[:-1])//10
        remainder = 10 - visual
        if visual <= 3:
            icon = icons['low']
        elif visual >= 4 and visual <= 6:
            icon = icons['med']
        else:
            icon = icons['high']
        show = icon + getVolume(sink)
        return show
    

def getVolume(sink):
    index = str(sink.volume).find('[')
    channels = str(sink.volume)[index+1:-1].split(' ')
    if channels[0] == channels[1]:
        return channels[0]
    else:
        vol = channels[0][:-1]
        vol = '0.' + vol
        pulse.set_all_chans(sink, vol)
        return channels[0]

sink = getSink(headphones)

if args.raisevol:
    raiseVolume(sink, args.raisevol)
if args.lowervol:
    lowerVolume(sink, args.lowervol)
if args.mute:
    if checkMute(sink):
        unmute(sink)
    else:
        mute(sink)
if args.volume:
    print(getVolume(sink))
if args.change:
    with open('headphones', 'w') as f:
        f.write(args.change)
if args.printvol:
    print(showVolume(sink))

pulse.close()
