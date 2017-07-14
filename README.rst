# Dyspatch: Framework providing dispatchers primitives and systems

Any project becoming big enough will eventualy implement it's own dispatcher. The most common use cases are routing (Django's urls.py, flask @route, etc) and events (tkinter's command, django's signals, etc).

All projects implements theirs versions, duplicating tests and documentation, increasing learning time, and adding a new, slightliy different API.

Dyspatch is an attemps at implementing primitives for dispatchers and high level systems so you can either use one of the tools provided out of the box, or build your own one with solid building blocks.

To manage this, we plan to build copy cat of popular projects' existing dispatchers and inject our own code and make sure their unit tests pass.
