var oswk = {
    _prefixC: false,
    _prefixU: false,
    _urlDic: "http://dic.search.naver.com/search.naver?where=dic&sm=tab_jum&query=",
    _urlMoz: "http://127.0.0.1:8090/",

    _keyAndCommand: {

	// KEY: [FUNCTION1,FUNCTION2]
	// FUNCTION1 is for C-u C-c prefix. FUNCTION2 is for C-c prefix
	49: ["openNewWindowCurrent", "openNewWindowReposition"], 	// 1
	50: ["openNewWindowReposition", "openNewWindowReposition"], 	// 2
	51: ["openEmacs", "openEmacsReposition"], 	// 3
	52: ["openEmacsReposition","openEmacsReposition"] 	// 4
	
    },

    eventHandler: function(event) {
	
	var e = event || window.event;

	if (e.type == "keydown") {
	    var code = e.keyCode;

	    // Turn on C-u prefix
	    if (e.ctrlKey && code == 85) {	// 85 is u
		this._prefixU = true;
	    }
	    // Turn on C-c prefix
	    else if (e.ctrlKey && code == 67) {	// 67 is c
		this._prefixC = true;
	    }
	    else {
		// C-u C-c
		if (this._prefixU && this._prefixC) {

		    if (this._keyAndCommand[code]) {
			this[this._keyAndCommand[code][1]]();
		    }
		}
		// C-c
		else if (this._prefixC) {
		    if (this._keyAndCommand[code]) {
			this[this._keyAndCommand[code][0]]();			
		    }
		}
		
		// Turn off prefixies
		this._prefixU = false;
		this._prefixC = false;
	    }
	}
	    
    },


    // Open new window.  
    openNewWindow: function(setPosition) {

	if (setPosition) {
	    window.moveTo(0,0);
	}
	var sl = window.screenX;
	var sr = window.screen.width - window.screenX - window.outerWidth;
	var px = window.screenX + window.outerWidth + 8;

	if (sl < sr) {
	    var args = "width=759, height="+window.screen.height+",scrollbars=no,resizable=yes,left=" + px;
	}
	else {
	    var args = "width=759, height="+window.screen.height+",scrollbars=no,resizable=yes,left=0";
	}
	winObj = window.open(this._urlDic,"NaverDic", args);
	winObj.forcus();
    },

    openNewWindowCurrent: function() {
	return this.openNewWindow(false);
    },

    openNewWindowReposition: function() {
	return this.openNewWindow(true);
    },

    openEmacs: function() {
	var url = this._urlMoz+'openEmacs';
	var req = new XMLHttpRequest();
	req.open("GET", url, false);
	req.send(null);
	
    },

    openEmacsReposition: function() {
	window.moveTo(0,0);
	this.openEmacs();
    },


    // Open in new tab. 
    openAndReuseOneTabPerAttribute: function (attrName, url) {
	netscape.security.PrivilegeManager.enablePrivilege('UniversalXPConnect');
	var wm = Components.classes["@mozilla.org/appshell/window-mediator;1"]
            .getService(Components.interfaces.nsIWindowMediator);
	for (var found = false, index = 0, tabbrowser = wm.getEnumerator('navigator:browser').getNext().getBrowser();
	     index < tabbrowser.mTabs.length && !found;
	     index++) {

	    // Get the next tab
	    var currentTab = tabbrowser.mTabs[index];
	    
	    // Does this tab contain our custom attribute?
	    if (currentTab.hasAttribute(attrName)) {

		// Yes--select and focus it.
		tabbrowser.selectedTab = currentTab;

		// Focus *this* browser in case another one is currently focused
		tabbrowser.focus();
		found = true;
	    }
	}

	if (!found) {
	    // Our tab isn't open. Open it now.
	    var browserEnumerator = wm.getEnumerator("navigator:browser");
	    var tabbrowser = browserEnumerator.getNext().getBrowser(); 
  
	    // Create tab
	    var newTab = tabbrowser.addTab(url);
	    newTab.setAttribute(attrName, "xyz");
  
	    // Focus tab
	    tabbrowser.selectedTab = newTab;
    
	    // Focus *this* browser in case another one is currently focused
	    tabbrowser.focus();
	}
    }
};
