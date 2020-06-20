import voicerss_tts

voice = voicerss_tts.speech({
    'key': '26446b3244ee4f96aada13c3a94da441',
    'hl': 'ru-ru',
    'src': 'Привет дорогой и любимый мир!',
    'r': '0',
    'c': 'mp3',
    'f': '44khz_16bit_stereo',
    'ssml': 'false',
    'b64': 'false'
})

with open('text_to_speech/outputfile.mp3', 'wb') as f:
    f.write(voice['response'])
f.close()
