import pygame
import easygui

pygame.init()
pygame.font.init()

window_width, window_height = 1920, 1080
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

bg_image_path = easygui.fileopenbox()
if bg_image_path is not None:
    bg_image = pygame.image.load(bg_image_path).convert()

def resize_bg_image():
    # Resize the background image to match the size of the window
    bg_image_rect = bg_image.get_rect()
    bg_image_rect.width = window.get_width()
    bg_image_rect.height = window.get_height()
    return pygame.transform.scale(bg_image, (bg_image_rect.width, bg_image_rect.height))

bg_image = resize_bg_image()

images = []
selected_image = None

# Define the dimensions of the right column
right_column_width = 150
right_column_height = window_height
right_column_x = window_width - right_column_width
right_column_y = 0

# Define the dimensions of each text box in the right column
text_box_width = 150
text_box_height = window_height // 10

# Create a list of text boxes in the right column
text_boxes = []
for i in range(10):
    text_box_rect = pygame.Rect(window_width - text_box_width, i * text_box_height, text_box_width, text_box_height)
    text_boxes.append({"rect": text_box_rect, "text": ""})

# Create a font object for the text boxes
font = pygame.font.Font(None, 24)

# Create a list of text boxes in the right column
text_boxes = [{"rect": pygame.Rect(right_column_x, 0, text_box_width, text_box_height), "text": "Turn Number"}]
for i in range(1, 10):
    text_box_rect = pygame.Rect(right_column_x, i * text_box_height, text_box_width, text_box_height)
    text_boxes.append({"rect": text_box_rect, "text": ""})

def resize_image(image, new_width, new_height):
    # Scale the image to the new size
    return pygame.transform.scale(image, (new_width, new_height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.VIDEORESIZE:
            # Resize the window and background image
            window_width, window_height = event.w, event.h
            window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            bg_image = resize_bg_image()

            # Update the dimensions of the text boxes
            text_box_height = window_height // 10
            for i in range(10):
                text_box_rect = pygame.Rect(window_width - text_box_width, i * text_box_height, text_box_width, text_box_height)
                text_boxes[i]["rect"] = text_box_rect

            # Update the dimensions of the right column and text boxes
            right_column_height = window_height
            for i in range(10):
                text_box_rect = pygame.Rect(window_width - text_box_width, i * text_box_height, text_box_width, text_box_height)
                text_boxes[i] = text_box_rect

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if selected_image is not None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        # Increase the size of the selected image
                        selected_image["rect"].width += 10
                        selected_image["rect"].height += 10
                        selected_image["image"] = resize_image(selected_image["original_image"], selected_image["rect"].width, selected_image["rect"].height)
                    elif event.button == 5:
                        # Decrease the size of the selected image
                        selected_image["rect"].width -= 10
                        selected_image["rect"].height -= 10
                        selected_image["image"] = resize_image(selected_image["original_image"], selected_image["rect"].width, selected_image["rect"].height)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if the mouse click is inside a text box
                        for i, text_box in enumerate(text_boxes):
                            if text_box.collidepoint(event.pos):
                                print(f"Clicked on text box {i}")

            # Check if an image was clicked
            image_clicked = False
            for i in range(len(images) - 1, -1, -1):
                if images[i]["rect"].collidepoint(mouse_pos):
                    selected_image = images[i]
                    selected_image["dragging"] = True
                    selected_image["drag_offset"] = (mouse_pos[0] - selected_image["rect"].x, mouse_pos[1] - selected_image["rect"].y)
                    image_clicked = True
                    break

            # If no image was clicked, clear the selected_image variable
            if not image_clicked:
                selected_image = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_image is not None:
                selected_image["dragging"] = False

        elif event.type == pygame.MOUSEMOTION:
            if selected_image is not None and selected_image["dragging"]:
                mouse_pos = pygame.mouse.get_pos()
                selected_image["rect"].x = mouse_pos[0] - selected_image["drag_offset"][0]
                selected_image["rect"].y = mouse_pos[1] - selected_image["drag_offset"][1]

        elif event.type == pygame.KEYDOWN:
            if selected_image is not None:
                if event.key == pygame.K_MINUS:
                    # Decrease the size of the selected image
                    selected_image["rect"].width -= 10
                    selected_image["rect"].height -= 10
                    selected_image["image"] = resize_image(selected_image["original_image"], selected_image["rect"].width, selected_image["rect"].height)
                elif event.key == pygame.K_EQUALS:
                    # Increase the size of the selected image
                    selected_image["rect"].width += 10
                    selected_image["rect"].height += 10
                    selected_image["image"] = resize_image(selected_image["original_image"], selected_image["rect"].width, selected_image["rect"].height)
                elif event.key == pygame.K_DELETE:
                    # Remove the selected image from the images list
                    images.remove(selected_image)
                    selected_image = None
                elif event.type == pygame.KEYDOWN:
                    # Handle key presses in the text boxes
                    for text_box in text_boxes:
                        if text_box["rect"].collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                text_box["text"] = text_box["text"][:-1]
                            else:
                                text_box["text"] += event.unicode

        elif event.type == pygame.DROPFILE:
            file_path = event.file
            if file_path.endswith(".jpg") or file_path.endswith(".png"):
                image = pygame.image.load(file_path)
                rect = image.get_rect()
                rect.x = 0
                rect.y = 0
                images.append({"original_image": image, "image": image, "rect": rect, "dragging": False})

    # Draw the background image
    window.blit(bg_image, (0, 0))

    # Draw the right column
    right_column_surface = pygame.Surface((right_column_width, right_column_height), pygame.SRCALPHA)
    right_column_surface.fill((255, 255, 255, 128))
    window.blit(right_column_surface, (right_column_x, right_column_y))

    # Draw the text boxes in the right column
    for i, text_box in enumerate(text_boxes):
        pygame.draw.rect(window, (255, 255, 255), text_box)
        text = font.render(f"Text Box {i}", True, (255, 255, 255))
        text_rect = text.get_rect(center=text_box.center)
        window.blit(text, text_rect)

    pygame.display.update()