class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene_function):
        """
        Add a new scene to the manager.
        
        Parameters:
        - name: Name of the scene
        - scene_function: Function to execute the scene's logic
        """
        self.scenes[name] = scene_function

    def switch_scene(self, name):
        """
        Switch to a different scene.
        
        Parameters:
        - name: Name of the scene to switch to
        """
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def update(self):
        """
        Update the current scene.
        """
        if self.current_scene:
            self.current_scene()
