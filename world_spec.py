class WorldSpec(object):
	def __init__(self, world_file="world_enhanced.dat"):
		self.x_width = 10
		self.y_width = 10
		self.x_player_start = 0
		self.y_player_start = 0
		self.walls = []
		self.specials = []
		self.__world_reader(world_file)

	def __world_reader(self, world_file):
		with open(f"./worlds/{world_file}", "r") as f:
			self.x_width = int(f.readline().split(":")[1].strip())
			self.y_width = int(f.readline().split(":")[1].strip())
			self.x_player_start = int(f.readline().split(":")[1].strip())
			self.y_player_start = int(f.readline().split(":")[1].strip())

			# Skip the walls keyword
			line = f.readline().strip()
			line = f.readline().strip()

			while(line != "specials"):
				x, y = line.strip().split(",")
				self.walls.append((int(x),int(y)))
				line = f.readline().strip()

			line = f.readline().strip()
			while line:
				x, y, color, reward, variable = line.strip().split(",")
				self.specials.append([int(x),int(y), color.strip(), int(reward), "True" == variable.strip()])
				line = f.readline().strip()


