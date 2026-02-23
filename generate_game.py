import os
import random
from PIL import Image, ImageDraw

def generate_gif():
    width, height = 800, 300
    frames = []
    
    # 1. Setup a fake GitHub Contribution Grid
    cols, rows = 30, 7
    tile_size = 15
    padding = 4
    start_x = (width - (cols * (tile_size + padding))) // 2
    start_y = 50

    empty_blocks = []
    filled_blocks = []
    
    # Randomly populate the grid with "commits" (green) and "zero-commits" (grey)
    for c in range(cols):
        for r in range(rows):
            x = start_x + c * (tile_size + padding)
            y = start_y + r * (tile_size + padding)
            # Make ~25% of the blocks empty targets
            is_empty = random.choice([True, False, False, False]) 
            if is_empty:
                empty_blocks.append([x, y, True]) # True means it hasn't been shot yet
            else:
                filled_blocks.append([x, y])

    # 2. Setup Spaceship and Environment
    ship_x = width // 2
    ship_y = height - 40
    ship_speed = 12
    lasers = []
    
    # Generate random stars for background parallax effect
    stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(70)]

    # 3. Create the Animation Frames
    for frame_num in range(80): # 80 frames of animation
        # Dark GitHub Background
        img = Image.new('RGB', (width, height), color=(13, 17, 23)) 
        draw = ImageDraw.Draw(img)
        
        # Animate Stars falling down
        for i, (sx, sy) in enumerate(stars):
            draw.point((sx, sy), fill=(100, 100, 100))
            stars[i] = (sx, (sy + 2) % height)

        # Draw "Safe" Commits (Green Blocks)
        for x, y in filled_blocks:
            draw.rounded_rectangle([x, y, x+tile_size, y+tile_size], radius=3, fill=(57, 211, 83))

        # Draw "Target" Commits (Grey Blocks)
        active_empty = [b for b in empty_blocks if b[2]]
        for x, y, active in empty_blocks:
            if active:
                draw.rounded_rectangle([x, y, x+tile_size, y+tile_size], radius=3, fill=(48, 54, 61))

        # Spaceship AI - Track the nearest grey block
        if active_empty:
            target_x = active_empty[0][0] + tile_size // 2
            if ship_x < target_x: 
                ship_x += min(ship_speed, target_x - ship_x)
            elif ship_x > target_x: 
                ship_x -= min(ship_speed, ship_x - target_x)
            
            # Fire laser!
            if abs(ship_x - target_x) < 8 and frame_num % 4 == 0:
                lasers.append([ship_x, ship_y - 20])

        # Animate Lasers & Check Collisions
        for l in lasers[:]:
            l[1] -= 25 # Laser moves up
            # Draw Laser
            draw.line([(l[0], l[1]), (l[0], l[1]+15)], fill=(255, 123, 114), width=4)
            
            # Did laser hit a grey block?
            for b in empty_blocks:
                if b[2] and b[0] <= l[0] <= b[0]+tile_size and b[1] <= l[1] <= b[1]+tile_size:
                    b[2] = False # Destroy the block!
                    # Draw Explosion
                    draw.ellipse([l[0]-15, l[1]-15, l[0]+15, l[1]+15], fill=(255, 165, 0)) 
                    if l in lasers: lasers.remove(l)

        # Draw the Spaceship
        draw.polygon([(ship_x, ship_y), (ship_x-15, ship_y+20), (ship_x+15, ship_y+20), (ship_x, ship_y+10)], fill=(88, 166, 255))
        draw.polygon([(ship_x, ship_y), (ship_x-5, ship_y+10), (ship_x+5, ship_y+10)], fill=(255, 255, 255)) # cockpit glass

        frames.append(img)

    # 4. Compile and Save GIF
    frames[0].save(
        "inverted-shooter.gif",
        save_all=True,
        append_images=frames[1:],
        duration=40, # Frame speed
        loop=0
    )
    print("Upgraded animation generated: inverted-shooter.gif")

if __name__ == "__main__":
    generate_gif()
