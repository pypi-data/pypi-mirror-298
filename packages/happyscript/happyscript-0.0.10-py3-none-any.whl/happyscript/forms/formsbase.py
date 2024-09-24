import wx
import wx.xrc
import wx.aui
ID_BTN_TESTLIST = 1000
ID_BTN_MESSAGES = 1001
ID_BTN_LOGGING = 1002
ID_BTN_SCRIPTS = 1003
ID_BTN_PYTHON = 1004
ID_BTN_CONTROLS = 1005
ID_BTN_CHARTS = 1006
class FormMain_Base ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"HappyScript -", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow( self )
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_ALLOW_FLOATING|wx.aui.AUI_MGR_RECTANGLE_HINT|wx.aui.AUI_MGR_TRANSPARENT_HINT)
        self.m_guiTimer = wx.Timer()
        self.m_guiTimer.SetOwner( self, wx.ID_ANY )
        self.m_mnuToolbar = wx.aui.AuiToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_TB_TEXT )
        self.m_mnuToolbar.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_mnuToolbar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_btnLayout = self.m_mnuToolbar.AddTool( wx.ID_ANY, u"User", wx.ArtProvider.GetBitmap( "layout_DD",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_mnuToolbar.AddSeparator()
        self.m_btnTestList = self.m_mnuToolbar.AddTool( ID_BTN_TESTLIST, u"Tests", wx.ArtProvider.GetBitmap( "tests",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_btnMessages = self.m_mnuToolbar.AddTool( ID_BTN_MESSAGES, u"Messages", wx.ArtProvider.GetBitmap( "messages",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_btnLogging = self.m_mnuToolbar.AddTool( ID_BTN_LOGGING, u"Logging", wx.ArtProvider.GetBitmap( "logging",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_btnScripts = self.m_mnuToolbar.AddTool( ID_BTN_SCRIPTS, u"Scripts", wx.ArtProvider.GetBitmap( "script_list",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_btnPython = self.m_mnuToolbar.AddTool( ID_BTN_PYTHON, u"Python", wx.ArtProvider.GetBitmap( "python",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_btnControls = self.m_mnuToolbar.AddTool( ID_BTN_CONTROLS, u"Controls", wx.ArtProvider.GetBitmap( "control_panel",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_btnCharts = self.m_mnuToolbar.AddTool( ID_BTN_CHARTS, u"Charts", wx.ArtProvider.GetBitmap( "charts",  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_mnuToolbar.AddSeparator()
        self.m_btnExit = self.m_mnuToolbar.AddTool( wx.ID_ANY, u"Exit", wx.ArtProvider.GetBitmap( wx.ART_QUIT,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
        self.m_mnuToolbar.Realize()
        self.m_mgr.AddPane( self.m_mnuToolbar, wx.aui.AuiPaneInfo().Name( u"dfasdf" ).Top().Caption( u"ZXcZXcZXcZXC" ).CaptionVisible( False ).CloseButton( False ).PaneBorder( False ).Movable( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).BottomDockable( False ).TopDockable( False ).LeftDockable( False ).RightDockable( False ).Floatable( False ).Layer( 3 ) )
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_mnuLayout = wx.Menu()
        self.m_mniLayoutOperator = wx.MenuItem( self.m_mnuLayout, wx.ID_ANY, u"Operator", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mniLayoutOperator.SetBitmap( wx.ArtProvider.GetBitmap( "user_operator",  ) )
        self.m_mnuLayout.Append( self.m_mniLayoutOperator )
        self.m_mniLayoutTechnician = wx.MenuItem( self.m_mnuLayout, wx.ID_ANY, u"Technician", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mniLayoutTechnician.SetBitmap( wx.ArtProvider.GetBitmap( "user_technician",  ) )
        self.m_mnuLayout.Append( self.m_mniLayoutTechnician )
        self.m_mniLayoutEngineer = wx.MenuItem( self.m_mnuLayout, wx.ID_ANY, u"Engineer", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mniLayoutEngineer.SetBitmap( wx.ArtProvider.GetBitmap( "user_engineer",  ) )
        self.m_mnuLayout.Append( self.m_mniLayoutEngineer )
        self.m_mniLayoutExpert = wx.MenuItem( self.m_mnuLayout, wx.ID_ANY, u"Expert", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mniLayoutExpert.SetBitmap( wx.ArtProvider.GetBitmap( "user_expert",  ) )
        self.m_mnuLayout.Append( self.m_mniLayoutExpert )
        self.m_mnuLayout.AppendSeparator()
        self.m_mniLayoutReset = wx.MenuItem( self.m_mnuLayout, wx.ID_ANY, u"Reset to default", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mniLayoutReset.SetBitmap( wx.ArtProvider.GetBitmap( "reset",  ) )
        self.m_mnuLayout.Append( self.m_mniLayoutReset )
        self.m_mniLayoutReset.Enable( False )
        self.m_mgr.Update()
        self.Centre( wx.BOTH )
        self.Bind( wx.EVT_CLOSE, self.OnFormClose )
        self.Bind( wx.EVT_TIMER, self.OnGuiTimer, id=wx.ID_ANY )
        self.Bind( wx.EVT_TOOL, self.OnMnuLayoutClicked, id = self.m_btnLayout.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnTestList, id = self.m_btnTestList.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnMessages, id = self.m_btnMessages.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnLogging, id = self.m_btnLogging.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnScripts, id = self.m_btnScripts.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnPython, id = self.m_btnPython.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnControls, id = self.m_btnControls.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnCharts, id = self.m_btnCharts.GetId() )
        self.Bind( wx.EVT_TOOL, self.OnBtnExit, id = self.m_btnExit.GetId() )
        self.Bind( wx.EVT_MENU, self.OnLayoutOperator, id = self.m_mniLayoutOperator.GetId() )
        self.Bind( wx.EVT_MENU, self.OnLayoutTechnician, id = self.m_mniLayoutTechnician.GetId() )
        self.Bind( wx.EVT_MENU, self.OnLayoutEngineer, id = self.m_mniLayoutEngineer.GetId() )
        self.Bind( wx.EVT_MENU, self.OnLayoutExpert, id = self.m_mniLayoutExpert.GetId() )
        self.Bind( wx.EVT_MENU, self.OnResetLayout, id = self.m_mniLayoutReset.GetId() )
    def __del__( self ):
        self.m_mgr.UnInit()
    def OnFormClose( self, event ):
        event.Skip()
    def OnGuiTimer( self, event ):
        event.Skip()
    def OnMnuLayoutClicked( self, event ):
        event.Skip()
    def OnBtnTestList( self, event ):
        event.Skip()
    def OnBtnMessages( self, event ):
        event.Skip()
    def OnBtnLogging( self, event ):
        event.Skip()
    def OnBtnScripts( self, event ):
        event.Skip()
    def OnBtnPython( self, event ):
        event.Skip()
    def OnBtnControls( self, event ):
        event.Skip()
    def OnBtnCharts( self, event ):
        event.Skip()
    def OnBtnExit( self, event ):
        event.Skip()
    def OnLayoutOperator( self, event ):
        event.Skip()
    def OnLayoutTechnician( self, event ):
        event.Skip()
    def OnLayoutEngineer( self, event ):
        event.Skip()
    def OnLayoutExpert( self, event ):
        event.Skip()
    def OnResetLayout( self, event ):
        event.Skip()
class FormSerials_Base ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Scan serial numbers", pos = wx.DefaultPosition, size = wx.Size( 400,287 ), style = wx.STAY_ON_TOP )
        self.SetSizeHints( wx.DefaultSize, wx.Size( 400,290 ) )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Scan serial numbers :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        bSizer10.Add( self.m_staticText8, 0, wx.ALL, 5 )
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
        self.m_lblSerial1 = wx.StaticText( self, wx.ID_ANY, u"Board 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_lblSerial1.Wrap( -1 )
        gSizer1.Add( self.m_lblSerial1, 2, wx.ALL|wx.EXPAND, 5 )
        self.m_txtSerial1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_txtSerial1.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        gSizer1.Add( self.m_txtSerial1, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_lblSerial2 = wx.StaticText( self, wx.ID_ANY, u"Board 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_lblSerial2.Wrap( -1 )
        gSizer1.Add( self.m_lblSerial2, 2, wx.ALL|wx.EXPAND, 5 )
        self.m_txtSerial2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_txtSerial2.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        gSizer1.Add( self.m_txtSerial2, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_lblSerial3 = wx.StaticText( self, wx.ID_ANY, u"Board 3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_lblSerial3.Wrap( -1 )
        gSizer1.Add( self.m_lblSerial3, 2, wx.ALL|wx.EXPAND, 5 )
        self.m_txtSerial3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_txtSerial3.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        gSizer1.Add( self.m_txtSerial3, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_lblSerial4 = wx.StaticText( self, wx.ID_ANY, u"Board 4", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_lblSerial4.Wrap( -1 )
        gSizer1.Add( self.m_lblSerial4, 2, wx.ALL|wx.EXPAND, 5 )
        self.m_txtSerial4 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_txtSerial4.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        gSizer1.Add( self.m_txtSerial4, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_lblSerial5 = wx.StaticText( self, wx.ID_ANY, u"Board 5", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_lblSerial5.Wrap( -1 )
        gSizer1.Add( self.m_lblSerial5, 2, wx.ALL|wx.EXPAND, 5 )
        self.m_txtSerial5 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_txtSerial5.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        gSizer1.Add( self.m_txtSerial5, 1, wx.ALL|wx.EXPAND, 5 )
        bSizer10.Add( gSizer1, 1, wx.EXPAND, 5 )
        bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_btnOK = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
        bSizer12.Add( self.m_btnOK, 3, wx.ALL, 5 )
        bSizer12.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        self.m_btnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
        bSizer12.Add( self.m_btnCancel, 2, wx.ALL, 5 )
        bSizer10.Add( bSizer12, 2, wx.EXPAND, 10 )
        self.SetSizer( bSizer10 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.m_txtSerial1.Bind( wx.EVT_TEXT, self.OnText1 )
        self.m_txtSerial1.Bind( wx.EVT_TEXT_ENTER, self.OnEnter1 )
        self.m_txtSerial2.Bind( wx.EVT_TEXT, self.OnText2 )
        self.m_txtSerial2.Bind( wx.EVT_TEXT_ENTER, self.OnEnter2 )
        self.m_txtSerial3.Bind( wx.EVT_TEXT, self.OnText3 )
        self.m_txtSerial3.Bind( wx.EVT_TEXT_ENTER, self.OnEnter3 )
        self.m_txtSerial4.Bind( wx.EVT_TEXT, self.OnText4 )
        self.m_txtSerial4.Bind( wx.EVT_TEXT_ENTER, self.OnEnter4 )
        self.m_txtSerial5.Bind( wx.EVT_TEXT, self.OnText5 )
        self.m_txtSerial5.Bind( wx.EVT_TEXT_ENTER, self.OnEnter5 )
        self.m_btnOK.Bind( wx.EVT_BUTTON, self.OnBtnOK )
        self.m_btnCancel.Bind( wx.EVT_BUTTON, self.OnBtnCancel )
    def __del__( self ):
        pass
    def OnText1( self, event ):
        event.Skip()
    def OnEnter1( self, event ):
        event.Skip()
    def OnText2( self, event ):
        event.Skip()
    def OnEnter2( self, event ):
        event.Skip()
    def OnText3( self, event ):
        event.Skip()
    def OnEnter3( self, event ):
        event.Skip()
    def OnText4( self, event ):
        event.Skip()
    def OnEnter4( self, event ):
        event.Skip()
    def OnText5( self, event ):
        event.Skip()
    def OnEnter5( self, event ):
        event.Skip()
    def OnBtnOK( self, event ):
        event.Skip()
    def OnBtnCancel( self, event ):
        event.Skip()
class FormAskImage_Base ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"HappyScript", pos = wx.DefaultPosition, size = wx.Size( 318,338 ), style = wx.CAPTION|wx.STAY_ON_TOP )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer12.Add( self.m_bitmap, 9, wx.ALL|wx.EXPAND, 5 )
        m_sizeButtons = wx.BoxSizer( wx.VERTICAL )
        m_sizeButtons.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        self.m_txtMessage = wx.StaticText( self, wx.ID_ANY, u"Message provided by script\nCould be several lines long.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_txtMessage.Wrap( -1 )
        m_sizeButtons.Add( self.m_txtMessage, 0, wx.ALL|wx.EXPAND, 5 )
        self.m_txtValue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        m_sizeButtons.Add( self.m_txtValue, 0, wx.ALL|wx.EXPAND, 5 )
        self.m_btnOK = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnOK.SetDefault()
        self.m_btnOK.SetMinSize( wx.Size( -1,40 ) )
        m_sizeButtons.Add( self.m_btnOK, 0, wx.ALL|wx.EXPAND, 5 )
        self.m_btnNo = wx.Button( self, wx.ID_ANY, u"No", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnNo.SetMinSize( wx.Size( -1,40 ) )
        m_sizeButtons.Add( self.m_btnNo, 0, wx.ALL|wx.EXPAND, 5 )
        m_sizeButtons.Add( ( 0, 0), 10, wx.EXPAND, 5 )
        self.m_btnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnCancel.SetMinSize( wx.Size( -1,40 ) )
        m_sizeButtons.Add( self.m_btnCancel, 0, wx.ALL|wx.EXPAND, 5 )
        bSizer12.Add( m_sizeButtons, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer12 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.m_btnOK.Bind( wx.EVT_BUTTON, self.OnButtonOK )
        self.m_btnNo.Bind( wx.EVT_BUTTON, self.OnButtonNo )
        self.m_btnCancel.Bind( wx.EVT_BUTTON, self.OnButtonCancel )
    def __del__( self ):
        pass
    def OnButtonOK( self, event ):
        event.Skip()
    def OnButtonNo( self, event ):
        event.Skip()
    def OnButtonCancel( self, event ):
        event.Skip()
class FormAskChoice_Base ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"HappyScript", pos = wx.DefaultPosition, size = wx.Size( 318,227 ), style = wx.CAPTION|wx.STAY_ON_TOP )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        bSizer12 = wx.BoxSizer( wx.VERTICAL )
        self.m_txtMessage = wx.StaticText( self, wx.ID_ANY, u"Message provided by script\nCould be several lines long.", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_txtMessage.Wrap( -1 )
        self.m_txtMessage.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        bSizer12.Add( self.m_txtMessage, 0, wx.ALL|wx.EXPAND, 10 )
        self.m_pnlChoices = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME|wx.TAB_TRAVERSAL )
        bSizer12.Add( self.m_pnlChoices, 1, wx.EXPAND |wx.ALL, 15 )
        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_btnOK = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnOK.SetDefault()
        self.m_btnOK.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_btnOK.Enable( False )
        self.m_btnOK.SetMinSize( wx.Size( -1,40 ) )
        bSizer21.Add( self.m_btnOK, 5, wx.ALL|wx.EXPAND, 10 )
        bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        self.m_btnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnCancel.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.m_btnCancel.SetMinSize( wx.Size( -1,40 ) )
        bSizer21.Add( self.m_btnCancel, 2, wx.ALL|wx.EXPAND, 10 )
        bSizer12.Add( bSizer21, 0, wx.EXPAND, 5 )
        self.SetSizer( bSizer12 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.m_btnOK.Bind( wx.EVT_BUTTON, self.OnButtonOK )
        self.m_btnCancel.Bind( wx.EVT_BUTTON, self.OnButtonCancel )
    def __del__( self ):
        pass
    def OnButtonOK( self, event ):
        event.Skip()
    def OnButtonCancel( self, event ):
        event.Skip()
class FormOnTestFailure_Base ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Error", pos = wx.DefaultPosition, size = wx.Size( 356,229 ), style = wx.CAPTION|wx.STAY_ON_TOP )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.Colour( 255, 206, 206 ) )
        bSizer14 = wx.BoxSizer( wx.VERTICAL )
        self.m_txtMessage = wx.StaticText( self, wx.ID_ANY, u"Test xxxx is gefaald.\nWat wil je doen ?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_txtMessage.Wrap( -1 )
        self.m_txtMessage.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_txtMessage.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        bSizer14.Add( self.m_txtMessage, 0, wx.ALL|wx.EXPAND, 5 )
        self.m_btnRetry = wx.Button( self, wx.ID_ANY, u"Test herhalen", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnRetry.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer14.Add( self.m_btnRetry, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_btnSkipTest = wx.Button( self, wx.ID_ANY, u"Test overslaan", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnSkipTest.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer14.Add( self.m_btnSkipTest, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_btnStopTests = wx.Button( self, wx.ID_ANY, u"Alle testen stoppen", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnStopTests.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        bSizer14.Add( self.m_btnStopTests, 1, wx.ALL|wx.EXPAND, 5 )
        self.SetSizer( bSizer14 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.m_btnRetry.Bind( wx.EVT_BUTTON, self.OnBtnRetry )
        self.m_btnSkipTest.Bind( wx.EVT_BUTTON, self.OnBtnSkip )
        self.m_btnStopTests.Bind( wx.EVT_BUTTON, self.OnBtnStop )
    def __del__( self ):
        pass
    def OnBtnRetry( self, event ):
        event.Skip()
    def OnBtnSkip( self, event ):
        event.Skip()
    def OnBtnStop( self, event ):
        event.Skip()
class Test_Panel ( wx.Panel ):
    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 579,501 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )
        bSizer22 = wx.BoxSizer( wx.VERTICAL )
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"GPIO" ), wx.VERTICAL )
        bSizer24 = wx.BoxSizer( wx.VERTICAL )
        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText14 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Red LED", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        bSizer25.Add( self.m_staticText14, 20, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.m_button24 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Off", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button24.SetMaxSize( wx.Size( 75,-1 ) )
        bSizer25.Add( self.m_button24, 1, wx.ALL, 5 )
        self.m_button25 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"On", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button25.SetMaxSize( wx.Size( 75,-1 ) )
        bSizer25.Add( self.m_button25, 1, wx.ALL, 5 )
        bSizer24.Add( bSizer25, 0, wx.EXPAND, 5 )
        sbSizer2.Add( bSizer24, 0, wx.EXPAND, 5 )
        sbSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        bSizer22.Add( sbSizer2, 0, wx.EXPAND, 5 )
        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Basic Actions" ), wx.VERTICAL )
        bSizer26 = wx.BoxSizer( wx.VERTICAL )
        self.m_button26 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Enable Ethernet", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer26.Add( self.m_button26, 0, wx.ALL, 5 )
        self.m_button27 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Enable video", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer26.Add( self.m_button27, 0, wx.ALL, 5 )
        bSizer27 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText15 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )
        bSizer27.Add( self.m_staticText15, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.m_button28 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"VGA", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer27.Add( self.m_button28, 1, wx.ALL, 5 )
        self.m_button29 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"NTSC", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer27.Add( self.m_button29, 1, wx.ALL, 5 )
        self.m_button30 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"HDMI", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer27.Add( self.m_button30, 1, wx.ALL, 5 )
        bSizer26.Add( bSizer27, 1, wx.EXPAND, 5 )
        bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText16 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Speed", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )
        bSizer28.Add( self.m_staticText16, 0, wx.ALL, 5 )
        self.m_slider1 = wx.Slider( sbSizer3.GetStaticBox(), wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        bSizer28.Add( self.m_slider1, 2, wx.ALL, 5 )
        self.m_spinCtrl1 = wx.SpinCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
        self.m_spinCtrl1.Enable( False )
        self.m_spinCtrl1.SetMaxSize( wx.Size( 75,-1 ) )
        bSizer28.Add( self.m_spinCtrl1, 0, wx.ALL, 5 )
        bSizer26.Add( bSizer28, 1, wx.EXPAND, 5 )
        sbSizer3.Add( bSizer26, 1, wx.EXPAND, 5 )
        bSizer22.Add( sbSizer3, 0, wx.EXPAND, 5 )
        bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer22 )
        self.Layout()
        self.m_button24.Bind( wx.EVT_BUTTON, self.OnBinaryOff )
        self.m_button25.Bind( wx.EVT_BUTTON, self.OnBinaryOn )
        self.m_button26.Bind( wx.EVT_BUTTON, self.OnSingleButton )
        self.m_button27.Bind( wx.EVT_BUTTON, self.OnSingleButton )
        self.m_button28.Bind( wx.EVT_BUTTON, self.OnMultiButton )
        self.m_button29.Bind( wx.EVT_BUTTON, self.OnMultiButton )
        self.m_button30.Bind( wx.EVT_BUTTON, self.OnMultiButton )
        self.m_slider1.Bind( wx.EVT_SCROLL, self.OnSingleSliderScroll )
    def __del__( self ):
        pass
    def OnBinaryOff( self, event ):
        event.Skip()
    def OnBinaryOn( self, event ):
        event.Skip()
    def OnSingleButton( self, event ):
        event.Skip()
    def OnMultiButton( self, event ):
        event.Skip()
    def OnSingleSliderScroll( self, event ):
        event.Skip()
class FormStop_base ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Happyscript", pos = wx.DefaultPosition, size = wx.Size( 480,198 ), style = wx.CAPTION|wx.STAY_ON_TOP )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        bSizer14 = wx.BoxSizer( wx.VERTICAL )
        self.m_lblMessage = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_lblMessage.Wrap( -1 )
        bSizer14.Add( self.m_lblMessage, 1, wx.ALL, 20 )
        self.m_btnCancel = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer14.Add( self.m_btnCancel, 0, wx.ALL|wx.EXPAND, 20 )
        self.SetSizer( bSizer14 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.m_btnCancel.Bind( wx.EVT_BUTTON, self.OnBtnStop )
    def __del__( self ):
        pass
    def OnBtnStop( self, event ):
        event.Skip()
