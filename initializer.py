import pip._internal as pip
pip.main(["install", "scrapy", "docutils", "pygments"])
pip.main(["install","--no-cache-dir","pypiwin32", "kivy.deps.sdl2", "kivy.deps.glew"])
pip.main(["install", "kivy.deps.gstreamer"])
pip.main(["install", "kivy"])
