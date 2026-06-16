\ProvidesClass{SVNITPhDReport}
%						      Author	: Milind Padalkar (milind.padalkar@gmail.com)
%						   Thanks to 	: Ankur Dave's Tutorial
%	   Modified for M.Tech Report by 	: Shreyas Patel (shreyaspatel29@gmail.com) (P14CO018)
%					Last modified on 	: 22-11-2015
%						
%-----------------------------------------------
% Page border functionality added on 26-05-2012
% Use command \addpageborder before the page
% where you want the border to appear. Similarly
% use \clearpageborder before the page where you
% want normal pages without border.
% I suggest using \addpageborder before \maketitle,
% while using \clearpageborder before you begin
% your first chapter/section.
%-----------------------------------------------

\LoadClass[12pt]{report}

%User Created Fields
\makeatletter
\RequirePackage{ifthen}
	%\newcommand{name}[num of arg]{definition}
	\newcommand{\borderPath}[1]{\def \@borderPath {#1}}
	\newcommand{\semester}[1]{\def \@semester {#1}}
	\newcommand{\seminarType}[1]{\def \@seminarType {#1}}
	\newcommand{\seminarNo}[1]{\def \@seminarNo {#1}}
	\newcommand{\course}[1]{\def \@course {#1}}
	\newcommand{\instlogo}[1]{\def \@instlogo {#1}}
	\newcommand{\dept}[1]{\def \@dept {#1}}
	\newcommand{\supervisorI}[1]{\def \@supervisorI {#1}}
	\newcommand{\supervisorII}[1]{\def \@supervisorII {#1}}
	\newcommand{\stitleI}[1]{\def \@stitleI {#1}}	
	\newcommand{\stitleII}[1]{\def \@stitleII {#1}}	
	\newcommand{\hodtitle}[1]{\def \@hodtitle {#1}}	
	\newcommand{\hodname}[1]{\def \@hodname {#1}}	
	\newcommand{\sinstI}[1]{\def \@sinstI {#1}}		
	\newcommand{\sinstII}[1]{\def \@sinstII {#1}}		
	\newcommand{\scityI}[1]{\def \@scityI {#1}}		
	\newcommand{\scityII}[1]{\def \@scityII {#1}}		
	\newcommand{\stitleO}[1]{\def \@stitleO {#1}}		
	\newcommand{\supervisorO}[1]{\def \@supervisorO {#1}}
	\newcommand{\regno}[1]{\def \@regno {#1}}
	\newcommand{\addressInstN}[1]{\def \@addressInstN {#1}}
	\newcommand{\addressInstD}[1]{\def \@addressInstD {#1}}
	\newcommand{\addressInstP}[1]{\def \@addressInstP {#1}}
	\newcommand{\acMonth}[1]{\def \@acMonth {#1}}
	\newcommand{\acYear}[1]{\def \@acYear {#1}}
	\newcommand{\calYear}[1]{\def \@calYear {#1}}
	\newcommand{\atitle}[1]{
		\def \@atitle {#1}
		%To place "his" when "mr or Mr or mr. or Mr." else "her"
		\ifthenelse{\equal{#1}{Mr.}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{Mr}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{mr.}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{mr}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{Ms.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{Ms}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{ms.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{ms}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{Mrs.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{Mrs}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{mrs.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{mrs}}{\def \person {her}}{\relax}
	}
	\borderPath{}
	\semester{}
	\seminarType{}
	\seminarNo{}
	\course{}
	\instlogo{}
	\dept{}
	\supervisorI{}
	\hodtitle{}
	\hodname{}
	\supervisorO{}
	\stitleI{}
	\stitleII{}
	\sinstI{}
	\sinstII{}
	\scityI{}
	\scityII{}
	\stitleO{}
	\regno{}
	\addressInstN{}
	\addressInstD{}
	\addressInstP{}
	\acMonth{}
	\acYear{}
	\calYear{}
	\atitle{}
\makeatother

%-----------------------------------
%		Loading Packages
%-----------------------------------
\usepackage{amsmath}
%\usepackage{array}	
%margins

\RequirePackage[a4paper]{geometry}
	%\geometry{vmargin={2.54cm,2.54cm},hmargin={3.17cm,3.17cm},includefoot}
	\geometry{vmargin={1in,1in},hmargin={1in,1in},includefoot}

%spacing
\RequirePackage{setspace}
	\setstretch{1.5}

%figures
\RequirePackage{graphicx}

%proper underlining
\RequirePackage[normalem]{ulem}

%For landscape page
\RequirePackage{lscape}
% Usage : \begin{landscape}\end{landscape}

%For Hyperlinks within the document
\RequirePackage[]{hyperref}
	\hypersetup{
	    colorlinks=false,
	    pdfborder={0 0 0},
	}

%%Colors
\RequirePackage{xcolor}
	\definecolor{white}{rgb}{1.0,1.0,1.0}
	\definecolor{black}{rgb}{0.0,0.0,0.0}
	\definecolor{bordercol}{rgb}{0.0,0.12,0.48}

% Package for special latin fonts
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

%For page borders using PSTRICKS
\RequirePackage{pst-node}% http://ctan.org/pkg/pstricks
\RequirePackage{eso-pic}% http://ctan.org/pkg/eso-pic

%Custom border page command
\makeatletter
\newcommand{\addpageborder}{%
	\AddToShipoutPictureBG{%
		\begin{pspicture}
			\includegraphics{./Figures/border.eps}			
		\end{pspicture}		
	}
}
%	\pagenumbering{roman}
%	\setcounter{page}{1}
\makeatother

% Clear border for a page
\newcommand{\clearpageborder}{
	\ClearShipoutPicture
%	\pagenumbering{arabic}
%	\setcounter{page}{1}
}

% For numbering subsubsections
\setcounter{secnumdepth}{3}

%fonts
\newcommand*{\monocor}[1]{\usefont{T1}{pzc}{m}{it}#1\normalfont} %similar to Monotype Corsiva (ZapfChancery)
\newcommand*{\timesnr}[1]{\usefont{T1}{ptm}{m}{n}#1\normalfont} %Times New Roman
\newcommand*{\helveticaf}[1]{\usefont{T1}{phv}{b}{n}#1\normalfont} %Helvetica Extra bold with caps
\newcommand*{\courierf}[1]{\usefont{T1}{pcr}{m}{n}#1\normalfont} %Courier
\newcommand*{\avantf}[1]{\usefont{T1}{pag}{m}{n}#1\normalfont} %Avant
\newcommand*{\centuryf}[1]{\usefont{T1}{pnc}{m}{n}#1\normalfont} %Century
\newcommand*{\concretef}[1]{\usefont{T1}{ccr}{m}{n}#1\normalfont} %Concrete

%empty page
\newcommand\blankpage{%
    \null
    \thispagestyle{empty}%
%    \addtocounter{page}{-1}%
    \newpage}

%-----------------------------------
%		Title Page
%-----------------------------------

\makeatletter
\def \maketitle{
%	\newgeometry{vmargin={1.54cm,1.54cm},hmargin={3.17cm,3.17cm}}
	\begin{titlepage}
		\begin{center}
			\vspace*{10pt}							
			

			%line 3
			%\courierf{
			\timesnr{
				\textbf{
					\Large
					\textcolor{black}{M.Tech. Dissertation Report}
					\normalsize
				}
			} \\ \vspace*{-5pt}				

			%line4
			\timesnr{
				\parbox{0.65\textwidth}{
					\centering
					\textbf{
						\small
						\textcolor{black}{\expandafter\lowercase\expandafter{titled}}					
						\normalsize
					}
				}
			} \\ \vspace*{20pt}
				
			%line5,6
			\timesnr{
				\parbox{0.65\textwidth}{
					\centering
					\textbf{
						\Large
						\textcolor{black}{\expandafter\uppercase\expandafter{\@title}}
						\normalsize
					}
				}
			} \\ \vspace*{15pt}

			%line7
			\timesnr{
			\parbox{0.66\textwidth}{
			\centering
			\textbf{
			\small
			\textcolor{black}{\footnotesize Submitted in partial fulfilment towards the award of the degree of \normalsize } %\newline for \newline the award of the degree of \normalsize} 			
					%\centering for \newline  \centering the award of the degree of \normalsize}
				}
			} 
			} %\\ \vspace*{15pt}

			%line8	 	
		 	\timesnr{
		 		\parbox{0.65\textwidth}{
		 			\centering
		 	%		\fontsize{18mm}{18mm}\selectfont
		 			\textbf{
		 			\Huge
%		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
		 			\textcolor{black}{{{\Large MASTERS OF TECHNOLOGY  }}}
		 					%\centering for \newline  \centering the award of the degree of \normalsize}
		 			}
		 		}
		 	}\\ \vspace*{5pt}
             	%line9
			\timesnr{
		 		\parbox{0.65\textwidth}{
		 			\centering
		 	%		\fontsize{18mm}{18mm}\selectfont
% 		 			\textbf{
% 		 			\Huge
% %		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
		 			\textcolor{black}{\Large\expandafter\expandafter{\bf in}}
		 					%\centering for \newline  \centering the award of the degree of \normalsize}
		 			}
		 		}
% 		 	}\\ 
% \vspace*{5pt}
        \vspace*{0pt}
		 	
		 	%line10
        \vspace*{10pt}
\timesnr{
  \parbox{0.95\textwidth}{
    \centering
    \textbf{
      \Huge
      \textcolor{black}{
        \Large
        COMPUTER SCIENCE AND ENGINEERING\\[-10pt]
        WITH SPECIALIZATION IN\\[-4pt]
        DATA SCIENCE
      }
    }
  }
}\\

%         \vspace*{10pt}
%                 \timesnr{
% 		 		\parbox{0.45\textwidth}{
% 		 			\centering
% 		 	%		\fontsize{18mm}{18mm}\selectfont
% 		 			\textbf{
% 		 			\Huge
% %		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
% 		 			\textcolor{black}{{{\Large }}}
% 		 					%\centering for \newline  \centering the award of the degree of \normalsize}
% 		 			}
% 		 		}
% 		 	}\\ 
        \vspace*{10pt}

		 	%line11
        \vspace*{0pt}
			\timesnr{
				{
					\textcolor{black}{by}
					\normalsize
				}
			} \\ \vspace*{-15pt}
			%line12,13
			\vspace*{5pt}
			\concretef{
				\textbf{
					\Large
					\textcolor{black}{\bf \@atitle\ \@author \\
                            \vspace*{5pt}
					{\expandafter\uppercase\expandafter{\@regno}} % % 
					}
					\normalsize
				}
			} \\ \vspace*{5pt}
	
			%line14,15a,(15b)
			\timesnr{
				\textbf{
					% \footnotesize
					\textcolor{black}{Supervisors}
					\normalsize
				}
			} \vspace*{-10pt}
			
			%line16
			\concretef{
				\textbf{
					\Large
					\textcolor{black}{ \bf \@stitleI\ \@supervisorI, \@sinstI, \@scityI\\  }
					\normalsize
				}
			}
   \vspace*{5pt}
                 \concretef{
				\textbf{
					\Large
					\textcolor{black}{\bf\@stitleII\ \@supervisorII, \@sinstII, \@scityII\ }
					\normalsize
				}
			} \\ \vspace*{5pt}
   \vspace*{5pt}
   
			%line17
			\ifx \@instlogo \@empty
				\relax
			\else				
				\includegraphics[width=0.25\textwidth]{\@instlogo} 
			\fi					

			%line18
            \vspace*{0pt}
			\timesnr{
				\textbf{
					\large % % 
					\textcolor{black}{\@acYear}
					%\textcolor{black}{\@acMonth,\@calYear}
					\normalsize
				}
			 } \\ \vspace*{5pt}
			
			%line19
            \timesnr{
		 		\parbox{0.65\textwidth}{
		 			\centering
		 	%		\fontsize{18mm}{18mm}\selectfont
		 			\textbf{
		 			\Huge
%		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
		 			%\textcolor{black}{{{\large Department of Computer Science and Engineering }}}
                    \textcolor{black}{\mbox{{\large Department of Computer Science and Engineering}}}
		 					%\centering for \newline  \centering the award of the degree of \normalsize}
		 			}
		 		}
		 	}\\ 

% 		 	%line9
% 			\timesnr{
% 		 		\parbox{0.65\textwidth}{
% 		 			\centering
% 		 	%		\fontsize{18mm}{18mm}\selectfont
% 		 			\textbf{
% 		 			\Huge
% %		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
% 		 			\textcolor{black}{\Large\expandafter\expandafter{in}}
% 		 					%\centering for \newline  \centering the award of the degree of \normalsize}
% 		 			}
% 		 		}
% 		 	}\\ \vspace*{5pt}
		 	
% 		 	%line10
% 			\timesnr{
% 		 		\parbox{0.80\textwidth}{
% 		 			\centering
% 		 	%		\fontsize{18mm}{18mm}\selectfont
% 		 			\textbf{
% 		 			\Huge
% %		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
% 		 			\textcolor{black}{{{\Large COMPUTER SCIENCE AND ENGINEERING \\
%                         WITH SPECIALIZATION IN\\
%                             DATA SCIENCE
%                                  }}}
% 		 					%\centering for \newline  \centering the award of the degree of \normalsize}
% 		 			}
% 		 		}
% 		 	}\\ \vspace*{10pt}

% 		 	%line11
% 			\timesnr{
% 				\textbf{
% 					\small
% 					\textcolor{black}{{by}}
% 					\normalsize
% 				}
% 			} \\ \vspace*{-2pt}
			
% 			%line12,13
			
% 			\concretef{
% 				\textbf{
% 					\Large
% 					\textcolor{black}{\@atitle\ \@author
%                     \\ \@regno
% 					%({\expandafter\uppercase\expandafter{\@regno}}) % % 
% 					}
% 					\normalsize
% 				}
% 			} \\ \vspace*{10pt}
	
% 			%line14,15a,(15b)
% 			\timesnr{
% 				\textbf{
% 					\footnotesize
% 					\textcolor{black}{Supervisors}
% 					\normalsize
% 				}
% 			} \vspace*{-10pt}
			
% 			%line16
% 			\concretef{
% 				\textbf{
% 					\Large
% 					\textcolor{black}{\@stitleI\ \@supervisorI, \@sinstI, \@scityI\\ }
% 					\normalsize
% 				}
% 			} \\ \vspace*{1pt}
%             			%line16
% 			\concretef{
% 				\textbf{
% 					\Large
% 					\textcolor{black}{Manish, Siemens DISW ,Pune\\ }
% 					\normalsize
% 				}
% 			} \\ \vspace*{1pt}

% 			%line17
% 			\ifx \@instlogo \@empty
% 				\relax
% 			\else				
% 				\includegraphics[width=0.25\textwidth]{\@instlogo} 
% 			\fi					

% 			%line18
% 			\timesnr{
% 				\textbf{
% 					\large % % 
% 					\textcolor{black}{\@acYear}
% 					%\textcolor{black}{\@acMonth,\@calYear}
% 					\normalsize
% 				}
% 			 } \\ \vspace*{4pt}
			
% 			%line19
% 			\centuryf{
% 				\textbf{
% 					\Large
% 					\textcolor{black}{Department of Computer Science and Engineering}
% 					\normalsize
% 				}
% 			} \\ \vspace*{4pt}
			
% 			%line20
			\concretef{
				\parbox{0.65\textwidth}{ \centering
					\textbf{
						\Large
						\textcolor{black}{\expandafter\expandafter{SVNIT, Surat}}
						\normalsize
					}
				}
			} \\ \vspace*{4pt}
			
			
		\end{center}
	\end{titlepage}
	%\restoregeometry
	\newpage
}
\makeatother

%-----------------------------------
%		Table of Contents Page
%-----------------------------------

\makeatletter
%Set the title of the ToC page to "Table of Contents" from "Contents"
\def\tableofcontents{\section*{\centering \Large Table of Contents}\@starttoc{toc}}
% How many levels of section head would you like to appear in the
%  Table of Contents?
%  0= chapter titles, 1= section titles, 2= subsection titles, 
%  3= subsubsection titles.
\setcounter{tocdepth}{3}
\newcommand{\bordertoc}{
			\tableofcontents
			\newpage
}
\def\l@chapter#1#2{{ 
	 \vspace*{10pt}
    \@dottedtocline{0}{0em}{1.2em}{\textbf{#1}}{\textbf{#2}}}} 
\def\l@spchapter#1#2{{
	\vspace*{10pt}
    \@dottedtocline{0}{0em}{1.2em}{\textbf{#1}}{\textbf{#2}}}}
\def\l@section{\@dottedtocline{1}{1.5em}{2.3em}}
\def\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
\def\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
\def\l@paragraph{\@dottedtocline{4}{10em}{5em}}
\def\l@subparagraph{\@dottedtocline{5}{13em}{5.8em}}
\makeatother

%-----------------------------------
%		List of figures Page
%-----------------------------------

\makeatletter
\def\listoffigures{\section*{\centering \Large List of Figures}\@starttoc{lof}}
\newcommand{\borderlof}{
			\listoffigures
			\newpage
}
\makeatother

%-----------------------------------
%		List of Tables Page
%-----------------------------------

\makeatletter
\def\listoftables{\section*{\centering \Large List of Tables}\@starttoc{lot}}
\newcommand{\borderlot}{		
			\listoftables
			\newpage
}
\makeatother

%-----------------------------------
%		Chapter Head settings
%-----------------------------------
\makeatletter
\renewcommand{\@makechapterhead}[1]{%
	\vspace*{10\p@}%
  	{\parindent \z@ \raggedleft \normalfont
    	\ifnum \c@secnumdepth >\m@ne
        	\huge\bfseries \@chapapp\space \textbf{\thechapter}
        	\par\nobreak
        	\vskip 20\p@
    	\fi
    	\interlinepenalty\@M
    	\Huge \bfseries \textbf{#1}\par\nobreak
    	\vskip 40\p@
  	}
}
\makeatother
%-----------------------------------
%		Table1(Admin) Page
%-----------------------------------

\makeatletter
\newcommand{\putTableAdmin}[1]{
		\newgeometry{vmargin={1.54cm,1.54cm},hmargin={3.17cm,3.17cm}}
		\begin{titlepage}
%			\pagenumbering{roman}
%	    	\setcounter{page}{2}		
			\begin{landscape}
%			\setlength{\textwidth}{9.7in}
%			\setlength{\textheight}{6.3in}
				\begin{center}
					\begin{LARGE}
						\expandafter\uline\expandafter{TABLE I : Details of the Seminars -- Administrative}
					\end{LARGE}
					\\ \vspace*{15pt}
					%\begin{large}
					{#1}
					%\end{large}
				\end{center}
			\end{landscape}
		\end{titlepage}
		\restoregeometry
			\newpage
}
\makeatother

%-----------------------------------
%Table2(Technical) Page
%-----------------------------------

\makeatletter
\newcommand{\putTableTech}[1]{
		%\newgeometry{vmargin={1.54cm,1.54cm},hmargin={3.17cm,3.17cm}}
		%\begin{titlepage}
		  	\setcounter{page}{3}
%			\hspace*{10pt}\parbox{0.90\textwidth}{
				\begin{center}
					\begin{LARGE}
						\expandafter\uline\expandafter{TABLE II : Details of the Seminars -- Technical}
					\end{LARGE}
					\\ \vspace*{35pt}
					%\begin{large}
					{#1}
					%\end{large}
				\end{center}
%			}
		%\end{titlepage}
%		\restoregeometry
			\newpage
}
\makeatother

%-----------------------------------
%		Decleration Page
%-----------------------------------

\makeatletter
\newcommand{\putdecleration}{
\hspace*{10pt}\parbox{0.90\textwidth}{
   %          \begin{minipage}[r]{0.8\textwidth}		
			% 	\centuryf{			
			% 		\textbf{				
			% 			\makebox[150pt] \\ \vspace*{-5pt}
   %                          \Large
			% 				\begin{center}
   %                          \uppercase{Sardar Vallabhbhai National Institute of Technology,\\
			% 					Surat}
			% 				\end{center}
			% 		}				
			% 	}			
			% \end{minipage}

            \begin{minipage}[r]{0.8\textwidth}		
				\centuryf{			
									
						\makebox[150pt] \\ \vspace*{-5pt}
                            \Large
							\begin{center}
                            \underline{
						\textbf{
							\uppercase{declaration}
						}
					}
							\end{center}						
				}			
			\end{minipage}
		\vspace*{20pt}
        \\
		\centuryf{	
				%\small
				\setstretch{2.5}
				\hspace*{15pt}I hereby declare that the work being presented in this dissertation report entitled ``\expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@title}}'' by me i.e., \uline{\@atitle\ }\expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@author}} bearing Admn No: \expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@regno}} and submitted to the Department of Computer Science and Engineering at Sardar Vallabhbhai National Institute of Technology, Surat; is an authentic record of my own work carried out during the period of July 2025 to June 2026 under the supervision of \expandafter\expandafter{\expandafter\uline\expandafter{\@supervisorI}}. The matter presented in this report has not been submitted by me in any other University/Institute for any cause.
                \\
                \hspace*{15pt}Neither the source code there in, nor the content of the project report have been copied or downloaded from any other source. I understand that my result grades would be revoked if later it is found to be so.	
                \\
		}		
		\\
		\makebox[150pt]{\hrulefill}		
		\\
		(Name \& Sign of the Candidate)
		\setstretch{1.5}		

		}
	\newpage
}
\makeatother
%-----------------------------------
%		Certificate Page
%-----------------------------------
\makeatletter
\newcommand{\putcertificate}{
\hspace*{10pt}\parbox{0.90\textwidth}
		
	\begin{center}
    \textbf{\LARGE CERTIFICATE} % Slightly larger text for the title
\end{center}

\vspace{0.75cm}

\noindent This is to certify that the dissertation report entitled \uline{"Cross-Domain Semantic Segmentation in Aerial Traffic Surveillance"}, is prepared and presented by \uline{Mr. Ayush Panchal}, bearing Admn. No: \uline{P24DS013}, of M. Tech. II, Semester IV in Computer Science and Engineering with specialization in Data Science, at the Department of Computer Science and Engineering, Sardar Vallabhbhai National Institute of Technology, Surat, is satisfactory.\\ \vspace*{12pt} 

   \noindent
\begin{minipage}[t]{0.48\textwidth}
  \vtop{
    \makebox[150pt]{\hrulefill} \\[2pt]
    Dr. Dipti P. Rana \\
    Associate Professor, \\
    Department of Computer \\
    Science and Engineering, \\
    Sardar Vallabhbhai National \\
    Institute of Technology, \\
    Surat - 395007, Gujarat, India \\[8pt]
   
  }

\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}
  \vtop{
    \makebox[150pt]{\hrulefill} \\[2pt]
    Sameer Chivukula \\
    Director Data Science, \\
    Elsevier, \\
    Chennai, Tamil Nadu\\
    India \\[8pt]
  }
\end{minipage}

\vspace{0.25cm}

\noindent
\begin{minipage}[t]{0.48\textwidth}
  \vtop{
    \makebox[150pt]{\hrulefill} \\[2pt]
    \textbf{Jury's Signature} \\[4pt]
  }
\end{minipage}

\vspace{0.35cm}

\noindent
\begin{minipage}[t]{0.48\textwidth}
  \vtop{
    \makebox[150pt]{\hrulefill} \\[2pt]
    PG Incharge, \\
    M.Tech. in Computer \\ Science and Engineering  \\
    with Specialization in \\
     Data Science, \\
    SVNIT, Surat \\[10pt]
  }
\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}
  \vtop{
    \makebox[150pt]{\hrulefill} \\[2pt]
    Head, \\
    Department of \\
    Computer Science and \\ Engineering, \\
    SVNIT, Surat \\[10pt]
  }
\end{minipage}

		
        \newpage		
}
\makeatother

%------------



%-----------------------------------
%		Acknowledgement Page
%-----------------------------------


\makeatletter
\newcommand{\putsvnitack}[1]{
	\hspace*{10pt}\parbox{0.90\textwidth}{
		\begin{center}
    \LARGE \textbf{Acknowledgements} % Make the title larger
\end{center}

\vspace{0.5cm} % Space after title

I extend my profound gratitude to my research supervisor and guide \textbf{\@supervisorI}, whose exceptional guidance and scholarly mentorship have been pivotal in the successful completion of this research work. The invaluable discussions, constructive feedback, and continuous support provided have significantly shaped the research methodology and outcomes. Special appreciation is extended to my research progress committee members for their critical evaluations, insightful comments, and scholarly suggestions that substantially enhanced the technical rigor and academic quality of this work.

I want to thank \textbf{Dr. Sankita J. Patel}, Head of Computer Science and Engineering, Sardar Vallabhbhai National Institute of Technology, Surat, and PG Incharge of Computer Science and Engineering with Specialization in Data Science, Sardar Vallabhbhai National Institute of Technology, Surat; for providing
infrastructural facilities and support for my work. I am deeply thankful to the faculty members
of the Department of Computer Science and Engineering at Sardar Vallabhbhai National
Institute of Technology, Surat, whose collective expertise and academic insights have been
instrumental in enriching this research journey.

I acknowledge the administrative and technical support provided by the departmental staff, whose assistance facilitated the smooth progression of this research work.
		%\newline
		
		%\hspace*{10pt}   \textsf I would like to express my gratitude to my parents and family for their kind cooperation and encouragement which help me complete my seminar work.
			
		\begin{flushright}
			\vspace{60pt}  
				\textbf{
					\@author	\\
					\@regno
				}
		\end{flushright}
	}	
	\newpage
}
\makeatother

%-----------------------------------
%		Abstract Page
%-----------------------------------

\makeatletter
\newcommand{\putsvnitabstract}[1]{
			%\hspace*{10pt}\parbox{0.90\textwidth}{
				\begin{center}
					\Large
						\timesnr{
							\textbf{
								{
									Abstract
								}
							}
						}				
				\end{center}
				\vspace*{40pt}
				{#1}
		%	}	
			\newpage
		}
\makeatother
%-----------------------------------
%		Place bibliography in table of contents
%-----------------------------------
\def\thebibliography#1{\cleardoublepage\chapter*{\raggedleft ddBibliography}\addcontentsline{toc}{chapter}{Bibliography}\list
  {[\arabic{enumi}]}{\settowidth\labelwidth{[#1]}\leftmargin\labelwidth
    \advance\leftmargin\labelsep
    \usecounter{enumi}}
    \def\newblock{\hskip .11em plus .33em minus .07em}
    \sloppy\clubpenalty4000\widowpenalty4000
    \sfcode`\.=1000\relax}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Approval Sheet
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\makeatletter
\newcommand{\putapprovalSheetDepartment}{

\hspace*{-10pt}\parbox{0.95\textwidth}{

		\begin{center}
			\centuryf{
				\textbf{
					\Large
					\textcolor{black}{SARDAR VALLABHBHAI NATIONAL INSTITUTE OF TECHNOLOGY, SURAT }
				}
			} \\ \vspace*{3pt}
			\large
			\textbf{Department of Computer Science and Engineering}\\
			\normalsize (2025-26)
			\\ \vspace*{5pt}
			\large
				\underline{\textbf{Approval Sheet}}
			\normalsize
			
		\end{center}
		
		\vspace*{10pt}
		
		\centuryf{	
				%\small
				%\setstretch{2.5} \makebox[400pt]{\hrulefill}
				This is to state that the Dissertation Report entitled \expandafter\uline\expandafter{\@title} \hspace{0.1cm} submitted by \hspace{0.1cm} \uline{\@atitle\ }\expandafter\uline\expandafter{\@author}     (Admission No: \expandafter\uline\expandafter{\@regno}) is approved	for the award of the degree of Masters of Technology in CSE with Specialization in Data Science.			
		}
		\vspace*{25pt}
		\begin{center}
			\centuryf{
				\textbf{
					\large
					\underline{\textbf{Board of Examiners}}
				}
			} \\ \vspace*{8pt}
			\normalsize \textbf{Examiners}
			
			\\ \vspace*{15pt}
			
			\makebox[250pt]{\hrulefill} \\
			\makebox[250pt]{\hrulefill}
			
			\\ \vspace*{15pt}
			
			\textbf{Supervisor}
			\\ \vspace*{10pt}
			\makebox[250pt]{\hrulefill} \\
			\\ \vspace*{10pt}
   \makebox[250pt]{\hrulefill} \\
   \\ \vspace*{10pt}
			% \textbf{Chairperson}
			% \\ \vspace*{10pt}
			% \makebox[250pt]{\hrulefill} \\
			
			\\ \vspace*{10pt}
			\textbf{Head, Department of Computer Science and Engineering}
			\\ \vspace*{10pt}
			\makebox[250pt]{\hrulefill} \\
			\\ \vspace*{10pt}
			
		\end{center}
		
		Date:\makebox[90pt]{\hrulefill}\\
		Place:\makebox[90pt]{\hrulefill}
		
		
	}	
	\newpage
}
\makeatother
