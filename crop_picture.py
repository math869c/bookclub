from PIL import Image
# Load the new image
new_image_path = "images/demo/backgrounds/shelf_superold.jpeg"
new_image = Image.open(new_image_path)

# Define the crop box to remove the left part with the text
new_width, new_height = new_image.size
new_crop_box = (new_width // 30, 0, new_width, new_height)

# Crop the image
new_cropped_image = new_image.crop(new_crop_box)

# Save the cropped image
new_cropped_image_path = "images/demo/backgrounds/shelf.jpeg"
new_cropped_image.save(new_cropped_image_path)

new_cropped_image_path
