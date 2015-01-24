=======
Modules
=======
* ArgParser.py       - handle argument passed to panda executive
* Config.py          - to initialize configuration file and plugins
* Controller.py      -
* ControllerError.py -
* Loader.py          -
* Log.py             -
* MkTransfer.py      -
* Post.py            - define Post class that handles all post-related operation
* Renderer.py        -* Selector.py        -
* Util.py            - operation needed by other modules

======================
Operation on PandaBlog
======================
USAGE: panda [operation]

The operation can be:
    generate    generate the entire site based on content in src folder
    clean       clean the entire file structure in public folder

====================
Generation Algorithm
====================
* Later, we will refer to the making of a single page by the term `compilation`, the process of producing the entire website as `generation`. The markdown files as `source file`.
* In the generation process, we will minimalize the html file change because this will make the update of a static website easier, otherwise we will lose one of the most valuable feature of static blog.

There are four kinds of pages needs compilation:
* index.html
* posts
* pages
* archives

And there are four types of archives
* archives by date
* archives by tag
* archives by category
* archives by author

Before the generation, we define the following protocol for site generation:
* Each post is uniquely identified by its filename. Each filename denote a single post or page.
* Each post may explicit own an `url` attribute, which will be referred in generation process to specify the url of the post. However, multiple post/page may own the same url. So, to avoid conflict, we will append a number after the url. Older post has more priority on determining its url.
* A post is *altered* when its component has been modified.

Each generation follows the following steps:
* Before the generation, we keep a record of the previous generation. In this record, we store all posts' hash value during the previous generation and the datetime of the previous generation.
* Then, we scan the entire `src` folder, we will read every files and calculate their hash values.
* Sort the pages and posts by their datetime.
* Determine real url with define conflict resolve protocol.
* Mark pages/post that need compilation.
* Compile marked pages/post. (Delete old html, generate new html)
* Generate html for archives. (NOT COMPLETE)