from PIL import Image, ImageDraw, ImageOps

def draw_shape(shape, color, filename):
    # Image size
    img_size = 100
    shape_size = 50
    square_corner_radius = 15
    
    # Create a new image with transparent background
    image = Image.new("RGBA", (img_size, img_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw rounded square (background)
    square = Image.new("RGBA", (img_size, img_size), (255, 255, 255, 0))
    draw_square = ImageDraw.Draw(square)
    draw_square.rounded_rectangle([(0, 0), (img_size, img_size)],
                                  radius=square_corner_radius,
                                  fill=(214, 214, 214))  # Light gray

    # Position for the shape in the center
    shape_position = ((img_size - shape_size) // 2, (img_size - shape_size) // 2)

    if shape == "cross":
        # Draw a blue cross (vertical and horizontal rectangles)
        cross_thickness = 20
        # Vertical rectangle
        draw.rectangle([40, 20, 60, 80], fill=color)
        # Horizontal rectangle
        draw.rectangle([20, 40, 80, 60], fill=color)
    elif shape == "triangle":
        # Draw a yellow triangle
        points = [
            (img_size // 2, shape_position[1]),  # Top
            (shape_position[0], shape_position[1] + shape_size),  # Bottom left
            (shape_position[0] + shape_size, shape_position[1] + shape_size)  # Bottom right
        ]
        draw.polygon(points, fill=color)
    elif shape == "square":
        # Draw a red square
        draw.rectangle([shape_position, (shape_position[0] + shape_size, shape_position[1] + shape_size)], fill=color)
    elif shape == "circle":
        # Draw a green circle
        draw.ellipse([shape_position, 
                      (shape_position[0] + shape_size, shape_position[1] + shape_size)], 
                      fill=color)

    # Composite the shape on top of the rounded square
    final_image = Image.alpha_composite(square, image)
    
    # Save the image as a PNG file
    final_image.save(filename)
    final_image.show()

# Drawing each shape with the specified color
draw_shape("cross", (76, 182, 221), "img/blue.png")    # Blue cross
draw_shape("triangle", (252, 163, 41), "img/yellow.png")  # Yellow triangle
draw_shape("square", (240, 51, 45), "img/red.png")     # Red square
draw_shape("circle", (124, 167, 45), "img/green.png")     # Green circle
