import wx
import wx.html2 as webview

username = "" # Identifiant ENT
password = "" # Mot de passe ENT
homePage = "http://www.labeli.org/" # Adresse URL valide. HTTPS interdit !

class WebPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.current = homePage
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        self.Bind(webview.EVT_WEBVIEW_ERROR, self.OnWebViewError, self.wv)
        self.Bind(webview.EVT_WEBVIEW_NEWWINDOW, self.OnWebViewNewWindow, self.wv)

        self.location = wx.TextCtrl(self, -1, "Start")
        btnSizer.Add(self.location, 1, wx.EXPAND)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.wv.LoadURL(self.current)

    def OnWebViewLoaded(self, evt):
        self.current = evt.GetURL()
        self.location.SetValue(self.current)
        urlSplitted = evt.GetURL().split('/')
        if len(urlSplitted) > 2 :
            if urlSplitted[2] == 'gw6.infra.univ-bordeaux.fr' :
                self.wv.RunScript("var links = document.getElementsByTagName('a');" +
                                  "location.href = links[6].href;")
            elif urlSplitted[2] == 'wayf.id.univ-bordeaux.fr' :
                self.wv.RunScript("var form = document.getElementById('IdPList');" +
                                  "var options = form.getElementsByTagName('option');" +
                                  "for(var i = 0; i < options.length ; i++)" +
                                  "{" +
                                  "if(options[i].value == '-'){options[i].removeAttribute('selected');}" +
                                  "else if(options[i].value == 'https://idp.u-bordeaux.fr/idp_ubx/shibboleth'){options[i].setAttribute('selected','selected');}" +
                                  "}" +
                                  "var remember = document.getElementById('rememberForSession');" +
                                  "remember.setAttribute('checked','checked');" +
                                  "form.submit();")
            elif urlSplitted[2] == 'cas.u-bordeaux.fr' :
                self.wv.RunScript("var formENT = document.getElementById('fm1');" +
                                  "var username = document.getElementById('username');" +
                                  "var password = document.getElementById('password');" +
                                  "username.value = '" + username + "';" +
                                  "password.value = '" + password + "';" +
                                  "formENT.submit.click();")

    def OnWebViewNewWindow(self, evt):
        self.wv.LoadURL(evt.GetURL())
        
           
    def OnWebViewError(self,evt):
        self.wv.LoadURL(homePage)
        
class WebFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Connexion Reaumur")
        panel = WebPanel(self)
        self.Show()
    
if __name__ == "__main__":
    app = wx.App(False)
    frame = WebFrame()
    app.MainLoop()
