#!/usr/bin/env python3
"""
We create a unit, that will be the test_ unit by ln -s simoultaneously. Runs with 'pytest'
"""
from fire import Fire

from cmd_ai import config
from cmd_ai.version import __version__

HELP = """
________________SYSTEM COMMANDS_____
.h      help
.q      quit
.e      execute the shown code
.r      reset messages, scripts
.l      show tokens
.m      show models
.l; .l number ... change limit tokens
.g      add google search functions (default OFF)
.u      add other functions ... CHMI weather (test)
.v      read the answer aloud
.c      catch up messages after crash...
________________ ROLES _______________
.a   assistant (default in INTERACTIVE and CMDLINE)
.p   python coder
.s   shell expert (default in PIPE)
.d   dalle 3 ... most exact prompt variant
.t   translator
.i   use vision - low detail
"""





#######################################################################
#     T O O L S ..... functions
#######################################################################
# localted  function_chmi.py  get_chmi()
tool_getCzechWeather = {
                    "type": "function",
                    "function": {
                        "name": "getCzechWeather",
                        "description": "The function provides weather forecast for today(dnes), night(noc) and tomorrow(zitra) in Czech Republic only. The function can provide also actual weather alert(vystraha) for Czech Republic. Text in Czech, parameters in Czech.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "time": {"type": "string", "description": "four options only: dnes | noc | zitra | vystraha"}
                            },
                            "required": ["time"]
                        }
                    }
                }


tool_searchGoogle = {
                    "type": "function",
                    "function": {
                        "name": "searchGoogle",
                        "description": "search Google.com for a phrase and obtain list of urls",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "searchstring": {"type": "string", "description": "optimal search phrase"}
                            },
                            "required": ["searchstring"]
                        }
                    }
                }


tool_getWebContent = {
                    "type": "function",
                    "function": {
                        "name": "getWebContent",
                        "description": "retrieve a text representation of a web page",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "description": "url of a web page to retrieve"}
                            },
                            "required": ["url"]
                        }
                    }
                }


#######################################################################
#     R O L E S
#######################################################################


role_assistant = """You are the assistant that responds questions correctly and fulfills given tasks. You use a short and brief language, you do not repeat yourself nor the users' questions. You make the answers short but precise."""

# The code must be always safe and secure, no harm for the filesystem nor for the network.
role_pythonista = """You are PYTHON program writer. The prompts instruct you to create a python code. The code must be able to run from the commandline, for this use Fire and default values. For graphs, use matplotlib. You use a short and brief language. Never repeat user questions. Make the answers short but precise. Do not give examples how to run the code from shell. Never use example paths e.g. '/path/to/', if not specified, use the current directory. Provide maximum ONE code block per response. Do not show how to install packages, unless explicitelly asked."""



role_translator = """ You translate scientific text prompts from English to Czech. Use clean and concise language. Reformulate the translated text clean and fluent.
It contains specific nuclear physics terminology so
 - "beam" means "svazek" in Czech
 - "target" means "terč" in Czech
 - "beam time" means "urychlovačový čas" in Czech
 - "beam dump" means "zařízení pro zastavení svazku" in Czech
 - "is promissing" mean "je slibná" or "je slibný" in Czech
 In a case I give you a text in SRT subtitles format : `line_number \n time-start --> time-end \n some_sentence(s) \n\n`. The time is in the format of srt: hh:mm:ss,fff - in that case you keep the format exactly he same and translate the sentences to czech.
"""

#  and secure, no harm for the filesystem nor for the network
role_sheller = """ You are an Ubuntu 22 commandline and bash expert. The code must be always safe. You use a short and brief language. Do not repeat the user questions.  Do not repeat yourself. You make the answers short but precise. Only shell code, no examples how to run. Never use example paths e.g. '/path/to/', if not specified, use the current directory. One code block per response maximum.
"""

#  and secure, no harm for the filesystem nor for the network
role_piper = """ You are an Ubuntu 22 commandline and bash expert. But not only. You use a short and brief language. Do not repeat the user questions.  Do not repeat yourself. You make the answers short but precise. No examples how to run. Never use example paths e.g. '/path/to/', '/path/to/search', replace it with the current directory.
"""

role_dalle = """I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:"""

role_vision = """What is in the picture?"""

#######################################################################
#     O R G
#######################################################################


org_header = r"""
# ######################## CODE DEFINITIONS ############################
#+OPTIONS: toc:nil        (no default TOC at all)
# # -------------- dont interpret ^_ as in math...
#+OPTIONS: ^:nil
#+OPTIONS: _:nil
# # --------------- do not number sections
#  +OPTIONS: num:nil

# +LATEX_HEADER: \addtolength{\textwidth}{4cm}
# +LATEX_HEADER: \addtolength{\textheight}{3cm}
# +LATEX_HEADER: \addtolength{\hoffset}{-2cm}
# +LATEX_HEADER: \addtolength{\voffset}{-3cm}


# -----------------------------------------  colored SOURCE blocks
# -----------pip install Pygments; mod .emacs
#+LaTeX_HEADER: \usepackage{minted}
#+LaTeX_HEADER: \usepackage{bookmark}
# --------- margins
#+LATEX_HEADER: \makeatletter \@ifpackageloaded{geometry}{\geometry{margin=2cm}}{\usepackage[margin=2cm]{geometry}} \makeatother
#+LaTeX_HEADER: \usemintedstyle{xcode}
#       xcode,monokai, paraiso-dark,, zenburn ... ... NOT shell /cd |
#       fruity .... NOT  + blackbg
#       colorful ... ok
#       vs ... too simple
#       inkpot ... yellowish-brown
#       vim ... pipe too light
#       gruvbox-dark,sas, stata, abap,algol, lovalace, igor, native, rainbow_dash, tango, manni, borland, autumn:), murphy, material, trac    ... italic
#       rrt ... too light green
#       perldoc, pastie, xcode, arduino ... ok (pastie,arduino (gray comments)
#  +LATEX_HEADER: % !TeX TXS-program:compile = txs:///pdflatex/[--shell-escape]


#
# ========================== this is for quote ... easy ========================
#+LaTeX_HEADER: \usepackage{etoolbox}\AtBeginEnvironment{quote}{\itshape\bf}


# =========================== new verbatim environment -------- gray example
#   tricky ... extra package needed... redefinition needed (example => verbatim)
#          ... it breaks "gray!10!white" color definitions......
#+LaTeX_HEADER: \usepackage{verbatim}
#+LaTeX_HEADER: \usepackage{framed,color,verbatim}
#+LaTeX_HEADER: \definecolor{shadecolor}{rgb}{.95, 1., .9}
#+LaTeX_HEADER: \definecolor{codecolor}{rgb}{.95, .95, .99}
#+LATEX_HEADER: \let\oldverbatim=\verbatim
#+LATEX_HEADER: \let\oldendverbatim=\endverbatim
#+LATEX_HEADER: \renewenvironment{verbatim}[1][test]
#+LATEX_HEADER: {
#+LATEX_HEADER:   \snugshade\oldverbatim
#+LATEX_HEADER: }
#+LATEX_HEADER: {
#+LATEX_HEADER:   \oldendverbatim\endsnugshade
#+LATEX_HEADER: }
"""


if __name__ == "__main__":
    print("i... in the __main__ of unitname of cmd_ai")
    Fire()
