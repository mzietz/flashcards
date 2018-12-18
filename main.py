#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import json
import os
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty, NumericProperty
from operator import itemgetter, attrgetter
from jsonlibrary import *


class SwipeManager(ScreenManager):
	pass
class PageOne(Screen):
	pass
class PageTwo(Screen):
	pass
class VocabPage(Screen):
	picture = StringProperty("data/pictures/app_welcome.png")
	text = StringProperty('Swipecards')
class OptionPage(Screen):
	pass
class HomePage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('Welcome')

class ChunkPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('Progress Saved')

class SwipeCardsApp(App):
	vocab1 = StringProperty()
	vocab2 = StringProperty()
	answer1 = StringProperty()
	answer2 = StringProperty()
	def build(self):
		kivy.Config.set('graphics', 'width',  380)
		kivy.Config.set('graphics', 'height', 610)
		self.title = 'Swiper'
		self.sm = SwipeManager()
		self.sm.transition = SlideTransition(duration=.4, direction='left')
		self.homepage = HomePage(name = 'home')
		self.vocabpage = VocabPage(name = 'vocab')
		self.pageone = PageOne(name ='pageone')
		self.pagetwo = PageTwo(name ='pagetwo')
		self.sm.add_widget(self.homepage)
		self.sm.add_widget(self.vocabpage)
		self.sm.add_widget(self.pageone)
		self.sm.add_widget(self.pagetwo)
		self.sm.current = 'home'
#		self.init()
		return self.sm

	def init(self):
#		print "init"
		self.lib = Library()
		self.lib.loadVocabs("Deutsch")
		self.lib.loadProgress()
		self.lib.chunkSize = 4
		self.lib.setChunks()
		self.lib.currentChunk = self.lib.nextChunk()
		self.lib.nextCard()
		self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
		self.answer1 = ""
		self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
		self.answer2 = ""
		self.answered = False
		self.lib.difficulty = 0

	def to_vocab(self):
		self.sm.transition.direction = 'left'
		self.sm.current = 'vocab'

	def go_from_welcome(self):
		self.sm.transition.direction = 'left'
		self.init()
		self.sm.current = 'pageone'

	def go_to_vocab(self):
		self.sm.transition.direction = 'left'
		self.vocabpage.picture = "data/pictures/blackboard.png"
		self.vocabpage.text = 'Progress saved'
		self.sm.current = 'vocab'
		print "vocab"

	def go_to_one(self, direction):
#		print("go to one")
		self.answered = False
		if self.lib.cardsLeft() == 1 and direction == 'left':
			self.lib.saveProgress()
			self.go_to_vocab()
		else:	
			if direction == 'left':
				self.lib.iknowCard()
			elif direction == 'right':
				self.lib.idontknowCard()
#				print self.lib.difficulty
			self.lib.nextCard()
			self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
			self.answer1 = ""
			self.sm.transition.direction = direction
			self.sm.current = 'pageone'

	def go_to_two(self, direction):
#		print("go to two")
		self.answered = False
		if self.lib.cardsLeft() == 1 and direction == 'left':
			self.lib.saveProgress()
			self.go_to_vocab()
		else:
			if direction == 'left':
				self.lib.iknowCard()
			elif direction == 'right':
				self.lib.idontknowCard()
#				print self.lib.difficulty

			self.lib.nextCard()
			self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
			self.answer2 = ""
			self.sm.transition.direction = direction
			self.sm.current = 'pagetwo'
	
	def show_answer(self, screen):
		if screen == self.pageone:
			self.answer1 = self.lib.library[self.lib.currentCard]["answer"]
		elif screen == self.pagetwo:
			self.answer2 = self.lib.library[self.lib.currentCard]["answer"]
	
	def touchdown(self, touch):
		self.coordinate = touch.x

	def touchup(self, touch):
		self.distance = touch.x - self.coordinate		
		if self.sm.current == "vocab":
			if self.distance < -50:
				self.go_from_welcome()
#			if self.distance > 50:
#				self.go_from_welcome()
		else:
			if self.answered ==False:
				if self.sm.current == 'pageone':
					self.show_answer(self.pageone)
				elif self.sm.current == 'pagetwo':
					self.show_answer(self.pagetwo)
				self.answered = True
			else:
				if self.sm.current == "pageone" and self.answered:
					if self.distance > 50:
						self.go_to_two('right')
					elif self.distance < -50:
						self.go_to_two('left')

				elif self.sm.current == "pagetwo" and self.answered:			
					if self.distance > 50:
						self.go_to_one('right')
					elif self.distance < -50:
						self.go_to_one('left')

if __name__ == '__main__':
	SwipeCardsApp().run()