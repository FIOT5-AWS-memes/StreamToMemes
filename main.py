#################################################################
#
#                       STREAM TO MEMES
#
#   This program generates a meme from a YouTube livestream
#   with a caption based off keywords typed-in by the user.
#
#   Made as part of the 5th Future Iot summer school in Berlin.
#   https://future-iot.org/
#   
#   Please install requirements and read the README.txt
#
#
#################################################################

import wx
import pls_meme
import video_stream_data

class ImagePanel(wx.Panel):
    """
    This is the class of the graphical user interface.
    The library we use is wxPython.
    """

    url = "https://www.youtube.com/"
    keywords = []
    outputPath = "img/out_meme.png"

    def __init__(self, parent, image_size):
        super().__init__(parent)
        self.max_size = 600

        img = wx.Image(*image_size)
        self.image_ctrl = wx.StaticBitmap(self, 
                                          bitmap=wx.Bitmap(img))

        meme_btn            = wx.Button(self, label='plsMeme')
        meme_btn.Bind(wx.EVT_BUTTON, self.please_meme)

        title               = wx.StaticText(self, label ="Stream to Memes")
        #   title font
        font = title.GetFont()
        font.PointSize += 10
        font = font.Bold()
        title.SetFont(font)

        hsizer              = wx.BoxSizer(wx.HORIZONTAL)

        #   URL type box
        url_title           = wx.StaticText(self, -1, "Stream URL (hit ENTER)")  
        self.url_text_field = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER,
                               size=(300, 20))
        self.url_text_field.SetFocus()
        self.url_text_field.Bind(wx.EVT_TEXT_ENTER,self.UrlOnEnterPressed)

        #   keyword selection
        keyword_title       = wx.StaticText(self, -1, "Type in keywords separated with spaces (hit ENTER)")
        self.kw_text_field  = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER,
                                size=(300, 20))
        self.kw_text_field.Bind(wx.EVT_TEXT_ENTER, self.KeywordOnEnterPressed)

        #   image field
        self.photo_txt      = wx.TextCtrl(self, size=(200, -1))

        """
        sizers
        """
        #   sizer creation
        main_sizer          = wx.BoxSizer(wx.VERTICAL)
        usizer              = wx.BoxSizer(wx.HORIZONTAL)
        ksizer              = wx.BoxSizer(wx.HORIZONTAL)
        hsizer              = wx.BoxSizer(wx.HORIZONTAL)

        #   sizer properties
        main_sizer.Add(title, proportion=0,
                        flag=wx.ALL | wx.ALIGN_CENTER,
                        border=5)
        usizer.Add(url_title, 1,wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,5)
        usizer.Add(self.url_text_field, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 0)
        ksizer.Add(keyword_title, 1,wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,5)
        ksizer.Add(self.kw_text_field, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 0)

        main_sizer.Add(usizer, 0, wx.ALL, 5)
        main_sizer.Add(ksizer, 0, wx.ALL, 5)
        main_sizer.Add(self.image_ctrl, 0, wx.ALL, 5)
        hsizer.Add(meme_btn, 0, wx.ALL, 5)
        hsizer.Add(self.photo_txt, 0, wx.ALL, 5)
        main_sizer.Add(hsizer, 0, wx.ALL, 5)

        self.SetSizer(main_sizer)
        main_sizer.Fit(parent)
        self.Layout()

    """
    actions of the buttons and text field
    """

    #   change attribute value (URL)
    def change_attribute(self, name, value):
        attribute = getattr(self, name)
        setattr(self, name, attribute)

    #    URL text field action            
    def UrlOnEnterPressed(self,event):
        stream_url = event.GetString()
        setattr(self, "url", stream_url)

    def KeywordOnEnterPressed(self, event):
        # we get the weywords as a string of words separated with spaces
        # we parse it to get the keywords
        keyword_string = event.GetString()
        keyword_string_split = keyword_string.split(' ')
        keyword_string_clean = list(filter(('').__ne__, keyword_string_split))
        setattr(self, "keywords", keyword_string_clean)

    #   meme generation algorithm
    def please_meme(self, event):
        self.load_image() # loads the image
    
    #   loading of the image
    def load_image(self):
        """
        Run the creating of a meme
        Parts of this code come the following tutorial:
        https://www.blog.pythonlibrary.org/2021/09/29/create-gui/
        """

        #   process the livestream
        (key_chunk_list, title, path) = video_stream_data.get_video_stream_data(self.url, self.keywords)
        caption = key_chunk_list[0]

        #   create the meme
        filepath = pls_meme.plsMeme(path, title, caption, self.outputPath)
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        
        #   scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.max_size
            NewH = self.max_size * H / W
        else:
            NewH = self.max_size
            NewW = self.max_size * W / H
        img = img.Scale(int(NewW),int(NewH))
        
        self.image_ctrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()

class MainFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='Stream To Memes')
        panel = ImagePanel(self, image_size=(500,500))
        self.Show()

if __name__ == '__main__':
    """
    Launches an infinite loop that will create a meme
    when it is matched in the audio stream of the videostream.
    """
    app = wx.App(redirect=False)
    frame = MainFrame()
    app.MainLoop()