import os
import speech_recognition as sr
import spacy
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs 
import _ssl

"""
FOR PRESENTATION:
splitting speech text into sentences doesn't work well, because there's no punctuation --> tried it but didn't continue with that approach
using noun chunks instead
"""

def get_video_stream_data(url, keyword_list): 
    """
    input: youtube video stream
    output: text (of youtube title and noun_chunks containing keywords) and image of corresponding videoclip
    Explanation: 
    1) access the video using ffmpeg and youtube_dl and saving it as 30sec mp4 clips, extract audio from each clip and save 
    2) call speech to text function, if speech to text finds keyword --> call aws face recognition function and sent result (text and image) back to main, else just continue (no feedback to frontend)
    """
    # currently set to run for 10min max -> 20 i 
    i = 0
    while (i<20):
        i=i+1
        print ("video {}".format(i))
        ### 1) access the video using ffmpeg and youtube_dl
        """
        ss: starting second - starts at second 5 --> why? we loose 5 seconds each loop?
        t: stops writing the output after x seconds - stops at second 30 - so because this the code is repeated every 30 seconds
        f: Video format code, downloads a specific format from YouTube --> if not used, youtube chooses best --> seems to work well here
        """
        # accessing the videostream on youtube and saving it locally in chunks of 30seconds  
        os.system('ffmpeg -ss 00:00:0.00 -i $(youtube-dl -g --no-check-certificate {}) -t 00:00:30.00 -c copy intermediate_output/video/video_{}.mp4'.format(url, i))
        # extract the audio from the video
        os.system('ffmpeg -i intermediate_output/video/video_{}.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 intermediate_output/audio/audio_{}.wav'.format(i, i))

        ### 2) call speech to text function
        ret =_speech_text_nlp(url, keyword_list, i)
        if ret is None:
            print("None was returned")
            continue
        return ret
        """
        key_chunk_list, title_string, img = ret
        if len(key_chunk_list) == 0:
            pass
        else:
            return (key_chunk_list, title_string, img) 
        
        else:
            # remove the video, audio and image after finishing to proces them
            os.remove('intermediate_output/video/video_{}.mp4'.format(i))
            os.remove('intermediate_output/audio/audio_{}.wav'.format(i))
            os.remove('intermediate_output/image/img_{}.jpeg'.format(i))
        """

def _speech_text_nlp(url, keyword_list, i): 
    """
    input: 30 sec audio clip [.wav]
    output: text [str] (of youtube title and noun_chunks containing keywords)
    Explanation: 
    1) transcripe speech to text
    2) check if noun chunks containing keywords where mentioned
    3) if 2) == true: 3.1) extract youtube title, add to meaningful noun_chunks and return as text output; 3.2) call aws image creation function, returning image from corresponding clip
    """
    ### 1) transcripe speech to text
    # initialize the recognizer
    r = sr.Recognizer()
    filename = 'intermediate_output/audio/audio_{}.wav'.format(i)
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
        except:
            text = ""
    ### 2) check if noun chunks containing keywords where mentioned
    '''
    - 1st splitting text into noun chunks for hashtags - a bit better than individual words but too short for actal context understanding --> used together with youtube title
    Example output noun chunks: "Europe, particularly the UK, the whole, the Europeans, you, policy intervention, the physical side, the bond Market,..."
    - 2nd search list of noun chunks for given keywords and extract those mentioned keyword chunks for hashtags of post
    Example output: 'particularly the UK', 'policy intervention'
    '''

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text) 
    key_chunk_list= []
    for chunk in doc.noun_chunks:
        for token in chunk: 
            if (token.text in keyword_list):
                key_chunk_list.append(chunk.text.strip())
    ### 3) if speech to text finds keyword --> call aws face recognition function and sent result (text and image) back to main, else just continue (no feedback to frontend)
    if len(key_chunk_list) == 0:
        print ("video_{}.mp4 does not mention a keyword".format(i))
        return None
    else: 
        ### 3.1) extract youtube title, add to meaningful noun_chunks and return as text output
        title_string = _youtube_title_text(url)
        ### 3.2) call aws image creation function, returning image from corresponding clip
        # get a screenshot in second 20 of each video - !!!this is only a placeholder!!! --> face recognition to come in here
        os.system('ffmpeg -i intermediate_output/video/video_{}.mp4 -ss 00:00:20 -frames:v 1 intermediate_output/image/img_{}.jpeg'.format(i, i))
        img = 'intermediate_output/image/img_{}.jpeg'.format(i)
        return (key_chunk_list, title_string, img)


def _youtube_title_text(url): 
    ### grab youtube title from stream link to add as text for the post
    # init an HTML Session
    session = HTMLSession()
    # get the html content
    response = session.get(url)
    # execute Java-script
    response.html.render(timeout=20)
    # create bs object to parse HTML
    soup = bs(response.html.html, "html.parser")
    title_string = soup.find("meta", itemprop="name")["content"]
    return title_string
