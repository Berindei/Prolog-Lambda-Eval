from abc import ABCMeta, abstractmethod

class Command(metaclass=ABCMeta):

	def __init__(self, env):
		self.env = env

	@abstractmethod
	def run(self, arglist):
		pass

	@property
	@abstractmethod
	def help(self):
		pass
	