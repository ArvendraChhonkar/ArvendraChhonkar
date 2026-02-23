import os
import re
import random
import requests
from PIL import Image, ImageDraw

def get_real_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    try:
        # Fetch the actual HTML of your GitHub graph
        response = requests.get(url, timeout=10)
        # Extract the contribution levels (0 = no commits, 1-4 = commits)
        levels = re.findall(r'data-level="(\d)"', response.text)
        if levels:
            return [int(lvl) for lvl in levels]
    except Exception as e:
        print(f"Error fetching data: {e}")
    # Fallback if fetch fails
    return [0] * (30 * 7)

def generate_gif():
    width, height = 800, 300
    frames = []
    
    username = os.getenv("USERNAME", "ArvendraChhonkar")
    all_levels = get_real_contributions(username)
    
    # Grid settings
    cols, rows = 30, 7
    tile_size = 15
    padding = 4
    start_x = (width - (cols * (tile_size + padding))) // 2
    start_y = 50

    # Get the last 30 weeks of data to fit the screen
    recent_levels = all_levels[-210:] if len(all_levels) >= 210 else all_levels
    
    # GitHub Contribution Colors
    colors = {
        0: (22, 27, 34),    # Dark grey (0 commits)
        1: (14, 68, 41),    # Light green
        2: (0, 109, 50),    # Medium green
        3: (38, 166, 65),   # Bright green
        4: (57, 211, 83)    # Brightest green
    }

    empty_blocks = []
    filled_blocks = []
    
    # Build the grid based on your REAL data
    for idx, level in enumerate(recent_levels):
        c = idx // rows
        r = idx % rows
        if c >= cols: break
        
        x = start_x + c * (tile_size + padding)
        y = start_y + r * (tile_size + padding)
        
        if level == 0:
            empty_blocks.append([x, y, True]) # True means active/unbroken target
        else:
            filled_blocks.append([x, y, colors.get(level, colors[4])])

    # Spaceship Settings
    ship_x = start_x
    ship_y = height - 40
    ship_direction = 1
    ship_speed = 8
    lasers = []
    
    # Stars for background
    stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(70)]

    # Generate the animation frames
    for frame_num in range(120): # Increased frames to give time to shoot!
        img = Image.new('RGB', (width, height), color=(13, 17, 23)) 
        draw = ImageDraw.Draw(img)
        
        # Draw Stars
        for i, (sx, sy) in enumerate(stars):
            draw.point((sx, sy), fill=(100, 100, 100))
            stars[i] = (sx, (sy + 2) % height)

        # Draw Real Commits (Green Blocks)
        for x, y, color in filled_blocks:
            draw.rounded_rectangle([x, y, x+tile_size, y+tile_size], radius=3, fill=color)

        # Draw Target Commits (Grey Blocks)
        for x, y, active in empty_blocks:
            if active:
                draw.rounded_rectangle([x, y, x+tile_size, y+tile_size], radius=3, fill=colors[0])

        # Spaceship AI - Sweeps back and forth aggressively 
        ship_x += ship_speed * ship_direction
        if ship_x > start_x + cols * (tile_size + padding):
            ship_direction = -1
        elif ship_x < start_x:
            ship_direction = 1
        
        # Fire lasers rapidly!
        if frame_num % 2 == 0:
            lasers.append([ship_x, ship_y - 20])

        # Animate Lasers & Check Collisions
        for l in lasers[:]:
            l[1] -= 25 # Move laser up
            draw.line([(l[0], l[1]), (l[0], l[1]+15)], fill=(255, 123, 114), width=4)
            
            # Hit detection for grey blocks only
            for b in empty_blocks:
                if b[2] and b[0] <= l[0] <= b[0]+tile_size and b[1] <= l[1] <= b[1]+tile_size:
                    b[2] = False # Destroy it!
                    draw.ellipse([l[0]-15, l[1]-15, l[0]+15, l[1]+15], fill=(255, 165, 0)) # Explosion
                    if l in lasers: lasers.remove(l)
                    break 

        # Draw Spaceship
        draw.polygon([(ship_x, ship_y), (ship_x-15, ship_y+20), (ship_x+15, ship_y+20), (ship_x, ship_y+10)], fill=(88, 166, 255))
        draw.polygon([(ship_x, ship_y), (ship_x-5, ship_y+10), (ship_x+5, ship_y+10)], fill=(255, 255, 255)) 

        frames.append(img)

    # Save the final GIF
    frames[0].save("inverted-shooter.gif", save_all=True, append_images=frames[1:], duration=40, loop=0)
    print("Real-data animation generated: inverted-shooter.gif")

if __name__ == "__main__":
    generate_gif()
