def ChangeColorImage(filepath, color):
     from PIL import Image
     picture = Image.open(filepath)

     # Get the size of the image
     (width, height) = picture.size

     # Process every pixel
     for x in range(width):
          for y in range(height):
               current_color = picture.getpixel( (x,y) )
               if (current_color[3] != 0):
                    picture.putpixel( (x,y),
                                      (int(255*((current_color[0]/255)*(color[0]/255)))
                                       ,int(255*((current_color[1]/255)*(color[1]/255)))
                                       ,int(255*((current_color[2]/255)*(color[2]/255)))))
     path = filepath
     pathDot = ""
     change = False
     for c in path:
          if c == ".":
               change = True
          if change == True:
               pathDot += c
     path = path.replace(pathDot, "")
     picture.save(path + "ByColor.png")
     
def ResetColorImage(filepath, beforecolor):
     from PIL import Image
     picture = Image.open(filepath)

     # Get the size of the image
     (width, height) = picture.size

     # Process every pixel
     for x in range(width):
          for y in range(height):
               current_color = picture.getpixel( (x,y) )
               if (current_color[3] != 0):
                    picture.putpixel( (x,y),
                                      (int(255*((current_color[0]/255)/(beforecolor[0]/255)))
                                       ,int(255*((current_color[1]/255)/(beforecolor[1]/255)))
                                       ,int(255*((current_color[2]/255)/(beforecolor[2]/255)))))
     path = filepath
     pathDot = ""
     change = False
     for c in path:
          if c == ".":
               change = True
          if change == True:
               pathDot += c
     path = path.replace(pathDot, "")
     os.remove(filepath)
     picture.save(path + "ByColor.png")
ChangeColorImage("spaceship.png", (63, 72,204))
