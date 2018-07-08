# 📸 Ilmol - Photo Blog Post Generator

Ilmol (_Korean:_ sunset) is a script that generates Markdown blog posts and checks them in to the final blog repository.

## Template Parameters

| Parameter | Description |
|:------|:------|
| `{{title}}` | Title for the blog posts. |
| `{{date}}` | Date at which the post was processed/generated. | 
| `{{slug}}` | URL slug for the generated image. |
| `{{url_template}}` | Template for the full image URL. |
| `{{image_name}}` | Image file name, with extension. |
| `{{description}}` | Description for the blog post. |
| `{{photo_relative_link}}` | Relative path to the image in the blog folder. |
| `{{alt_text}}` | Alternative text for the image. |
| `{{camera_model_string}}` | String identifying the camera model. |
| `{{camera_model_url}}` | URL for the camera model. |
| `{{f_number}}` | f number. |
| `{{shutter_speed}}` | Shutter speed. |
| `{{iso}}` | ISO. |
| `{{lens}}` | Lens information. |
| `{{location_string}}` | Location string representing the city and the country. |
| `{{location_url}}` | URL for the location. |