import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=400, height=400, bg="black")
        self.canvas.pack()
        self.master.bind("<KeyPress>", self.on_keypress)

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        self.food = None
        self.obstacles = []
        self.create_enemy_snake()
        #self.enemy_snake = []
        self.enemy_direction = "Left"

        self.score = 0
        self.score_label = None
        self.snake_length_label = None  # Added snake length label

        self.game_over_text = None

        self.create_score_board()
        self.create_food()  # Initial food for the player snake
        self.create_obstacles()  # Initial obstacles

        self.update()
        self.master.bind("<KeyPress-r>", self.restart_game)

    def create_score_board(self):
        self.score_label = self.canvas.create_text(
            50, 10, text=f"Score: {self.score}", fill="white", font=("Helvetica", 10)
        )
        self.snake_length_label = self.canvas.create_text(
            350, 10, text=f"Length: {len(self.snake)}", fill="white", font=("Helvetica", 10)
        )

    def draw_snake(self, snake, color):
        self.canvas.delete(color)
        for segment in snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill=color, tags=color)

    def draw_score_board(self):
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.snake_length_label, text=f"Length: {len(self.snake)}")  # Update snake length label

    def move_snake(self, snake, direction):
        head = snake[0]
        x, y = head
    
        if direction == "Up":
            y -= 10
        elif direction == "Down":
            y += 10
        elif direction == "Left":
            x -= 10
        elif direction == "Right":
            x += 10
    
        snake.insert(0, (x, y))
    
        if head == self.food:
            self.create_food()
            self.update_score()
            self.update_snake_length()
        else:
            snake.pop()
            

        
        return snake

    def create_food(self):
        if self.food:
            x, y = self.food
            self.canvas.delete("food")
            self.food = None

        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        while (x, y) in self.snake or (x, y) in self.obstacles or (x, y) in self.enemy_snake:
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10
        self.food = (x, y)
        self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red", tags="food")

    def create_enemy_snake(self):
        self.enemy_snake = [(300, 300), (310, 300), (320, 300)]
        self.enemy_direction = "Left"

    def move_enemy_snake(self):
        if self.enemy_snake:
            head = self.enemy_snake[0]
            x, y = head

            if x < self.food[0]:
                self.enemy_direction = "Right"
            elif x > self.food[0]:
                self.enemy_direction = "Left"
            elif y < self.food[1]:
                self.enemy_direction = "Down"
            elif y > self.food[1]:
                self.enemy_direction = "Up"

            if self.enemy_direction == "Up":
                y -= 5
            elif self.enemy_direction == "Down":
                y += 5
            elif self.enemy_direction == "Left":
                x -= 5
            elif self.enemy_direction == "Right":
                x += 5

            self.enemy_snake.insert(0, (x, y))

            if self.check_enemy_collision():
                self.enemy_snake.pop()

            if head in self.snake:
                self.game_over()

            if head == self.food:
                self.create_food()
            else:
                self.enemy_snake.pop()

    def create_obstacles(self):
        for _ in range(10):
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10
            while (x, y) in self.snake or (x, y) in self.obstacles or (x, y) == self.food:
                x = random.randint(0, 39) * 10
                y = random.randint(0, 39) * 10
            self.obstacles.append((x, y))
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="blue", tags="obstacle")

    def check_collision(self):
        return (
            self.check_wall_collision() or
            self.check_self_collision() or
            self.check_obstacle_collision() or
            self.check_enemy_collision() or
            self.check_food_collision()
        )
    
    # Inside SnakeGame class
    def check_food_collision(self):
        head = self.snake[0]
        if head == self.food:
            self.score += 1
            new_segment = (self.snake[-1][0], self.snake[-1][1])
            self.snake.append(new_segment)  # Append a new segment for the user snake
            self.create_food()
            self.draw_score_board()
    
        if self.enemy_snake:  # Check if the enemy snake exists
            head_enemy = self.enemy_snake[0]
            if head_enemy == self.food:
                self.score += 1
                self.enemy_snake.append((0, 0))  # Append a new segment for the AI snake
                self.create_food()
                self.draw_score_board()


    def check_wall_collision(self):
        head = self.snake[0]
        return head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400

    def check_self_collision(self):
        return self.snake[0] in self.snake[1:]

    def check_obstacle_collision(self):
        head = self.snake[0]
        return head in self.obstacles

    def check_enemy_collision(self):
        return self.snake[0] in self.enemy_snake

    def game_over(self):
        self.master.after_cancel(self.after_id)
        self.game_over_text = self.canvas.create_text(
            200, 200, text="Game Over", fill="white", font=("Helvetica", 16)
        )
        if self.game_over_text is None:
            self.game_over_text = self.canvas.create_text(
                200, 200, text="Game Over", fill="white", font=("Helvetica", 16)
            )

    def restart_game(self, event):
        self.canvas.delete("all")
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = None
        self.obstacles = []
        self.enemy_snake = [(300, 300), (310, 300), (320, 300)]
        self.enemy_direction = "Left"
        self.score = 0
        self.game_over_text = None
        self.create_food()
        self.create_obstacles()
        self.update()
        self.create_score_board()
        self.update_score()
        self.update_snake_length()



    def update(self):
        if not self.check_collision():
            self.snake = self.move_snake(self.snake, self.direction)
            self.move_enemy_snake()
            self.check_food_collision()
            self.draw_snake(self.snake, "green")
            self.draw_snake(self.enemy_snake, "orange")
            self.draw_score_board()
            self.after_id = self.master.after(100, self.update)  # Update after_id here
        else:
            self.game_over()
            self.game_over_text = self.canvas.create_text(
                200, 200, text="Game Over", fill="white", font=("Helvetica", 16)
            )


    def on_keypress(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            opposite_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if self.direction != opposite_directions[key]:
                self.direction = key

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
