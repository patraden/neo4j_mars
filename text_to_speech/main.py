import sys
sys.path.append('/app/text_to_speech/')
import voicerss_tts

def application(environ, start_response):
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
#    with open('/app/text_to_speech/outputfile.mp3', 'wb') as f:
#        f.write(voice['response'])
#    f.close()
    status = '200 OK'
    output = voice['response']
    response_headers = [('Content-type', 'audio/mpeg'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]