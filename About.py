import sys

import wx                  # This module uses the new wx namespace
import wx.html
import wx.lib.wxpTag
from subdown_version import __version__
#---------------------------------------------------------------------------

class MyAboutBox(wx.Dialog):
    text = '''
<html>
<body bgcolor="#AC76DE">
<center><table bgcolor="#458154" width="100%%" cellspacing="0"
cellpadding="0" border="1">
<tr>
    <td align="center">
    <h1>SubDown %s</h1>
    Compiled against Python %s<br>
    </td>
</tr>
</table>

<p><b>SubDown</b> is a Python Application for downloading <br>Subtitles for Movies and Serials.</p>

<p>Visit  <b>https://sainyamkapoor.github.io/subdown</b> for more info and to download updated version.</p>

<p><b>SubDown</b> is brought to you by <b>Sainyam Kapoor</b> <br>Copyright (c) 2014.</p>

<p><br>
<font size="-1">Please see <i>license.txt</i> for licensing information.</font>
</p>

<p><wxp module="wx" class="Button">
    <param name="label" value="Okay">
    <param name="id"    value="ID_OK">
</wxp></p>
</center>
</body>
</html>
'''
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About the Subdown '+__version__,)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        py_version = sys.version.split()[0]
        txt = self.text % (__version__,
                           #", ".join(wx.PlatformInfo[1:]),
                           py_version
                           )
        html.SetPage(txt)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------



if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = MyAboutBox(None)
    dlg.ShowModal()
   # dlg.Destroy()
    app.MainLoop()

