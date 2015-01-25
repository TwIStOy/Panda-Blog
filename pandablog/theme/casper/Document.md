####Common
Top-level variables listed in Common are used during any page generation.

| Variable name       | Description                                                          |
|---------------------|----------------------------------------------------------------------|
| `{{site_url}}`      | The url of the site.                                                 |
| `{{site_title}}`    | Title of the site.                                                   |
| `{{asset_path}}`    | url of the asset (without trailing slash).                           |
| `{{template_path}}` | url of the template.                                                 |
| `{{year}}`          | The current year.                                                    |
| `{{image}}`         | The url of the image that will display in the header, it's optional. |
| `{{title}}`         | The title of the page.                                               |
| `{{description}}`   | Description of the current page, it's optional.                      |


####Required by `index.html`

| Variable name          | Description                                         |
|------------------------|-----------------------------------------------------|
| `{{site_logo}}`        | url of the logo of the site.                        |
| `{{site_description}}` | Description of the site.                            |
| `{{posts}}`            | A list of `post`.                                   |


####Required by `post.html`


| Variable name       | Description                                           |
|---------------------|-------------------------------------------------------|
| `{{content}}`       | Content of the single post.                           |
| `{{datetime}}`      | datetime of the single post.                          |
| `{{previous_url}}`  | url of previous post of this post .                   |
| `{{next_url}}`      | url of next post of this post.                        |
| `{{tags}}`          | A list of `tag`.                                      |
| `{{author}}`        | An `author` of this single post.                      |


####Required by `page.html`

| Variable name       | Description                                           |
|---------------------|-------------------------------------------------------|
| `{{content}}`       | Content of the page.                                  |
| `{{title}}`         | Title of the page.                                    |


####Required by `archive.html`


| Variable name  | Description                                           |
|----------------|-------------------------------------------------------|
| `{{posts}}`    | List of `post` in the archive                         |


####Tag object

| Variable name        | Description                                          |
|----------------------|------------------------------------------------------|
| `{{tag.name}}`       | Display name of the tag.                             |
| `{{tag.url}}`        |                                                      |


####Author object

| Variable name          | Description                                           |
|------------------------|-------------------------------------------------------|
| `{{author.url}}`       |                                                       |
| `{{author.image}}`     |                                                       |
| `{{author.name}}`      |                                                       |
| `{{author.location}}`  |                                                       |
| `{{author.bio}}`       | Biography of the author                               |
| `{{author.website}}`   |                                                       |


####Post object

| Variable name        | Description                                           |
|----------------------|-------------------------------------------------------|
| `{{post.title}}`     | Post title                                            |
| `{{post.content}}`   | Content of the post                                   |
