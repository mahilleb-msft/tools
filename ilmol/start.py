from core.Ilmol import Ilmol

# Batch of test images.
images = ["/Users/ten/Pictures/Edited/Untitled Export/20-3.jpg","/Users/ten/Pictures/Edited/Untitled Export/21-3.jpg", "/Users/ten/Pictures/Edited/test.jpg", "/Users/ten/Pictures/Edited/Untitled Export/test2.jpg"]

ilmol = Ilmol()
ilmol.process_images(images)