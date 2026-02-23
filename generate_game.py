import os
from PIL import Image, ImageDraw

# 1. Fetch GitHub Data
username = os.getenv("USERNAME", "ArvendraChhonkar")
token = os.getenv("GITHUB_TOKEN")

def get_empty_commit_days():
    # Placeholder coordinates representing days with 0 commits.
    return [(10, 50), (30, 50), (50, 50)] 

# 2. Build the GIF Frames
def generate_gif():
    frames = []
    empty_days = get_empty_commit_days()
    
    # Create 20 frames for a simple animation
    for i in range(20):
        # Create a dark background frame
        img = Image.new('RGB', (800, 200), color=(13, 17, 23))
        draw = ImageDraw.Draw(img)
        
        # Draw the "Empty Commit" blocks
        for (x, y) in empty_days:
            draw.rectangle([x, y, x+10, y+10], fill=(48, 54, 61))
            
        # Draw the spaceship (Moving across the screen)
        ship_x = i * 40
        ship_y = 150
        draw.polygon([(ship_x, ship_y), (ship_x-10, ship_y+20), (ship_x+10, ship_y+20)], fill=(88, 166, 255))
        
        # Draw the laser shooting upwards at the empty blocks
        if i % 2 == 0:
            draw.line([(ship_x, ship_y), (ship_x, ship_y-100)], fill=(255, 123, 114), width=2)
            
        frames.append(img)
        
    # 3. Save as an animated GIF
    frames[0].save(
        "inverted-shooter.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )
    print("Animation generated: inverted-shooter.gif")

if __name__ == "__main__":
    generate_gif()
