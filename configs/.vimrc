syntax on
set nu
set ruler
set showcmd
set autoindent
set nocompatible
filetype on
filetype plugin indent on

set showmatch
set cin
set noerrorbells
set background=dark
":colorscheme morning
:colorscheme desert

"set fileencoding=gbk

set ai
set si
set fo+=mB
let g:explVertical=1

" Encoding settings
if has("multi_byte")
" Set fileencoding priority
if getfsize(expand("%")) > 0
set fileencodings=ucs-bom,utf-8,cp936,big5,euc-jp,euc-kr,latin1
else
set fileencodings=cp936,big5,euc-jp,euc-kr,latin1
endif

" CJK environment detection and corresponding setting
if v:lang =~ "^zh_CN"
" Use cp936 to support GBK, euc-cn == gb2312
set encoding=cp936
set termencoding=cp936
set fileencoding=cp936
elseif v:lang =~ "^zh_TW"
" cp950, big5 or euc-tw
" Are they equal to each other?
set encoding=big5
set termencoding=big5
set fileencoding=big5
elseif v:lang =~ "^ko"
" Copied from someone's dotfile, untested
set encoding=euc-kr
set termencoding=euc-kr
set fileencoding=euc-kr
elseif v:lang =~ "^ja_JP"
" Copied from someone's dotfile, unteste
set encoding=euc-jp
set termencoding=euc-jp
set fileencoding=euc-jp
endif
" Detect UTF-8 locale, and replace CJK setting if needed
if v:lang =~ "utf8$" || v:lang =~ "UTF-8$"
set encoding=utf-8
set termencoding=utf-8
set fileencoding=utf-8
endif
else
echoerr "Sorry, this version of (g)vim was not compiled with multi_byte"
endif

"Key maping
set pastetoggle=<F2>
map ,m :w<CR>:make %<<CR>
map ,r :!./%<<CR>
map ,d :!gdb ./%<<CR>
map ,i ggi/********************************************************************

map <C-A> <Esc>ggVG

autocmd FileType tex set fileencoding=gbk

"NERD_comments.vim leader
"let NERD_mapleader='.c'
let g:BASH_AuthorName   = 'Li Yingjie'
let g:BASH_AuthorRef    = 'hero'
let g:BASH_Email        = 'yingjie.li@intel.com'
let g:BASH_Company      = 'Intel Mobile Communication Ltd.'

let g:Perl_AuthorName      = 'Li Yingjie'
let g:Perl_AuthorRef       = 'hero'
let g:Perl_Email           = 'yingjie.li@intel.com'
let g:Perl_Company         = 'Intel Mobile Communication Ltd.'  
