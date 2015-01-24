-------
Modules
-------
| Module        | Usage                                       |
| ------------- |---------------------------------------------------------------------|
| ArgParser     | parser for arguments passed to executive.                           |
| Config        | load global_config.                                                 |
| Core          | core of the blog engine.                                            |
| Error         | defines all kinds of exceptions.                                    |
| Loader        | `Loader` used during the loading process of site generation.        |
| Log           | log module.                                                         |
| MkTransfer    | extend markdown features                                            |
| Post          | `Post` class used to all kinds info about posts and pages.          |
| Generator     | `Generator` used in the last stage of site generation.              |
| Processor     | `Processor` used in the second processing stage of site generation. |
| Util          | utilities used in all part of this app.                             |
| Plugin        | implement plugin registration procdure.                             |

----------------------
Operation on PandaBlog
----------------------
```
USAGE: panda [operation]

The operation can be:
    generate          generate the entire site based on content in src folder
    clean             clean the entire file structure in public folder
    force-generate    clean the record and regenerate
```

--------------------
Generation Algorithm
--------------------
* In later description, we will refer to the making of a single page as `compilation`, the process of producing the entire website as `generation`. The markdown files as `source file`, `post` and `page` as `article`.
* In the generation process, we will minimalize the html file change because this will make the update of a static website easier, otherwise we will lose one of the most valuable features of static blog.

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
* Each article is uniquely identified by its filename. Each filename denote a single article.
* Each article may explicit own an `url` attribute, which will be referred in generation process to specify the url of the article. However, multiple article may own the same url. So, to avoid conflict, we will append a number after the url. Older article has more priority on determining its url.
* A article is *altered* when its component has been modified.

Generation of the site was each handled by **Loader**, **Processor**, and **Generator**:
#### Loader
* Before the generation, we keep a record of the previous generation. In this record, we store all posts' hash value during the previous generation and the datetime of the previous generation. [`Loader`]
* Then, scan the entire `src` folder, will read every files and calculate their hash values. [`Loader`]

#### Processor
* Sort the pages and posts by their datetime.
* Determine real url with define conflict resolve protocol.
* Draw a graph on how articles and archives are related for further analyzation.
* Mark article that need compilation.

#### Generator
* Compile marked article. Delete obsolete file.
* Generate site content for archives. Delete obsolete file.
* Generate `index.html` Delete obsolete file.

TODO: Add description on how to handle `assets` folder.