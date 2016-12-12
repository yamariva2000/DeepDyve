## A well designed project repo

Your project repo is going to demonstrate to potential employers what you're capable of. Cleaning it up and making it easy to navigate goes a long way.

### 1. Code Cleanup

Some of these are serious red flags that would raise the alarm of your potential employers and are really simple to fix!

1. Make separate folders for the different parts of your project. For example: `scrape`, `model`, `app`.
2. Run `pep8`. Make sure to do this again even if you already did! Your changes could have mucked things up! These small changes will go a long way in making your code look professional.
3. Remove extraneous files like `.pyc` files, `.ipynb_checkpoints` and `.DS_Store`. Use a [.gitignore](.gitignore) file like the one in this very repo to help you avoid these issues.
4. Make sure all code is in `.py` files ***with docstrings for all functions***.
5. Put all your code in classes or functions (aside from constants, which you should use all caps for).
6. Keep your functions short with meaningful names. A function >20 lines is probably too long.
7. Use the main block. For code that you want to run, make sure to use `if __name__ == '__main__'`.
8. Don't use lots of try/excepts! *You can probably replace it with an if statement.* If you do need to use a try/except, keep just a single line in the try block and make sure you say what error you are excepting (e.g. `except IndexError`).
9. Move any EDA out of your main code folder.
10. Ipython notebooks can be valuable for demonstrating some insights on your data, your results, or an example of how to use your code. Do not put your real code in an ipython notebook. If you're using ipython notebooks to demonstrate things, make sure to use some markdown cells to explain what's going on. Don't have large output cells that make it hard to scroll through the whole thing.

### 2. The README

Your readme should be a guide to your project. Make sure it contains these four components and that you answer the questions that are relevant to your project:

1. An overview of your project.
    * What is the goal of your project?
    * How did you accomplish this goal? (Include an explanation that's not too technical)
    * What are your results?
    * How can I see what you did? (Link to your live app!)
2. An in-depth explanation of your process
    * What algorithms and techniques did you use?
    * How did you validate your results?
    * What interesting insights did you gain?
3. How to run on my own.f
    * Give instructions for how to run your code on their computer (e.g. Run `python scraper.py` to collect the data, then run...)

### Optional

1. Code walk-through
    * Give an overview of what each section of your code does.
    * Make it clear to the reader of your repo how they should navigate your code.
    * If you have a particular bit of code you think is clever or where the meat of your work is, make sure to point it out. If you tell them what to look at, they will listen.

### Examples

Look at the [examples](readme.md#selected-alumni-examples) we've picked out.
