import math
import os
import pygame
import cv2  # Import OpenCV
import numpy as np

# Initialize Pygame
pygame.init()

# Set the window size
size = (800, 800)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Celestial Exploratory")



# Function to load and resize images using OpenCV, and remove the background
def load_image_with_transparency(image_path, size):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image.shape[2] == 4:  # If the image has an alpha channel
        alpha_channel = image[:, :, 3]
        mask = alpha_channel != 0
        new_image = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2RGB)
        new_image[~mask] = (0, 0, 0)
        new_image = cv2.resize(new_image, size)
        alpha_channel = cv2.resize(alpha_channel, size)
        result = np.dstack((new_image, alpha_channel))
    else:
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        new_image = cv2.resize(new_image, size)
        result = np.dstack((new_image, np.ones(size, dtype=np.uint8) * 255))

    return pygame.image.frombuffer(result.tobytes(), result.shape[1::-1], "RGBA")


# Load the images for each planet using OpenCV with transparency
sun_image = load_image_with_transparency(os.path.join("planets", "sun.png"), (80, 80))
mercury_image = load_image_with_transparency(os.path.join("planets", "mercury.png"), (15, 15))
venus_image = load_image_with_transparency(os.path.join("planets", "venus.png"), (25, 25))
earth_image = load_image_with_transparency(os.path.join("planets", "earth.png"), (30, 30))
mars_image = load_image_with_transparency(os.path.join("planets", "mars.png"), (20, 20))
jupiter_image = load_image_with_transparency(os.path.join("planets", "jupiter.png"), (50, 50))
saturn_image = load_image_with_transparency(os.path.join("planets", "saturn_ring.png"), (100, 40))
uranus_image = load_image_with_transparency(os.path.join("planets", "uranus.png"), (35, 35))
neptune_image = load_image_with_transparency(os.path.join("planets", "neptune.png"), (40, 40))

# Load the background image using OpenCV
background_image = load_image_with_transparency(os.path.join("planets", "space.png"), (800, 800))

# Create a list of planets with their properties
planets = [
    {"name": "Sun", "image": sun_image, "radius": 200, "x": 400, "y": 390, "vx": 0, "vy": 0},
    {"name": "Mercury", "image": mercury_image, "angle": 0, "distance": 65, "period": 0.24, "radius": 10},
    {"name": "Venus", "image": venus_image, "angle": 0, "distance": 90, "period": 0.62, "radius": 20},
    {"name": "Earth", "image": earth_image, "angle": 0, "distance": 125, "period": 1, "radius": 25},
    {"name": "Mars", "image": mars_image, "angle": 0, "distance": 155, "period": 1.88, "radius": 15},
    {"name": "Jupiter", "image": jupiter_image, "angle": 0, "distance": 195, "period": 11.86, "radius": 45},
    {"name": "Saturn", "image": saturn_image, "angle": 0, "distance": 260, "period": 29.5, "radius": 40},
    {"name": "Uranus", "image": uranus_image, "angle": 0, "distance": 320, "period": 84, "radius": 30},
    {"name": "Neptune", "image": neptune_image, "angle": 0, "distance": 370, "period": 164.8, "radius": 35}
]

# Initialize the positions of the planets
for planet in planets[1:]:
    planet["x"] = planets[0]["x"] + math.cos(planet["angle"]) * planet["distance"]
    planet["y"] = planets[0]["y"] + math.sin(planet["angle"]) * planet["distance"]

# Create a list of past positions for each planet
for planet in planets[1:]:
    planet["past_positions"] = []

# Load sounds for each planet
click_sound_sun = pygame.mixer.Sound(os.path.join("sounds", "sun_sound.mp3"))
click_sound_mercury = pygame.mixer.Sound(os.path.join("sounds", "mercury_sound.mp3"))
click_sound_venus = pygame.mixer.Sound(os.path.join("sounds", "venus_sound.mp3"))
click_sound_earth = pygame.mixer.Sound(os.path.join("sounds", "earth_sound.mp3"))
click_sound_mars = pygame.mixer.Sound(os.path.join("sounds", "mars_sound.mp3"))
click_sound_jupiter = pygame.mixer.Sound(os.path.join("sounds", "jupiter_sound.mp3"))
click_sound_saturn = pygame.mixer.Sound(os.path.join("sounds", "saturn_sound.mp3"))
click_sound_uranus = pygame.mixer.Sound(os.path.join("sounds", "uranus_sound.mp3"))
click_sound_neptune = pygame.mixer.Sound(os.path.join("sounds", "neptune_sound.mp3"))

# Load the universe sound
universe_sound = pygame.mixer.Sound(os.path.join("sounds", "universe_sound.mp3"))

# Start the universe sound
universe_sound.play(-1)

# Define the speech text for each planet
planet_speech = {
    "Sun": "I am the Sun, the heart of the Solar System, a massive sphere of plasma radiating light and heat. My gravitational pull holds the planets in their orbits, and my energy supports life on Earth. I am a constant, unyielding force, burning brightly at the center of it all.",
    "Mercury": "As Mercury, I am the swift messenger of the Solar System, tracing a graceful path around the Sun in a dance of extremes. My surface is a testament to cosmic violence, scarred by countless impacts yet holding secrets of the universe's infancy. Days scorch under unrelenting sunlight, while nights freeze in eternal darkness. My iron heart beats faintly, a core generating a feeble magnetic shield against the Sun's tempestuous winds. Though small, I embody resilience and endurance, a silent witness to the grandeur and harshness of the cosmic stage around me.",
    "Venus": "As Venus, I am cloaked in a veil of perpetual mystery and beauty. Swathed in thick clouds of sulfuric acid, I reflect sunlight with a serene radiance visible even from Earth. My surface is a tumultuous landscape of volcanic plains and towering mountains, shaped by ancient cataclysms. A runaway greenhouse effect envelopes me in searing heat, making me the hottest planet in the Solar System. Yet amidst this hostile environment, I harbor secrets of potential past oceans and atmospheric evolution. I am a planet of contrasts—both enchanting and forbidding—a celestial enigma awaiting further exploration and understanding.",
    "Earth": "As Earth, I am a blue jewel in the vastness of space, adorned with swirling oceans, verdant landscapes, and towering mountains. My atmosphere is a delicate shield, nurturing life with a perfect balance of gases. From space, I appear serene yet dynamic, with weather systems sculpting my surface and shaping climates. I am home to a rich tapestry of life forms, from the depths of oceans to the heights of mountains. Humanity has flourished on my surface, building civilizations, exploring my wonders, and contemplating the mysteries of the cosmos. I am a planet of diversity, beauty, and interconnected ecosystems—a precious oasis in the cosmos.",
    "Mars": "As Mars, I am the red planet, a world of striking contrasts and ancient wonders. My rusty surface bears the scars of colossal volcanoes, deep canyons like Valles Marineris, and the remnants of vast, dry riverbeds. Dusty winds sweep across my barren landscapes, shaping dunes and painting the skies with hues of ochre. At my poles, caps of ice shimmer beneath thin atmospheres. I am a planet of exploration, where rovers traverse rocky terrain, seeking clues to my watery past and potential for life. Mars, the frontier of human ambition and scientific inquiry—a testament to the enduring spirit of exploration.",
    "Jupiter": "As Jupiter, I am the colossal giant of the Solar System, a swirling mass of clouds and storms. My Great Red Spot, a tempest that has raged for centuries, is a symbol of my dynamic atmosphere. Bands of clouds stretch across my vast expanse, while moons like Io and Europa orbit in a dance of gravity. I am a planet of extremes, with crushing pressures and intense magnetic fields. Jupiter, the king of planets, a majestic guardian of the outer Solar System—a realm of mystery and wonder.",
    "Saturn": "As Saturn, I am the elegant giant adorned with a crown of rings, a mesmerizing spectacle in the night sky. My rings, composed of countless icy particles, shimmer like cosmic jewels. Titan, my largest moon, hides beneath a thick atmosphere, while Enceladus spews geysers of water into space. I am a planet of grandeur, second in size only to Jupiter, with a composition of hydrogen and helium. Saturn, the ringed jewel of the Solar System—a planet of beauty, mystery, and scientific fascination.",
    "Uranus": "As Uranus, I am the icy giant of the Solar System, a world tilted on its side with a faint ring system and a host of icy moons. My atmosphere is composed mainly of hydrogen and helium, with traces of methane giving me a pale blue hue. Despite my frigid temperatures, I possess a dynamic atmosphere with winds and cloud patterns. I am unique among the planets, rotating on my side like a rolling ball through space, likely due to a cataclysmic collision in the ancient past. Uranus, the enigmatic ice giant—a planet of curiosity and intrigue, awaiting further exploration and understanding.",
    "Neptune": "As Neptune, I am the distant blue giant of the Solar System, a world of frigid temperatures, turbulent storms, and a mysterious dark spot. My atmosphere is composed mainly of hydrogen, helium, and methane, giving me a vivid blue hue. Winds race through my atmosphere, creating dark storms like the Great Dark Spot—a swirling vortex larger than Earth. I am a planet of extremes, with temperatures plunging to icy depths yet harboring dynamic weather patterns. Neptune, the blue jewel of the outer Solar System—a planet of mystery and scientific discovery, beckoning explorers to unveil its secrets."
}


# Function to print text to the console
def print_text(text):
    print(text)


# Set the frame rate
fps = 60
clock = pygame.time.Clock()

# Start the main game loop
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                paused = not paused
                if paused:
                    universe_sound.stop()
                else:
                    universe_sound.play(-1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and paused:
            mouse_x, mouse_y = event.pos
            for planet in planets:
                image_rect = planet["image"].get_rect()
                image_rect.center = (int(planet["x"]), int(planet["y"]))
                if image_rect.collidepoint(mouse_x, mouse_y):
                    if planet["name"] == "Sun":
                        click_sound_sun.play()
                        print_text(planet_speech["Sun"])
                    elif planet["name"] == "Mercury":
                        click_sound_mercury.play()
                        print_text(planet_speech["Mercury"])
                    elif planet["name"] == "Venus":
                        click_sound_venus.play()
                        print_text(planet_speech["Venus"])
                    elif planet["name"] == "Earth":
                        click_sound_earth.play()
                        print_text(planet_speech["Earth"])
                    elif planet["name"] == "Mars":
                        click_sound_mars.play()
                        print_text(planet_speech["Mars"])
                    elif planet["name"] == "Jupiter":
                        click_sound_jupiter.play()
                        print_text(planet_speech["Jupiter"])
                    elif planet["name"] == "Saturn":
                        click_sound_saturn.play()
                        print_text(planet_speech["Saturn"])
                    elif planet["name"] == "Uranus":
                        click_sound_uranus.play()
                        print_text(planet_speech["Uranus"])
                    elif planet["name"] == "Neptune":
                        click_sound_neptune.play()
                        print_text(planet_speech["Neptune"])

    if not paused:
        screen.blit(background_image, (0, 0))

        # Update the position of the planets
        for planet in planets[1:]:
            planet["angle"] += 0.05 * (1 / planet["period"])
            planet["x"] = planets[0]["x"] + math.cos(planet["angle"]) * planet["distance"]
            planet["y"] = planets[0]["y"] + math.sin(planet["angle"]) * planet["distance"]
            planet["past_positions"].append((planet["x"], planet["y"]))
            for i in range(1, len(planet["past_positions"])):
                pygame.draw.line(screen, (153, 153, 0), planet["past_positions"][i - 1], planet["past_positions"][i], 1)
            image_rect = planet["image"].get_rect()
            image_rect.center = (int(planet["x"]), int(planet["y"]))
            screen.blit(planet["image"], image_rect)

        # Draw the Sun separately to ensure it is always on top
        sun_rect = planets[0]["image"].get_rect()
        sun_rect.center = (int(planets[0]["x"]), int(planets[0]["y"]))
        screen.blit(planets[0]["image"], sun_rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
