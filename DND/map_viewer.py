import pygame
import easygui
import pygame_textinput

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
text_box_width = right_column_width
text_box_height = right_column_height // 10

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

            # Update the dimensions of the right column and text boxes
            right_column_height = window_height
            right_column_y = 0
            text_box_height = right_column_height // 10
            for i in range(10):
                text_box_rect = pygame.Rect(right_column_x, i * text_box_height, text_box_width, text_box_height)
                text_boxes[i]["rect"] = text_box_rect

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

        elif event.type == pygame.DROPFILE:
            file_path = event.file
            if file_path.endswith(".jpg") or file_path.endswith(".png"):
                image = pygame.image.load(file_path)
                rect = image.get_rect()
                rect.x = 0
                rect.y = 0
                images.append({"original_image": image, "image": image, "rect": rect, "dragging": False})

    window.blit(bg_image, (0, 0))

    # Draw images
    for image in images:
        if image == selected_image:
            pygame.draw.rect(window, (255, 0, 0), image["rect"], 2)
        window.blit(image["image"], image["rect"])

    # Draw the right column and text boxes
    pygame.draw.rect(window, (255, 255, 255), (right_column_x, right_column_y, right_column_width, right_column_height))
    for text_box in text_boxes:
        pygame.draw.rect(window, (0, 0, 0), text_box["rect"], 1)
        font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
        text_surface = font.render(text_box["text"], True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = text_box["rect"].center
        window.blit(text_surface, text_rect)

    pygame.display.update()