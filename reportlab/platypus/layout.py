###############################################################################
#
#	ReportLab Public License Version 1.0
#
#	Except for the change of names the spirit and intention of this
#	license is the same as that of Python
#
#	(C) Copyright ReportLab Inc. 1998-2000.
#
#
# All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted, provided
# that the above copyright notice appear in all copies and that both that
# copyright notice and this permission notice appear in supporting
# documentation, and that the name of ReportLab not be used
# in advertising or publicity pertaining to distribution of the software
# without specific, written prior permission.
#
#
# Disclaimer
#
# ReportLab Inc. DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS,
# IN NO EVENT SHALL ReportLab BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
###############################################################################
#	$Log: layout.py,v $
#	Revision 1.27  2000/05/17 16:29:40  rgbecker
#	Removal of SimpleFrame
#
#	Revision 1.26  2000/05/16 16:15:16  rgbecker
#	Changes related to removal of SimpleFlowDocument
#	
#	Revision 1.25  2000/05/15 13:36:11  rgbecker
#	Splitting changes
#	
#	Revision 1.24  2000/05/12 12:52:00  rgbecker
#	Fixes to BasicFrame split method
#	
#	Revision 1.23  2000/05/11 14:02:14  rgbecker
#	Removed usage of spaceBefore/After in wrap methods
#	
#	Revision 1.22  2000/05/10 13:04:35  rgbecker
#	Added softspace handling
#	
#	Revision 1.21  2000/05/10 09:54:40  rgbecker
#	Flowable.split should return list
#	
#	Revision 1.20  2000/04/28 13:39:12  rgbecker
#	Fix _doNothing argument name
#	
#	Revision 1.19  2000/04/26 11:07:15  andy_robinson
#	Tables changed to use reportlab.lib.colors instead of
#	the six hard-coded color strings there previously.
#	
#	Revision 1.18  2000/04/25 15:42:04  rgbecker
#	Factored out BasicFrame from SimpleFrame
#	
#	Revision 1.17  2000/04/14 16:12:11  rgbecker
#	Debugging xml changes
#	
#	Revision 1.16  2000/04/14 11:54:57  rgbecker
#	Splitting layout.py
#	
#	Revision 1.15  2000/04/14 08:56:20  rgbecker
#	Drawable ==> Flowable
#	
#	Revision 1.14  2000/04/13 17:06:40  rgbecker
#	Fixed SimpleFrame.add
#	
#	Revision 1.13  2000/04/13 14:48:41  rgbecker
#	<para> tag added in layout.py paraparser.py
#	
#	Revision 1.12  2000/04/12 16:26:51  rgbecker
#	XML Tagged Paragraph parser changes
#	
#	Revision 1.11  2000/04/10 14:08:19  rgbecker
#	fixes related to offset
#	
#	Revision 1.10  2000/04/10 12:25:10  rgbecker
#	Typo fixes for justified paras
#	
#	Revision 1.9  2000/04/07 12:31:29  rgbecker
#	Color fixes/changes
#	
#	Revision 1.8  2000/04/06 09:52:02  andy_robinson
#	Removed some old comments; tweaks to experimental Outline methods.
#	
#	Revision 1.7  2000/03/08 13:06:39  andy_robinson
#	Moved inch and cm definitions to reportlab.lib.units and amended all demos
#	
#	Revision 1.6  2000/02/23 10:53:33  rgbecker
#	GMCM's memleak fixed
#	
#	Revision 1.5  2000/02/17 02:09:05  rgbecker
#	Docstring & other fixes
#	
#	Revision 1.4  2000/02/16 09:42:50  rgbecker
#	Conversion to reportlab package
#	
#	Revision 1.3  2000/02/15 17:55:59  rgbecker
#	License text fixes
#	
#	Revision 1.2  2000/02/15 15:47:09  rgbecker
#	Added license, __version__ and Logi comment
#	
__version__=''' $Id: layout.py,v 1.27 2000/05/17 16:29:40 rgbecker Exp $ '''
__doc__="""
Page Layout And TYPography Using Scripts
a page layout API on top of PDFgen
currently working on paragraph wrapping stuff.
"""

# 200-10-13 gmcm
#	packagizing
#	rewrote grid stuff - now in tables.py

import string

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import red

from reportlab.lib.pagesizes import DEFAULT_PAGE_SIZE
PAGE_HEIGHT = DEFAULT_PAGE_SIZE[1]

#############################################################
#	Flowable Objects - a base class and a few examples.
#	One is just a box to get some metrics.	We also have
#	a paragraph, an image and a special 'page break'
#	object which fills the space.
#############################################################
class Flowable:
	"""Abstract base class for things to be drawn.	Key concepts:
	1. It knows its size
	2. It draws in its own coordinate system (this requires the
		base API to provide a translate() function.
	"""
	def __init__(self):
		self.width = 0
		self.height = 0
		self.wrapped = 0

	def drawOn(self, canvas, x, y):
		"Tell it to draw itself on the canvas.	Do not override"
		self.canv = canvas
		self.canv.saveState()
		self.canv.translate(x, y)

		self.draw()   #this is the bit you overload

		self.canv.restoreState()
		del self.canv


	def wrap(self, availWidth, availHeight):
		"""This will be called by the enclosing frame before objects
		are asked their size, drawn or whatever.  It returns the
		size actually used."""
		return (self.width, self.height)

	def split(self, availWidth, availheight):
		"""This will be called by more sophisticated frames when
		wrap fails. Stupid flowables should return []. Clever flowables
		should split themselves and return a list of flowables"""
		return []

	def getSpaceAfter(self):
		if hasattr(self,'spaceAfter'): return self.spaceAfter
		elif hasattr(self,'style') and hasattr(self.style,'spaceAfter'): return self.style.spaceAfter
		else: return 0

	def getSpaceBefore(self):
		if hasattr(self,'spaceBefore'): return self.spaceBefore
		elif hasattr(self,'style') and hasattr(self.style,'spaceBefore'): return self.style.spaceBefore
		else: return 0

class XBox(Flowable):
	"""Example flowable - a box with an x through it and a caption.
	This has a known size, so does not need to respond to wrap()."""
	def __init__(self, width, height, text = 'A Box'):
		Flowable.__init__(self)
		self.width = width
		self.height = height
		self.text = text

	def draw(self):
		self.canv.rect(0, 0, self.width, self.height)
		self.canv.line(0, 0, self.width, self.height)
		self.canv.line(0, self.height, self.width, 0)

		#centre the text
		self.canv.setFont('Times-Roman',12)
		self.canv.drawCentredString(0.5*self.width, 0.5*self.height, self.text)

class Preformatted(Flowable):
	"""This is like the HTML <PRE> tag.  The line breaks are exactly where you put
	them, and it will not be wrapped.  So it is much simpler to implement!"""
	def __init__(self, text, style, bulletText = None, dedent=0):
		self.style = style
		self.bulletText = bulletText

		#tidy up text - carefully, it is probably code.  If people want to
		#indent code within a source script, you can supply an arg to dedent
		#and it will chop off that many character, otherwise it leaves
		#left edge intact.

		templines = string.split(text, '\n')
		self.lines = []
		for line in templines:
			line = string.rstrip(line[dedent:])
			self.lines.append(line)
		#don't want the first or last to be empty
		while string.strip(self.lines[0]) == '':
			self.lines = self.lines[1:]
		while string.strip(self.lines[-1]) == '':
			self.lines = self.lines[:-1]

	def wrap(self, availWidth, availHeight):
		self.width = availWidth
		self.height = self.style.leading*len(self.lines)
		return (self.width, self.height)

	def draw(self):
		#call another method for historical reasons.  Besides, I
		#suspect I will be playing with alternate drawing routines
		#so not doing it here makes it easier to switch.

		cur_x = self.style.leftIndent
		cur_y = self.height - self.style.fontSize
		self.canv.addLiteral('%PreformattedPara')

		tx = self.canv.beginText(cur_x, cur_y)
		#set up the font etc.
		tx.setFont(self.style.fontName,
				   self.style.fontSize,
				   self.style.leading)

		for text in self.lines:
			tx.textLine(text)
		self.canv.drawText(tx)

class Image(Flowable):
	def __init__(self, filename, width=None, height=None):
		"""If size to draw at not specified, get it from the image."""
		import Image  #this will raise an error if they do not have PIL.
		self.filename = filename
		print 'Creating Image for', filename
		img = Image.open(filename)
		(self.imageWidth, self.imageHeight) = img.size
		if width:
			self.drawWidth = width
		else:
			self.drawWidth = self.imageWidth
		if height:
			self.drawHeight = height
		else:
			self.drawHeight = self.imageHeight

	def wrap(self, availWidth, availHeight):
		#the caller may decide it does not fit.
		self.availWidth = availWidth
		return (self.drawWidth, self.drawHeight)

	def draw(self):
		#center it
		startx = 0.5 * (self.availWidth - self.drawWidth)
		self.canv.drawInlineImage(self.filename,
								  startx,
								  0,
								  self.drawWidth,
								  self.drawHeight
								  )
class Spacer(Flowable):
	"""A spacer just takes up space and doesn't draw anything - it can
	ensure a gap between objects."""
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def wrap(self, availWidth, availHeight):
		return (self.width, self.height)

	def draw(self):
		pass

class PageBreak(Flowable):
	"""This works by consuming all remaining space in the frame!"""

	def wrap(self, availWidth, availHeight):
		self.width = availWidth
		self.height = availHeight
		return (availWidth,availHeight)  #step back a point

	def draw(self):
		pass

class Macro(Flowable):
	"""This is not actually drawn (i.e. it has zero height)
	but is executed when it would fit in the frame.  Allows direct
	access to the canvas through the object 'canvas'"""
	def __init__(self, command):
		self.command = command
	def wrap(self, availWidth, availHeight):
		return (0,0)
	def draw(self):
		exec self.command in globals(), {'canvas':self.canv}

class BasicFrame:
	'''Abstraction for the definitional part of a Frame

                width                    x2,y2
    	+---------------------------------+
    	| l  top padding                r | h
    	| e +-------------------------+ i | e
    	| f |                         | g | i
    	| t |                         | h | g
    	|   |                         | t | h
    	| p |                         |   | t
    	| a |                         | p |
    	| d |                         | a |
    	|   |                         | d |
    	|   +-------------------------+   |
    	|    bottom padding				  |
    	+---------------------------------+
    	(x1,y1)
	'''
	def __init__(self, x1, y1, width,height, leftPadding=6, bottomPadding=6,
			rightPadding=6, topPadding=6, id=None, showBoundary=0):

		self.id = id

		#these say where it goes on the page
		self.x1 = x1
		self.y1 = y1
		self.x2 = x1 + width
		self.y2 = y1 + height

		#these create some padding.
		self.leftPadding = leftPadding
		self.bottomPadding = bottomPadding
		self.rightPadding = rightPadding
		self.topPadding = topPadding

		#efficiency
		self.y1p = self.y1 + bottomPadding

		# if we want a boundary to be shown
		self.showBoundary = showBoundary

		self._reset()

	def	_reset(self):
		#work out the available space
		self.width = self.x2 - self.x1 - self.leftPadding - self.rightPadding
		self.height = self.y2 - self.y1 - self.topPadding - self.bottomPadding
		#drawing starts at top left
		self.x = self.x1 + self.leftPadding
		self.y = self.y2 - self.topPadding
		self.atTop = 1

	def _add(self, flowable, canv, trySplit=0):
		""" Draws the flowable at the current position.
		Returns 1 if successful, 0 if it would not fit.
		Raises a LayoutError if the object is too wide,
		or if it is too high for a totally empty frame,
		to avoid infinite loops"""
		y = self.y
		p = self.y1p
		s = self.atTop and 0 or flowable.getSpaceBefore()
		h = y - p - s
		if h>0:
			w, h = flowable.wrap(self.width, h)
		else:
			return 0

		h = h + s
		y = y - h

		if y < p:
			if ((h > self.height and not trySplit) or w > self.width):
				raise "LayoutError", "Flowable (%dx%d points) too large for frame (%dx%d points)." % (w,h, self.width,self.height)
			return 0
		else:
			#now we can draw it, and update the current point.
			flowable.drawOn(canv, self.x, y)
			y = y - flowable.getSpaceAfter()
			self.atTop = 0
			self.y = y
			return 1

	add = _add

	def split(self,flowable):
		'''calls split on the flowable'''
		y = self.y
		p = self.y1p
		s = self.atTop and 0 or flowable.getSpaceBefore()
		return flowable.split(self.width, y-p-s)

	def drawBoundary(self,canv):
		canv.rect(
				self.x1,
				self.y1,
				self.x2 - self.x1,
				self.y2 - self.y1
				)

	def addFromList(self, drawlist, canv):
		"""Consumes objects from the front of the list until the
		frame is full.	If it cannot fit one object, raises
		an exception."""

		if self.showBoundary:
			self.drawBoundary(canv)

		while len(drawlist) > 0:
			head = drawlist[0]
			if self.add(head,canv,trySplit=0):
				del drawlist[0]
			else:
				#leave it in the list for later
				break

class Sequencer:
	"""Something to make it easy to number paragraphs, sections,
	images and anything else. Usage:
		>>> seq = layout.Sequencer()
		>>> seq.next('Bullets')
		1
		>>> seq.next('Bullets')
		2
		>>> seq.next('Bullets')
		3
		>>> seq.reset('Bullets')
		>>> seq.next('Bullets')
		1
		>>> seq.next('Figures')
		1
		>>>
	I plan to add multi-level linkages, so that Head2 could be reet
	"""
	def __init__(self):
		self.dict = {}

	def next(self, category):
		if self.dict.has_key(category):
			self.dict[category] = self.dict[category] + 1
		else:
			self.dict[category] = 1
		return self.dict[category]

	def reset(self, category):
		self.dict[category] = 0

def _doNothing(canvas, doc):
	"Dummy callback for onPage"
	pass
