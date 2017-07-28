# imports
import random



def who_is_user():
	print("")
	name = input("Hello, please type in your name: ")
	return name



def values(name):
	print("")
	try:
		x = int(input("Please tell me the smallest number to use: "))
		y = int(input("please tell me the largest number to use: "))
		note = "{}, the smallest number is {} and the largest number is {}.".format(name, x, y)
		status = True
	except:
		x = 0
		y = 0
		note = "I'm sorry, {}, you did not enter a number; please start the program again.".format(name)
		status = False
	finally:
		return [note, min(x, y), max(x, y), status]


def number_of_problems(name):
	print("")
	try:
		count = int(input("{}, please tell me how many problems to create: ".format(name)))
	except:
		count = 0
	finally:
		return count


def create_addition_problem(x, y, name):
	a = random.randint(x, y)
	b = random.randint(x, y)
	c = a + b
	correct = False
	while not correct:
		try:
			answer = int(input("{} + {} = ".format(a, b)))
			if answer == c:
				correct = True
				print("Good job, {}!".format(name, a, b, c))
			else:
				if answer < c:
					print("Too low; please try again.")
				else:
					print("Too high; please try again.")
		except:
			print("That's not correct; please try again.")


def create_multiplication_problem(x, y, name):
	a = random.randint(x, y)
	b = random.randint(x, y)
	c = a * b
	correct = False
	while not correct:
		try:
			answer = int(input("{} x {} = ".format(a, b)))
			if answer == c:
				correct = True
				print("Good job, {}!".format(name, a, b, c))
			else:
				if answer < c:
					print("Too low; please try again.")
				else:
					print("Too high; please try again.")
		except:
			print("That's not correct; please try again.")



def math_practice():
	name = who_is_user()
	details = values(name)
	note = details[0]
	x = details[1]
	y = details[2]
	status = details[3]
	if status:
		problems = number_of_problems(name)
		if problems == 0:
			print("You didn't enter an appropriate number; please start the program again")
		else:
			for i in range(0, problems, 1):
				create_addition_problem(x, y, name)
				print("")
		print("Great job, {}, you did all the problems.".format(name))
		print("")
	else:
		print(note)



if __name__ == "__main__":
	math_practice()